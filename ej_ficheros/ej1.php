<?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['color'])) {
        $_COOKIE['color'] = $_POST['color'];
        setcookie('color', $_POST['color'], time() + 3600); // Guardar la cookie durante 1 hora
    }
    $color = isset($_COOKIE['color']) ? $_COOKIE['color'] : '#ffffff'; // Color por defecto si no hay cookie
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejercicio 1</title>
    <link rel="stylesheet" href="estilos.css">
    <!-- Solo el color de fondo va aquí, porque sale de la cookie (PHP) -->
    <style>
        body { background-color: <?php echo htmlspecialchars($color); ?>; }
    </style>
</head>
<body>
    <main class="tarjeta">
        <h1>Elige tu color de fondo</h1>
        <p class="subtitulo">Se guardará en una cookie y la próxima vez que entres la página aparecerá con ese color.</p>

        <form action="ej1.php" method="POST">
            <label for="color">Color:</label>
            <input type="color" id="color" name="color" value="<?php echo htmlspecialchars($color); ?>">
            <input type="submit" value="Guardar">
        </form>

        <p class="actual">Color actual: <code><?php echo htmlspecialchars($color); ?></code></p>
    </main>
</body>
</html>