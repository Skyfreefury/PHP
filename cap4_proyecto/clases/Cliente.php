<?php
require_once __DIR__ . '/BD.php';
class Cliente {
    private $id;
    private $nombre;
    private $correo;
    private $direccion;

    public function __construct($id, $nombre, $correo, $direccion) {
        $this->id = $id;
        $this->nombre = $nombre;
        $this->correo = $correo;
        $this->direccion = $direccion;
    }

    public function getId() {
        return $this->id;
    }

    public function getNombre() {
        return $this->nombre;
    }

    public function getCorreo() {
        return $this->correo;
    }

    public function getDireccion() {
        return $this->direccion;
        }
    public static function comprobar($correo, $clave) {
            $bd = BD::conectar();
            $stmt = $bd->prepare('SELECT * FROM cliente WHERE correo = :correo');
            $stmt->execute(['correo' => $correo]);
            $fila = $stmt->fetch();
            if ($fila && password_verify($clave, $fila['Clave'])) {
                return new Cliente($fila['ID_Cliente'], $fila['Nombre'], $fila['Correo'], $fila['Direccion']);
            }
            return null;
        }
}
