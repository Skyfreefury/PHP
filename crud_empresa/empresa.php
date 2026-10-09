<?php
    require('conexion.php');
    echo "Conexión realizada con éxito<br>";

    try {
        if (isset($_POST['nombre'])) {
            $sql = $bd->prepare('SELECT nombre, clave, rol FROM usuarioss WHERE nombre = :nombre');
            $sql->bindValue(':nombre', $_POST['nombre']);
            $sql->execute();
        } else {
            $sql = $bd->prepare('SELECT nombre, clave, rol FROM usuarioss');
            $sql->execute();
        }

        $usuarios = $sql;
        echo $usuarios->rowCount(). "<br>";
        foreach ($usuarios as $row) {
            print $row['nombre']. " - ";
            print $row['clave']. "<br>";
        }
    }
    catch (PDOException $e) {
        echo "Error en la consulta: " . $e->getMessage();
    }
?>

<form action="empresa.php" method="post">
    <label for="nombre">Buscar por nombre:</label>
    <input type="text" name="nombre" id="nombre" placeholder="ana">
    <button type="submit">Buscar</button>
</form>
