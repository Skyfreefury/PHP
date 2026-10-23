<?php
    // CREATE: formulario para dar de alta un usuario. Lo procesa acciones.php.
    $titulo = 'Nuevo usuario';
    $activa = 'crear';
    require('cabecera.php');
?>
        <form action="acciones.php" method="post">
            <div class="grupo campos">
                <label class="campo">
                    <span>Nombre</span>
                    <input type="text" name="nombre" placeholder="Obligatorio" required autofocus>
                </label>
                <label class="campo">
                    <span>Clave</span>
                    <input type="text" name="clave" placeholder="Obligatorio" required>
                </label>
                <label class="campo">
                    <span>Rol</span>
                    <input type="number" id="rol" name="rol" value="0" min="0" required>
                    <!-- Stepper: − baja y + sube el número del campo rol -->
                    <span class="stepper">
                        <button type="button" aria-label="Bajar rol" onclick="document.getElementById('rol').stepDown()">−</button>
                        <button type="button" aria-label="Subir rol" onclick="document.getElementById('rol').stepUp()">+</button>
                    </span>
                </label>
            </div>
            <p class="nota-seccion">El nombre no se puede repetir.</p>

            <button type="submit" name="accion" value="insertar" class="boton boton-ancho">Guardar usuario</button>
        </form>
<?php require('pie.php'); ?>
