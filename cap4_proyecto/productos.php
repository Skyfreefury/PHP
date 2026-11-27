<?php
    require_once __DIR__ . "/clases/Sesion.php";
    require_once __DIR__ . "/clases/Producto.php";
    Sesion::comprobar();
    if (!isset($_GET['categoria'])) {
        header('Location: categorias.php');
        exit();
    }
    $idCategoria = $_GET['categoria'];
    $productos = Producto::porCategoria($idCategoria);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arrivederci · Productos</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <a class="marca" href="categorias.php">Arrivederci</a>
        <nav>
            <a href="categorias.php">Volver a categorías</a>
            <a href="carrito.php">Ver carrito</a>
            <a href="logout.php">Cerrar sesión</a>
        </nav>
    </header>

    <main class="contenido">
        <p class="antetitulo"><?= count($productos) ?> productos</p>
        <h1>Productos</h1>
        <ul class="lista-productos">
            <?php foreach ($productos as $producto): ?>
                <?php $foto = 'img/productos/' . $producto->getId() . '.png'; ?>
                <li class="producto">
                    <?php if (file_exists(__DIR__ . '/' . $foto)): ?>
                        <img class="foto" src="<?= $foto ?>" alt="">
                    <?php else: ?>
                        <div class="sin-foto" aria-hidden="true"><?= htmlspecialchars(mb_substr($producto->getNombre(), 0, 1)) ?></div>
                    <?php endif; ?>
                    <div class="datos">
                        <h2><?= htmlspecialchars($producto->getNombre()) ?></h2>
                        <p class="descripcion"><?= htmlspecialchars($producto->getDescripcion()) ?></p>
                        <span class="precio"><?= number_format($producto->getPrecio(), 2, ',', '.') ?> €</span>
                        <span class="stock"><?= $producto->getStock() ?> disponibles</span>
                        <form action="agregar-carrito.php" method="post">
                            <input type="hidden" name="id" value="<?= $producto->getId() ?>">
                            <input type="number" name="unidades" min="1" max="10" value="1" required>
                            <button type="submit">Agregar al carrito</button>
                            <input type="hidden" name="categoria" value="<?= htmlspecialchars($idCategoria) ?>">
                        </form>
                    </div>
                </li>
            <?php endforeach; ?>
        </ul>
    </main>
</body>
</html>