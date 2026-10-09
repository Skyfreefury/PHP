<?php
    include('header.php');

?>

<form action="search.php" method="get">
    <label for="nota">Buscar:</label>
    <input type="text" name="nota" id="nota" style="width: 220px;" placeholder="Ingrese el limite de nota a buscar">
    <button type="submit">Buscar</button>
</form>