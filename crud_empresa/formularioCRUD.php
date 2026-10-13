<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="bd_insert_update_delete.php" method="post">
        <label for="new_name">User Name</label>
        <input type="text" name="nombre" id="new_name" placeholder="Camilo09">
        <label for="key">Clave</label>
        <input type="password" name="clave" id="key" placeholder="****">
        <label for="rol">Rol</label>
        <input type="number" name="rol" id="rol" placeholder="0">
        <button type="submit">Insertar</button>
    </form>

    <?php

    ?>
</body>
</html>
