<?php
    // READ: listado de usuarios con botones de Editar y Borrar en cada fila.
    require('conexion_mongo.php');

    // find() devuelve todos los documentos; se ordenan por nombre
    $lista = $usuarios->find([], ['sort' => ['nombre' => 1]])->toArray();

    $titulo = 'Usuarios';
    $activa = 'listado';
    require('cabecera.php');
?>
        <p class="nota-seccion"><?php echo count($lista); ?> usuario<?php echo count($lista) === 1 ? '' : 's'; ?></p>

        <?php if (empty($lista)): ?>
            <div class="grupo vacio">
                <p>No hay usuarios todavía.</p>
                <a class="boton" href="crear.php">Añadir usuario</a>
            </div>
        <?php else: ?>
            <ul class="grupo lista">
                <?php foreach ($lista as $usu): ?>
                    <li class="fila">
                        <div class="fila-texto">
                            <span class="fila-titulo"><?php echo htmlspecialchars($usu['nombre'] ?? ''); ?></span>
                            <span class="fila-detalle">
                                Clave <?php echo htmlspecialchars($usu['clave'] ?? ''); ?> · Rol <?php echo htmlspecialchars($usu['rol'] ?? 0); ?>
                            </span>
                        </div>
                        <div class="fila-acciones">
                            <!-- UPDATE: lleva el _id del documento a editar.php -->
                            <a class="boton-texto" href="editar.php?id=<?php echo urlencode((string) $usu['_id']); ?>">Editar</a>

                            <!-- DELETE: manda el _id de ESTE documento a acciones.php -->
                            <form action="acciones.php" method="post"
                                  onsubmit="return confirm('¿Borrar a <?php echo htmlspecialchars(addslashes($usu['nombre'] ?? ''), ENT_QUOTES); ?>?');">
                                <input type="hidden" name="id" value="<?php echo htmlspecialchars((string) $usu['_id']); ?>">
                                <button type="submit" name="accion" value="borrar" class="boton-texto peligro">Borrar</button>
                            </form>
                        </div>
                    </li>
                <?php endforeach; ?>
            </ul>
        <?php endif; ?>
<?php require('pie.php'); ?>
