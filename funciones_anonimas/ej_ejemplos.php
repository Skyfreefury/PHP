<!-- //Escribir 5 DNI, crear un array y meterlos y buscar un DNI X en ese array -->

<!-- Probar foreach, modificar -->

<!-- Ejercicio variables.php -->

<!-- actividad 2.3 del libro -->
<?php
//Crear funcion anonima y guardarla en una variable
$castellano = function($text){
    return "Hola, " . $text;
};

$ingles = function($text){
    return "Hello, " . $text;
};
$italiano = function($text){
    return "Ciao, " . $text;
};

//Crear la funcion principal que recibe otra funcion como parametro
function ejecutarProceso($callback){
    return $callback("Chris");
};

//Pasar la funcion anonima como argumento
echo ejecutarProceso($castellano) . "<br>";
echo ejecutarProceso($ingles) . "<br>";
echo ejecutarProceso($italiano) . "<br>";
echo ejecutarProceso(function($text){
    return "Hola, " . $text;
}) . "<br>";

function potencia($base, $exponente = 2){
    $resultado = 1;
    for($i = 0; $i<$exponente; $i++){
        $resultado = $resultado*$base;
    }
    return $resultado;
}

echo potencia(5) . "<br>";
echo potencia(2, 4) . "<br>";
echo potencia(7, 0) . "<br>";
?>