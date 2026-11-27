<?php
require_once __DIR__ . "/clases/Producto.php";
require_once __DIR__ . "/clases/Sesion.php";
Sesion::comprobar();

$total = 0;
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arrivederci · Carrito</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <a class="marca" href="categorias.php">Arrivederci</a>
        <nav>
            <a href="categorias.php">Volver a categorías</a>
            <a href="historial.php">Mis pedidos</a>
            <a href="logout.php">Cerrar sesión</a>
        </nav>
    </header>

    <main class="contenido">
        <h1>Tu carrito</h1>
        <?php if (isset($_GET['error'])): ?>
            <p class="aviso aviso-error">No se pudo guardar el pedido. Inténtalo de nuevo.</p>
        <?php endif; ?>
        <?php if (!empty($_SESSION["carrito"])): ?>
            <ul class="lista-carrito">
                <?php foreach ($_SESSION["carrito"] as $id => $unidades): ?>
                    <?php
                        $producto = Producto::porId($id);
                        if (!$producto) {
                            continue;
                        }
                        $subtotal = $producto->getPrecio() * $unidades;
                        $total += $subtotal;
                    ?>
                    <li class="linea-carrito">
                        <span class="nombre"><?= htmlspecialchars($producto->getNombre()) ?></span>
                        <span class="unidades"><?= $unidades ?> x <?= number_format($producto->getPrecio(), 2, ',', '.') ?> €</span>
                        <span class="subtotal"><?= number_format($subtotal, 2, ',', '.') ?> €</span>
                        <form class="editar" action="actualizar-carrito.php" method="post">
                            <input type="hidden" name="id" value="<?= $producto->getId() ?>">
                            <input type="number" name="unidades" min="1" max="10" value="<?= $unidades ?>" required>
                            <button type="submit" name="accion" value="cambiar">Actualizar</button>
                            <button type="submit" name="accion" value="eliminar" formnovalidate>Eliminar</button>
                        </form>
                    </li>
                <?php endforeach; ?>
            </ul>
            <div class="resumen">
                <p class="total">Total <strong><?= number_format($total, 2, ',', '.') ?> €</strong></p>
                <form action="realizar-pedido.php" method="post">
                    <button class="boton" type="submit">Realizar pedido</button>
                </form>
            </div>
        <?php else: ?>
            <div class="carrito-vacio">
                <p>Tu carrito está vacío.</p>
                <a class="boton" href="categorias.php">Ver la carta</a>
            </div>
        <?php endif; ?>
    </main>
</body>
</html>
