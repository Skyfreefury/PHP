<?php
class Carrito {
    private const MAX_UNIDADES = 10;

    public static function agregar($idProducto, $unidades) {
        // Primero se valida: si no está entre 1 y 10, no se guarda nada.
        if ($unidades < 1 || $unidades > self::MAX_UNIDADES) {
            return;
        }
        $actuales = $_SESSION['carrito'][$idProducto] ?? 0;
        // Se suma a lo que ya había, con un tope de 10.
        $_SESSION['carrito'][$idProducto] = min($actuales + $unidades, self::MAX_UNIDADES);
    }
}
