<?php
    // Parte de arriba común a todas las páginas del CRUD.
    // Antes de hacer require('cabecera.php') cada página define:
    //   $titulo -> título grande de la página
    //   $activa -> qué pestaña del menú se marca ('listado', 'crear' o 'transaccion')

    // Mensaje que deja acciones.php al volver ('ok' en verde, 'error' en rojo)
    $mensaje = $_GET['mensaje'] ?? '';
    $tipo = ($_GET['tipo'] ?? 'ok') === 'error' ? 'error' : 'ok';

    $paginas = [
        'listado'     => ['index.php', 'Usuarios'],
        'crear'       => ['crear.php', 'Nuevo'],
        'transaccion' => ['alta_transaccion.php', 'Transacción'],
    ];
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo htmlspecialchars($titulo); ?> · CRUD MongoDB</title>
    <link rel="stylesheet" href="estilo.css?v=3">
</head>
<body>
    <main class="pagina">
        <p class="subtitulo">MongoDB · libroservidor.usuarios</p>
        <h1 class="titulo-grande"><?php echo htmlspecialchars($titulo); ?></h1>

        <!-- Menú: control segmentado con las tres páginas -->
        <nav class="segmentos">
            <?php foreach ($paginas as $clave => [$enlace, $texto]): ?>
                <a href="<?php echo $enlace; ?>" class="<?php echo $clave === ($activa ?? '') ? 'activo' : ''; ?>">
                    <?php echo $texto; ?>
                </a>
            <?php endforeach; ?>
        </nav>

        <?php if ($mensaje !== ''): ?>
            <div class="aviso aviso-<?php echo $tipo; ?>"><?php echo htmlspecialchars($mensaje); ?></div>
        <?php endif; ?>
