<?php
	session_start();
	if(!isset($_SESSION['usuario']) || $_SESSION['rol'] != 1){
		header("Location: ej2_login.php?redirigido=true");
		exit;
	}
?>
<!DOCTYPE html>
<html>
	<head>
		<title>Zona Admin</title>
		<meta charset = "UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="estilos.css">
	</head>
	<body>
		<main class="tarjeta">
			<h1>Zona Admin</h1>
			<p class="subtitulo">Bienvenido, <?php echo $_SESSION['usuario']; ?></p>
			<div class="acciones">
				<a class="boton" href="ej2_principal.php">Volver a Principal</a>
			</div>
		</main>
	</body>
</html>