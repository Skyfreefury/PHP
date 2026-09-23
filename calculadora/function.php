<?php
    function valMax($array){
        $max = $array[0];
        foreach($array as $valor){
            if($valor > $max){
                $max = $valor;
            }
        }
        return $max;
    }
    function valMin($array){
        $min = $array[0];
        foreach($array as $valor){
            if($valor < $min){
                $min = $valor;
            }
        }
        return $min;
    }
    function valMedia($array){
        $suma = 0;
        foreach($array as $valor){
            $suma += $valor;
        }
        return $suma / count($array);
    }
    function valSuma($array){
        $suma = 0;
        foreach($array as $valor){
            $suma += $valor;
        }
        return $suma;
    }
    function validar($array){
        $validar = true;
        foreach($array as $valor){
            if(!is_numeric($valor)){
                throw new Exception("El valor $valor no es un número válido.");
            }
        }
        return $validar;
    }
?>