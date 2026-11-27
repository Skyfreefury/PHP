<?php
    require_once __DIR__ . "/clases/Sesion.php";
    Sesion::comprobar();
    $idPedido = (int) ($_GET['pedido'] ?? 0);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arrivederci · Pedido confirmado</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
    <header class="cabecera">
        <a class="marca" href="categorias.php">Arrivederci</a>
        <nav>
            <a href="historial.php">Mis pedidos</a>
            <a href="logout.php">Cerrar sesión</a>
        </nav>
    </header>

    <main class="contenido confirmacion">
        <p class="antetitulo">Pedido nº <?= $idPedido ?></p>
        <h1>¡Pedido recibido!</h1>
        <p>Ya está en el horno. Te llegará a tu dirección en unos 30 minutos.</p>
        <a class="boton" href="categorias.php">Volver a la carta</a>
    </main>
</body>
</html>