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
    <title>Arrivederci · Categorías</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <a class="marca" href="categorias.php">Arrivederci</a>
        <nav>
            <span><?= htmlspecialchars($_SESSION['nombre']) ?></span>
            <a href="carrito.php">Ver carrito</a>
            <a href="historial.php">Mis pedidos</a>
            <a href="logout.php">Cerrar sesión</a>
        </nav>
    </header>

    <main class="contenido">
        <p class="antetitulo">Ciao <?= htmlspecialchars($_SESSION['nombre']) ?></p>
        <h1>¿Qué te apetece hoy?</h1>
        <ul class="lista-categorias">
            <?php foreach($categorias as $categoria): ?>
                <li>
                    <a class="categoria" href="productos.php?categoria=<?= $categoria->getId() ?>">
                        <div class="texto">
                            <h2><?= htmlspecialchars($categoria->getNombre()) ?></h2>
                            <p><?= htmlspecialchars($categoria->getDescripcion()) ?></p>
                            <span class="ver">Ver la carta</span>
                        </div>
                        <img src="img/categorias/<?= $categoria->getId() ?>.png" alt="">
                    </a>
                </li>
            <?php endforeach; ?>
        </ul>
    </main>
</body>
</html>