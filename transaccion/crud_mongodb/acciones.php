<?php
    // Archivo "trabajador": recibe el POST de crear.php, alta_transaccion.php,
    // editar.php o del botón Borrar del listado, hace la operación en MongoDB
    // y vuelve a la página que toque con un mensaje.
    require('conexion_mongo.php');

    $accion = $_POST['accion'] ?? '';
    $mensaje = '';
    $tipo = 'ok';            // 'ok' (verde) o 'error' (rojo)
    $volver = 'index.php';   // página a la que se vuelve al terminar

    try {
        switch ($accion) {

            // --- CREATE: insertOne() añade un documento nuevo ---
            case 'insertar':
                $volver = 'crear.php';
                $nombre = trim($_POST['nombre'] ?? '');
                $usuarios->insertOne([
                    'nombre' => $nombre,
                    'clave'  => $_POST['clave'] ?? '',
                    'rol'    => (int) ($_POST['rol'] ?? 0),
                ]);
                $mensaje = "Usuario $nombre guardado";
                $volver = 'index.php';
                break;

            // --- TRANSACCIÓN: dos insertOne() que se guardan juntos o no se guarda ninguno ---
            case 'insertar_transaccion':
                $nombre1 = trim($_POST['nombre1'] ?? '');
                $nombre2 = trim($_POST['nombre2'] ?? '');
                $clave = $_POST['clave'] ?? '';

                $sesion = $cliente->startSession();
                $sesion->startTransaction();
                try {
                    // cada operación lleva la sesión: así forma parte de la transacción
                    $usuarios->insertOne(['nombre' => $nombre1, 'clave' => $clave, 'rol' => 0], ['session' => $sesion]);
                    $usuarios->insertOne(['nombre' => $nombre2, 'clave' => $clave, 'rol' => 0], ['session' => $sesion]);

                    $sesion->commitTransaction();
                    $mensaje = "Transacción confirmada: se han guardado $nombre1 y $nombre2";
                } catch (MongoDB\Driver\Exception\Exception $e) {
                    // algo ha fallado: se deshace también la primera inserción
                    $sesion->abortTransaction();
                    $motivo = str_contains($e->getMessage(), 'E11000') ? 'un nombre ya existe o está repetido' : 'error de MongoDB';
                    $mensaje = "Transacción anulada ($motivo). No se ha guardado ni $nombre1 ni $nombre2";
                    $tipo = 'error';
                }
                // se vuelve al listado en los dos casos, para comprobar quién se ha guardado
                break;

            // --- UPDATE: updateOne() con $set cambia solo los campos indicados ---
            case 'actualizar':
                $id = $_POST['id'] ?? '';
                $volver = 'editar.php?id=' . urlencode($id);
                $res = $usuarios->updateOne(
                    ['_id' => new MongoDB\BSON\ObjectId($id)],
                    ['$set' => [
                        'nombre' => trim($_POST['nombre'] ?? ''),
                        'clave'  => $_POST['clave'] ?? '',
                        'rol'    => (int) ($_POST['rol'] ?? 0),
                    ]]
                );
                $mensaje = $res->getModifiedCount() > 0 ? 'Usuario actualizado' : 'No había nada que cambiar';
                $volver = 'index.php';
                break;

            // --- DELETE: deleteOne() borra el documento con ese _id ---
            case 'borrar':
                $res = $usuarios->deleteOne(['_id' => new MongoDB\BSON\ObjectId($_POST['id'] ?? '')]);
                if ($res->getDeletedCount() > 0) {
                    $mensaje = 'Usuario borrado';
                } else {
                    $mensaje = 'Ese usuario ya no existía';
                    $tipo = 'error';
                }
                break;

            default:
                $mensaje = 'Acción no válida';
                $tipo = 'error';
        }
    } catch (MongoDB\Driver\Exception\BulkWriteException $e) {
        // El código 11000 es "clave duplicada": el índice unique de nombre lo impide.
        // Se vuelve al formulario de donde se vino ($volver) para poder corregirlo.
        $mensaje = str_contains($e->getMessage(), 'E11000')
            ? 'Ya existe un usuario con ese nombre'
            : 'No se pudo completar la operación';
        $tipo = 'error';
    } catch (Exception $e) {
        $mensaje = 'No se pudo completar la operación';
        $tipo = 'error';
    }

    // Redirige (así al recargar la página no se repite el envío del formulario)
    $separador = str_contains($volver, '?') ? '&' : '?';
    header('Location: ' . $volver . $separador . 'tipo=' . $tipo . '&mensaje=' . urlencode($mensaje));
    exit;
