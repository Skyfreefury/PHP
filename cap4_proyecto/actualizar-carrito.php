<?php
    require_once __DIR__ . "/clases/Sesion.php";
    require_once __DIR__ . "/clases/Carrito.php";
    Sesion::comprobar();
    if (!isset($_POST['id']) || !isset($_POST['accion'])) {
        header('Location: carrito.php');
        exit();
    }
    $idProducto = (int) $_POST['id'];
    if ($_POST['accion'] === 'eliminar') {
        Carrito::eliminar($idProducto);
    } else {
        Carrito::cambiar($idProducto, (int) ($_POST['unidades'] ?? 0));
    }
    header('Location: carrito.php');
    exit();