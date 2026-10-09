<?php
    include('header.php');

    function mostrarArray(array $array) {
        foreach ($array as $clave => $valor) {
            echo $clave . " => " . $valor . "<br>";
        }
        echo "<br>";
    }

    $notas = [
        "Christian" => 10,
        "Jorge" => 7,
        "Martin" => 8,
        "Thomas" => 3,
    ];

    echo "Array original <br>";
    mostrarArray($notas);

    $copia1 = $notas;
    sort($copia1);
    echo "sort() - valores de menor a mayor, claves reindexadas <br>";
    mostrarArray($copia1);

    $copia2 = $notas;
    rsort($copia2);
    echo "rsort() - valores de mayor a menor, claves reindexadas <br>";
    mostrarArray($copia2);

    $copia3 = $notas;
    ksort($copia3);
    echo "ksort() - ordenado por clave, mantiene las claves <br>";
    mostrarArray($copia3);

    include('footer.php');
?>
