<?php
require_once __DIR__ . "/BD.php";
class Producto {
    private $id;
    private $nombre;
    private $descripcion;
    private $precio;
    private $stock;

    public function __construct($id, $nombre, $descripcion, $precio, $stock) {
        $this->id = $id;
        $this->nombre = $nombre;
        $this->descripcion = $descripcion;
        $this->precio = $precio;
        $this->stock = $stock;
    }

    // Getters
    public function getId() {
        return $this->id;
    }

    public function getNombre() {
        return $this->nombre;
    }

    public function getDescripcion() {
        return $this->descripcion;
    }

    public function getPrecio() {
        return $this->precio;
    }

    public function getStock() {
        return $this->stock;
    }
    public static function porCategoria($idCategoria) {
        $productos = [];
        $bd = BD::conectar();
        $stmt = $bd->prepare("SELECT * FROM producto WHERE ID_Categoria = :id");
        $stmt->execute(['id' => $idCategoria]);
        foreach($stmt as $fila){
            $productos[] = new Producto($fila["ID_Producto"], $fila["Nombre"], $fila["Descripcion"], $fila["Precio"], $fila["Stock"]);
        }
        return $productos;
    }
    public static function porId($idProducto) {
        $bd = BD::conectar();
        $stmt = $bd->prepare("SELECT * FROM producto WHERE ID_Producto = :id");
        $stmt->execute(['id' => $idProducto]);
        $fila = $stmt->fetch();
        if ($fila) {
            return new Producto($fila["ID_Producto"], $fila["Nombre"], $fila["Descripcion"], $fila["Precio"], $fila["Stock"]);
        }
        return null;
    }
}
?>