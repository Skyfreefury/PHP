<?php
    require("function.php");
    require("header.php");
?>
<?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $numeros = [$_POST['num1'], $_POST['num2'], $_POST['num3'], $_POST['num4'], $_POST['num5']];
        try{
        validar($numeros);
        }
        catch(Exception $e){
            echo "<p style='color:red;'>Error: " . $e->getMessage() . "</p>";
            exit;
        }
        switch ($_POST['action']) {
            case 'enviar':
                echo "<p>Los números introducidos son: " . implode(", ", $numeros) . "</p>";
                break;
            case 'sumar':
                $resultado = valSuma($numeros);
                echo "<p>La suma de los números es: $resultado</p>";
                break;
            case 'maximo':
                $resultado = valMax($numeros);
                echo "<p>El valor máximo es: $resultado</p>";
                break;
            case 'minimo':
                $resultado = valMin($numeros);
                echo "<p>El valor mínimo es: $resultado</p>";
                break;
            case 'medio':
                $resultado = valMedia($numeros);
                echo "<p>El valor medio es: $resultado</p>";
                break;
            default:
                echo "<p>Acción no válida.</p>";
        }
    }

    require("footer.php");
?>