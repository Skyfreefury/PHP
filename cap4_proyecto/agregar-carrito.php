<?php
    require_once __DIR__ . "/clases/Sesion.php";
    require_once __DIR__ . "/clases/Carrito.php";
    Sesion::comprobar();
    if (!isset($_POST['id']) || !isset($_POST['unidades'])) {
        header('Location: productos.php?categoria=' . (int) ($_POST['categoria'] ?? 0));
        exit();
    }
    $idProducto = (int) $_POST['id'];
    $unidades = (int) $_POST['unidades'];
    $categoria = (int) $_POST['categoria'];
    Carrito::agregar($idProducto, $unidades);
    header('Location: productos.php?categoria=' . $categoria);
    exit();
