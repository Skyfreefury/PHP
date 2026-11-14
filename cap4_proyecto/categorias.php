<?php
    require_once  __DIR__ . '/clases/Sesion.php';
    require_once __DIR__ . '/clases/Categoria.php';
    Sesion::comprobar();
    $categorias = Categoria::todas();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Categorias</title>
</head>
<body>
    <h2>Ciao <?= htmlspecialchars($_SESSION['nombre']) ?></h2>
    <ul>
        <?php foreach($categorias as $categoria): ?>
            <li><a href="productos.php?categoria=<?= $categoria->getId() ?>"><?= htmlspecialchars($categoria->getNombre()) ?></a></li>
        <?php endforeach; ?>
        
    </ul>
</body>
</html>