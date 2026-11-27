<?php
    require_once __DIR__ . "/clases/Sesion.php";
    require_once __DIR__ . "/clases/Pedido.php";
    Sesion::comprobar();
    if ($_SERVER['REQUEST_METHOD'] !== 'POST' || empty($_SESSION['carrito'])) {
        header('Location: carrito.php');
        exit();
    }
    $idPedido = Pedido::crear($_SESSION['id_cliente'], $_SESSION['carrito']);
    if ($idPedido === null) {
        header('Location: carrito.php?error=1');
        exit();
    }
    $_SESSION['carrito'] = [];
    header('Location: confirmacion.php?pedido=' . $idPedido);
    exit();