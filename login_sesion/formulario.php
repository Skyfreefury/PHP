<?php
    
?>
<h1>Formulario</h1>
<form action="inicio.php" method="POST">
    <label for="usuario">Nombre de Usuario</label>
    <input type="text" name="usuario" id="usuario" placeholder="Vicky99">
    <input type="password" name="password" id="password" placeholder="****">
    <input type="submit" value="Enviar">
</form>

<?php
    include('footer.php');
?>
