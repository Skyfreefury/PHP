<?php
    // Conexión a la base "empresa": deja creada la variable $bd (PDO)
    require __DIR__ . '/../crud_empresa/conexion.php';
    $usuarios = $bd->query("SELECT * FROM usuarios");

    // Pinta una fila <tr> por cada usuario recibido
    function mostrar_usuarios($usuarios) {
        foreach ($usuarios as $fila => $usuario) {
            echo "<tr>";
            echo "<td>" . htmlspecialchars($usuario['Nombre']) . "</td>";
            echo "<td>" . htmlspecialchars($usuario['Codigo']) . "</td>";
            echo "<td>" . htmlspecialchars($usuario['Clave']) . "</td>";
            echo "<td>" . htmlspecialchars($usuario['Rol']) . "</td>";
            echo "</tr>";
        }
    }
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <table>
        <tr>
            <th>Nombre</th>
            <th>Codigo</th>
            <th>Clave</th>
            <th>Rol</th>
        </tr>
        <?php mostrar_usuarios($usuarios); ?>
    </table>
</body>
</html>
