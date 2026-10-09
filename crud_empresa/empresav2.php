<?php
    require('conexion.php');

    //consulta preparada
    $sql1 = 'select nombre from usuarioss where rol = ? and nombre = ?';
    $preparada = $bd->prepare($sql1);
    $rol = 1;
    $nombre = 'ana';
    $preparada->execute(array($rol, $nombre));
    echo 'Usuarios con rol ' . $rol . ' y nombre "' . $nombre . '": ' . $preparada->rowCount() . '<br>';
    foreach($preparada as $usu){
        print "Nombre: " . $usu['nombre'] . "<br>";
    }

?>
