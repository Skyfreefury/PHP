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
    <title>Arrivederci · Entrar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body class="pagina-login">
    <div class="lema">
        <a class="marca" href="index.php">Arrivederci</a>
        <div>
            <h1>Recién salida<br>del horno.</h1>
            <p>Pizzas, bebidas y complementos. Pide en dos pasos.</p>
        </div>
    </div>

    <div class="tarjeta-login">
        <h2>Entrar</h2>
        <p class="subtitulo">Usa el correo y la clave de tu cuenta.</p>
        <?php if (isset($_GET['redirigido'])): ?>
            <p class="aviso">Haga login para continuar.</p>
        <?php endif; ?>
        <?php if (isset($error)): ?>
            <p class="aviso aviso-error">Revise usuario y contraseña.</p>
        <?php endif; ?>
        <form action="login.php" method="post">
            <label for="correo">Correo electrónico</label>
            <input type="email" id="correo" name="correo" value="<?= htmlspecialchars($valorCorreo) ?>" required>
            <label for="clave">Clave</label>
            <input type="password" id="clave" name="clave" required>
            <input class="boton" type="submit" value="Entrar">
        </form>
    </div>
</body>
</html>