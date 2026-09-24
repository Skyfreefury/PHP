<?php
    require("function.php");
    
?>
<?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $numeros = [$_POST['uno'], $_POST['dos'], $_POST['tres'], $_POST['cuatro'], $_POST['cinco']];
        try{
            validar($numeros);
        }
        catch(Exception $e){
            $campo = 1;
            foreach($numeros as $valor){
                if(!is_numeric($valor)){
                    $campo = $i +1;
                    break;
                }
                
            }
            header("Location: calculadora.php?error=1&" . http_build_query($_POST));
            exit;
        }
        
        require("header.php");
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