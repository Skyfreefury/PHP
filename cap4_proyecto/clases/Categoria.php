<?php
    require_once __DIR__ . "/BD.php";
    class Categoria {
        private $id;
        private $nombre;
        private $descripcion;

        public function __construct($id, $nombre, $descripcion) {
            $this->id = $id;
            $this->nombre = $nombre;
            $this->descripcion = $descripcion;
        }

        public function getDescripcion() {
            return $this->descripcion;
        }

        public function getId() {
            return $this->id;
        }

        public function getNombre() {
            return $this->nombre;
        }
        public static function todas(){
            $categorias = [];
            $bd = BD::conectar();
            $resultado = $bd->query("SELECT * FROM categoria");
            foreach($resultado as $fila){
                $categorias[] = new Categoria($fila["ID_Categoria"], $fila["Nombre"], $fila["Descripcion"]);
            }
            return $categorias;
        }
    }

?>