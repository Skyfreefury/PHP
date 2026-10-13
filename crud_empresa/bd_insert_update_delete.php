<?php
    require('conexion.php');

    //insertar nuevo usuario
    $ins = 'insert into usuarios(nombre, clave,rol) values()';

    //actualizar usuario
    $updt = "update usuarios set rol = 0 where rol = 1";
    $result = $bd->query($updt)

    //borrar usuario
?>