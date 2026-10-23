<?php
    // UPDATE: busca el usuario por su _id y muestra el formulario ya relleno.
    require('conexion_mongo.php');

    try {
        // El _id de MongoDB no es un texto, es un ObjectId: hay que convertirlo
        $id = new MongoDB\BSON\ObjectId($_GET['id'] ?? '');
        $usu = $usuarios->findOne(['_id' => $id]);
    } catch (Exception $e) {
        $usu = null;
    }

    if (!$usu) {
        header('Location: index.php?tipo=error&mensaje=' . urlencode('Ese usuario no existe'));
        exit;
    }

    $titulo = 'Editar usuario';
    $activa = '';
    require('cabecera.php');
?>
        <a class="volver" href="index.php">‹ Usuarios</a>

        <form action="acciones.php" method="post">
            <input type="hidden" name="id" value="<?php echo htmlspecialchars((string) $usu['_id']); ?>">

            <div class="grupo campos">
                <label class="campo">
                    <span>Nombre</span>
                    <input type="text" name="nombre" value="<?php echo htmlspecialchars($usu['nombre'] ?? ''); ?>" required>
                </label>
                <label class="campo">
                    <span>Clave</span>
                    <input type="text" name="clave" value="<?php echo htmlspecialchars($usu['clave'] ?? ''); ?>" required>
                </label>
                <label class="campo">
                    <span>Rol</span>
                    <input type="number" id="rol" name="rol" value="<?php echo htmlspecialchars($usu['rol'] ?? 0); ?>" min="0" required>
                    <!-- Stepper: − baja y + sube el número del campo rol -->
                    <span class="stepper">
                        <button type="button" aria-label="Bajar rol" onclick="document.getElementById('rol').stepDown()">−</button>
                        <button type="button" aria-label="Subir rol" onclick="document.getElementById('rol').stepUp()">+</button>
                    </span>
                </label>
            </div>

            <button type="submit" name="accion" value="actualizar" class="boton boton-ancho">Guardar cambios</button>
        </form>
<?php require('pie.php'); ?>
