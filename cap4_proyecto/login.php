<?php
// Conexión única a la base "arrivederci".
session_start();

require_once __DIR__ . '/clases/BD.php';
require_once __DIR__ . '/clases/Cliente.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $correo = $_POST['correo'];
            $clave = $_POST['clave'];
            $cliente = Cliente::comprobar($correo, $clave);
            if ($cliente) {
                $_SESSION['id_cliente'] = $cliente->getId();
                $_SESSION['nombre'] = $cliente->getNombre();
                $_SESSION['carrito'] = [];
                $_SESSION['ultima_actividad'] = time();
                setcookie('correo', $correo, time() + 30 * 24 * 3600, '/');
                header('Location: categorias.php');
                exit();
            } else {
                $error = true;
            }
        }
        $valorCorreo = $correo ?? $_COOKIE['correo'] ?? '';
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arrivederci</title>
</head>
<body>
    <h1>Arrivederci</h1>
    <?php if (isset($_GET['redirigido'])): ?>
        <p>Haga login para continuar.</p>
    <?php endif; ?>
    <?php if (isset($error)): ?>
        <p>Revise usuario y contraseña.</p>
    <?php endif; ?>
    <form action="login.php" method="post">
        <label for="correo">Correo:</label>
        <input type="email" id="correo" name="correo" value="<?= htmlspecialchars($valorCorreo) ?>" required>
        <br>
        <label for="clave">Clave:</label>
        <input type="password" id="clave" name="clave" required>
        <br>
        <input type="submit" value="Iniciar sesión">
    </form>
</body>
</html>