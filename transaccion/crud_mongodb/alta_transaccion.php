<?php
    // TRANSACCIÓN: alta de dos usuarios a la vez. O se guardan los dos o ninguno.
    // Lo procesa acciones.php (caso 'insertar_transaccion').
    $titulo = 'Alta en transacción';
    $activa = 'transaccion';
    require('cabecera.php');
?>
        <p class="explicacion">
            Se insertan dos usuarios dentro de la misma transacción. Si el segundo falla
            (por ejemplo, porque ese nombre ya existe), se deshace también el primero.
        </p>

        <form action="acciones.php" method="post">
            <div class="grupo campos">
                <label class="campo">
                    <span>Usuario 1</span>
                    <input type="text" name="nombre1" placeholder="Nombre" required autofocus>
                </label>
                <label class="campo">
                    <span>Usuario 2</span>
                    <input type="text" name="nombre2" placeholder="Nombre" required>
                </label>
                <label class="campo">
                    <span>Clave</span>
                    <input type="text" name="clave" placeholder="Para los dos" required>
                </label>
            </div>
            <p class="nota-seccion">Prueba a poner en «Usuario 2» un nombre que ya exista para ver cómo se anula.</p>

            <button type="submit" name="accion" value="insertar_transaccion" class="boton boton-ancho">Insertar los dos</button>
        </form>
<?php require('pie.php'); ?>
