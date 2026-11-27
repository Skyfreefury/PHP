<?php
    require_once __DIR__ . "/clases/Sesion.php";
    require_once __DIR__ . "/clases/Pedido.php";
    Sesion::comprobar();
    $pedidos = Pedido::delCliente($_SESSION['id_cliente']);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arrivederci · Mis pedidos</title>
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
        <p class="antetitulo"><?= count($pedidos) ?> pedidos</p>
        <h1>Mis pedidos</h1>
        <?php if (empty($pedidos)): ?>
            <div class="carrito-vacio">
                <p>Todavía no has hecho ningún pedido.</p>
                <a class="boton" href="categorias.php">Ver la carta</a>
            </div>
        <?php else: ?>
            <ul class="lista-pedidos">
                <?php foreach ($pedidos as $pedido): ?>
                    <li class="linea-pedido">
                        <span class="numero">Pedido nº <?= (int) $pedido['ID_Pedido'] ?></span>
                        <span class="fecha"><?= date('d/m/Y H:i', strtotime($pedido['Fecha'])) ?></span>
                        <span class="articulos"><?= (int) $pedido['Unidades'] ?> <?= $pedido['Unidades'] == 1 ? 'artículo' : 'artículos' ?></span>
                        <span class="importe"><?= number_format($pedido['Total'], 2, ',', '.') ?> €</span>
                        <?php if ($pedido['Enviado']): ?>
                            <span class="estado enviado">Enviado</span>
                        <?php else: ?>
                            <span class="estado">En preparación</span>
                        <?php endif; ?>
                    </li>
                <?php endforeach; ?>
            </ul>
        <?php endif; ?>
    </main>
</body>
</html>
