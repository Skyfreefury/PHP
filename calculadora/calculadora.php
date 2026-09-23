<?php
    require("function.php");
    require("header.php");
?>

    <form action="plantilla.php" method="post">
        <input type="number" name="num1" placeholder="Número 1" value="0">
        <input type="number" name="num2" placeholder="Número 2" value="0">
        <input type="number" name="num3" placeholder="Número 3" value="0">
        <input type="number" name="num4" placeholder="Número 4" value="0">
        <input type="number" name="num5" placeholder="Número 5" value="0">
        <button type="submit" name="action" value="enviar">ENVIAR</button>
        <button type="submit" name="action" value="sumar">Sumar</button>
        <button type="submit" name="action" value="maximo">Valor Máximo</button>
        <button type="submit" name="action" value="minimo">Valor Mínimo</button>
        <button type="submit" name="action" value="medio">Valor Medio</button>
    </form>


<?php
    require("footer.php");
?>