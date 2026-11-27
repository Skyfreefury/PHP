<?php
require_once __DIR__ . "/BD.php";
require_once __DIR__ . "/Producto.php";

class Pedido {

    // Guarda el pedido y sus líneas en una sola transacción (RF-10, RNF-05).
    // Devuelve el ID del pedido nuevo, o null si algo falla.
    public static function crear($idCliente, $carrito) {
        $bd = BD::conectar();
        try {
            $bd->beginTransaction();

            $stmt = $bd->prepare("INSERT INTO pedido (Fecha, Enviado, ID_Cliente) VALUES (NOW(), 0, :cliente)");
            $stmt->execute(['cliente' => $idCliente]);
            $idPedido = $bd->lastInsertId();

            $linea = $bd->prepare("INSERT INTO pedido_producto (ID_Pedido, ID_Producto, Unidades, Precio)
                                VALUES (:pedido, :producto, :unidades, :precio)");
            foreach ($carrito as $idProducto => $unidades) {
                // El precio se lee de la base de datos en este momento (RN-03).
                $producto = Producto::porId($idProducto);
                if (!$producto) {
                    throw new Exception("Producto $idProducto no existe");
                }
                $linea->execute([
                    'pedido'   => $idPedido,
                    'producto' => $idProducto,
                    'unidades' => $unidades,
                    'precio'   => $producto->getPrecio(),
                ]);
            }

            $bd->commit();
            return $idPedido;
        } catch (Exception $e) {
            // Si falla una línea, no se guarda nada del pedido.
            $bd->rollBack();
            error_log('Error al crear pedido: ' . $e->getMessage());
            return null;
        }
    }

    // Pedidos de un cliente, del más nuevo al más antiguo (RF-14).
    // Cada fila trae ID_Pedido, Fecha, Enviado, Unidades y Total.
    public static function delCliente($idCliente) {
        $bd = BD::conectar();
        $stmt = $bd->prepare("SELECT p.ID_Pedido, p.Fecha, p.Enviado,
                                     SUM(pp.Unidades) AS Unidades,
                                     SUM(pp.Unidades * pp.Precio) AS Total
                              FROM pedido p
                              JOIN pedido_producto pp ON pp.ID_Pedido = p.ID_Pedido
                              WHERE p.ID_Cliente = :cliente
                              GROUP BY p.ID_Pedido, p.Fecha, p.Enviado
                              ORDER BY p.Fecha DESC, p.ID_Pedido DESC");
        $stmt->execute(['cliente' => $idCliente]);
        return $stmt->fetchAll();
    }
}