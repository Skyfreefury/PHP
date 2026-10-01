<?php
    $num1 = $_POST['num1'];
    $num2 = $_POST['num2'];
    $num3 = $_POST['num3'];
    $array1 = array($num1, $num2, $num3);

    function resolverEcuacion($array1) {
        $num1 = $array1[0];
        $num2 = $array1[1];
        $num3 = $array1[2];
        if ($num1 == 0) {
            throw new Exception("El coeficiente a no puede ser cero.");
        }
        $discriminante = pow($num2, 2) - 4 * $num1 * $num3;
        if ($discriminante < 0) {
            throw new Exception("La ecuación no tiene soluciones reales.");

        }
        elseif ($discriminante == 0) {
            $x = -$num2 / (2 * $num1);
            return [$x];
        }
        else {
            $x1 = (-$num2 + sqrt($discriminante)) / (2 * $num1);
            $x2 = (-$num2 - sqrt($discriminante)) / (2 * $num1);
            return [$x1, $x2];
        }
    }
    try {
        $soluciones = resolverEcuacion($array1);
        if (count($soluciones) == 1) {
            echo "La ecuación tiene una solución doble: x = " . $soluciones[0];
        } else {
            echo "Las soluciones son: x1 = " . $soluciones[0] . ", x2 = " . $soluciones[1];
        }
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage();
    }
?>
