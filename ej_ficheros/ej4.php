<?php
    // Conexión a la base "empresa": deja creada la variable $bd (PDO)
    require __DIR__ . '/../crud_empresa/conexion.php';

    // Inserta un usuario. Codigo no se pasa porque es auto_increment.
    // Devuelve true si lo inserta y false si falla (por ejemplo, nombre repetido)
    function insertar_usuario($bd, $nombre, $clave, $rol) {
        try {
            $ins = $bd->prepare("INSERT INTO usuarios (Nombre, Clave, Rol) VALUES (?, ?, ?)");
            return $ins->execute([$nombre, $clave, $rol]);
        } catch (PDOException $e) {
            return false;
        }
    }

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // PDO solo lanza excepciones si se lo pedimos
        $bd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        if (insertar_usuario($bd, $_POST['nombre'], $_POST['clave'], $_POST['rol'])) {
            $mensaje = "Usuario " . $_POST['nombre'] . " insertado";
        } else {
            $mensaje = "No se pudo insertar. ¿Ya existe ese nombre?";
        }
    }
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insertar usuario</title>
</head>
<body>
    <h1>Nuevo usuario</h1>

    <?php if (isset($mensaje)) {
        echo "<p>" . htmlspecialchars($mensaje) . "</p>";
    } ?>

    <form action="ej4.php" method="POST">
        <label for="nombre">Nombre</label>
        <input type="text" id="nombre" name="nombre" maxlength="20" required>

        <label for="clave">Clave</label>
        <input type="password" id="clave" name="clave" maxlength="20" required>

        <label for="rol">Rol</label>
        <input type="number" id="rol" name="rol" value="0" required>

        <input type="submit" value="Insertar">
    </form>

    <p><a href="ej3.php">Ver la tabla de usuarios</a></p>
</body>
</html>
