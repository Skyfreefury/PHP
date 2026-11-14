<?php
/* Formulario de login habitual:
	si va bien abre sesión, guarda el nombre de usuario y redirige a principal.php
	si va mal, mensaje de error */
function comprobar_usuario($nombre, $clave) {
    if ($nombre === "usuario" and $clave === "1234") {
        $usu['nombre'] = "usuario";
        $usu['rol'] = 0;
        return $usu;
    } elseif ($nombre === "admin" and $clave === "1234") {
        $usu['nombre'] = "admin";
        $usu['rol'] = 1;
        return $usu;
    } else {
        return false;
    }
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $usu = comprobar_usuario($_POST['usuario'], $_POST['clave']);
    if ($usu == false) {
        $err = true;
        $usuario = $_POST['usuario'];
    } else {
        session_start();
        $_SESSION['usuario'] = $_POST['usuario'];
		$_SESSION['rol'] = $usu['rol'];
        header("Location: ej2_principal.php");
		exit;
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Formulario de login</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="estilos.css">
</head>
<body>
    <main class="tarjeta">
        <h1>Iniciar sesión</h1>
        <p class="subtitulo">Introduce tu usuario y contraseña</p>

        <?php if (isset($_GET["redirigido"])) {
            echo "<p class='aviso'>Haga login para continuar</p>";
        } ?>
        <?php if (isset($err) and $err == true) {
            echo "<p class='aviso'>Revise usuario y contraseña</p>";
        } ?>

        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="POST">
            <div class="campo">
                <label for="usuario">Usuario</label>
                <input value="<?php if (isset($usuario)) echo $usuario; ?>" id="usuario" name="usuario" type="text">
            </div>
            <div class="campo">
                <label for="clave">Clave</label>
                <input id="clave" name="clave" type="password">
            </div>
            <input type="submit" value="Entrar">
        </form>
    </main>
</body>
</html>
