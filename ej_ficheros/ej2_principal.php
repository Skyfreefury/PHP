<?php
	session_start();
	if(!isset($_SESSION['usuario'])){
		header("Location: ej2_login.php?redirigido=true");
		exit;
	}
?>
<!DOCTYPE html>
<html>
	<head>
		<title>Página principal</title>
		<meta charset = "UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="estilos.css">
	</head>
	<body>
		<main class="tarjeta">
			<h1><?php echo "Bienvenido ".$_SESSION['usuario'];?></h1>
			<p class="subtitulo">Página principal</p>
			<div class="acciones">
				<?php
					if($_SESSION['rol'] == 1){
						echo "<a class='boton boton-admin' href='ej2_admin.php'>Zona Admin</a>";
					}
				?>
				<a class="boton boton-secundario" href="ej2_logout.php">Salir</a>
			</div>
		</main>
	</body>
</html>