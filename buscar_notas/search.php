<?php
    include('header.php');
    
    $limite = $_GET['nota'] ?? '';
    // function buscarNotas($array1, $limite) {
    //     $resultados = array();
    //     foreach ($array1 as $nombre => $nota) {
    //         if ($nota <= $limite) {
    //             $resultados[$nombre] = $nota;
    //         }
    //     }
    //     return $resultados;
    // }
    function buscarNotas(string $nombreFichero, float $limite): array {
        $fichero_lineas = file($nombreFichero, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        $resultados = array();
        foreach ($fichero_lineas as $linea) {
            list($nombre, $nota) = explode(',', $linea);
            $nota = (float)$nota;
            if ($nota <= $limite) {
                $resultados[] = $nombre . "=>" . $nota;
            }
        }
        return $resultados;
    }
    foreach (buscarNotas('notas.txt', (float)$limite) as $resultado) {
        echo $resultado . "<br>";
    }
?>

