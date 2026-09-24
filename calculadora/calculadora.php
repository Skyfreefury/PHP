<?php
    require("function.php");
    require("header.php");
?>

    <form action="plantilla.php" method="post">
        <?php
            if(isset($_GET['error']) && $_GET['error'] == '1'){
                echo "<p style='color:red;'>Error: Por favor, introduce solo números válidos.</p>";
            }
        ?>
        <input type="text" name="uno" placeholder="Número 1" value="<?php if(isset($_GET['uno'])) {echo $_GET['uno'];} else{echo '0';} ?>">
        <?php
            if(isset($_GET['error']) && $_GET['error'] == '2'){
                echo "<p style='color:red;'>Error: Por favor, introduce solo números válidos.</p>";
            }
        ?>
        <input type="text" name="dos" placeholder="Número 2" value="<?php if(isset($_GET['dos'])) {echo $_GET['dos'];} else{echo '0';} ?>">
        <?php
            if(isset($_GET['error']) && $_GET['error'] == '3'){
                echo "<p style='color:red;'>Error: Por favor, introduce solo números válidos.</p>";
            }
        ?>
        <input type="text" name="tres" placeholder="Número 3" value="<?php if(isset($_GET['tres'])) {echo $_GET['tres'];} else{echo '0';} ?>">
        <?php
            if(isset($_GET['error']) && $_GET['error'] == '4'){
                echo "<p style='color:red;'>Error: Por favor, introduce solo números válidos.</p>";
            }
        ?>
        <input type="text" name="cuatro" placeholder="Número 4" value="<?php if(isset($_GET['cuatro'])) {echo $_GET['cuatro'];} else{echo '0';} ?>">
        <?php
            if(isset($_GET['error']) && $_GET['error'] == '5'){
                echo "<p style='color:red;'>Error: Por favor, introduce solo números válidos.</p>";
            }
        ?>
        <input type="text" name="cinco" placeholder="Número 5" value="<?php if(isset($_GET['cinco'])) {echo $_GET['cinco'];} else{echo '0';} ?>">
        <select name="action" id="">
            <option value="sumar">Sumar</option>
            <option value="maximo">Valor Máximo</option>
            <option value="minimo">Valor Mínimo</option>
            <option value="medio">Valor Medio</option>
        </select>
        <button type="submit" value="enviar">ENVIAR</button>
    </form>


<?php
    require("footer.php");
?>

