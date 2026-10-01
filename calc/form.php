<?php
    include('header.php');

?>
<legend>Calculadora de ejercicios de 2do grado
    <form action="calcular.php" method="post">
        <label for="num1">Numero a:</label>
        <input type="text" id="num1" name="num1"><br><br>
        <label for="num2">Numero b:</label>
        <input type="text" id="num2" name="num2"><br><br>
        <label for="num3">Numero c:</label>
        <input type="text" id="num3" name="num3"><br><br>
        <input type="submit" value="Enviar">
    </form>
</legend>