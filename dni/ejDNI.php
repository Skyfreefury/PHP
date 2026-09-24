<?php
    
$array1 = [
    "12345678Z" => "Ana García",
    "87654321X" => "Luis Martínez",
    "11111111H" => "Marta López",
    "22222222J" => "Carlos Sánchez",
    "33333333P" => "Lucía Fernández",
];
?>

<form action="ejDNI.php" method="post">
        <label for="">Buscar por DNI</label>
        <input type="text" name="DNI" placeholder="DNI a buscar">
        <button type="submit">Buscar</button>
    </form>

<?php

    if(isset($_POST["DNI"])){
        $dni = $_POST["DNI"];
        if(array_key_exists($dni, $array1)){
            echo "El DNI pertenece a: " . $array1[$dni];
        }
        else{
            echo "No existe ese DNI";
        }
    }
?>