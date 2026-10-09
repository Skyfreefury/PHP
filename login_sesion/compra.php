<?php
    session_start();
    echo "Segundos transcurridos: " . (time() - $_SESSION['hora_inicio']) . "<br>";

    if (!isset($_SESSION['usuario'])) {
        // caso 1: nunca inició sesión
        header('Location: formulario.php');
        exit;
    } elseif (time() - $_SESSION['hora_inicio'] > 60) {
        // caso 2: han pasado mas de 60s, se cierra la sesion
        $_SESSION = array();
        session_destroy();
        header('Location: formulario.php');
        exit;
    }

?>

<h2>Compra confirmada</h2>
<p>Gracias por tu compra, <?php echo htmlspecialchars($_SESSION['usuario']); ?>.</p>

<?php
    include('footer.php');
?>
