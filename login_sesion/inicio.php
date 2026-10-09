<?php
    session_start();
    $_SESSION['usuario'] = $_POST['usuario'];
    $_SESSION['hora_inicio'] = time();

    
?>
<div style="display: flex; justify-content: flex-start; align-items: center; gap: 12px;">
    <h2>Inicio</h2>
    <span><?php echo htmlspecialchars($_SESSION['usuario']); ?></span>
</div>

<form action="compra.php" method="post">
    <input type="submit" value="Comprar">
</form>

<?php
    include('footer.php');
?>
