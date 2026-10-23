<?php
// Transacción que SÍ se completa: dos usuarios con nombres distintos.
// Se pueden cambiar los nombres en la URL: transaccion_ok.php?nombre1=Marta&nombre2=Sergio
$cadena_conexion = 'mysql:dbname=empresa;host=127.0.0.1';
$usuario = 'root';
$clave = '';

$nombre1 = $_GET['nombre1'] ?? 'Marta';
$nombre2 = $_GET['nombre2'] ?? 'Sergio';

try {
    $bd = new PDO($cadena_conexion, $usuario, $clave);
    echo "Conexión realizada con éxito<br>";

    // comenzar la transacción
    $bd->beginTransaction();

    $ins = $bd->prepare("insert into usuarios (nombre, clave, rol) values (?, '33333', 1)");
    $ins->execute([$nombre1]);
    echo "Insertado " . htmlspecialchars($nombre1) . "<br>";
    $ins->execute([$nombre2]);
    echo "Insertado " . htmlspecialchars($nombre2) . "<br>";

    // las dos inserciones han ido bien: se guardan
    $bd->commit();
    echo "Transacción confirmada<br>";
} catch (PDOException $e) {
    if (isset($bd) && $bd->inTransaction()) {
        echo "Error: " . $e->getMessage();
        $bd->rollBack();
        echo "<br>Transacción anulada<br>";
    } else {
        echo 'Error al conectar: ' . $e->getMessage();
    }
}

// mostrar cómo queda la tabla
if (isset($bd)) {
    echo "<br>Usuarios en la tabla:<br>";
    foreach ($bd->query("select nombre from usuarios order by codigo") as $fila) {
        echo "- " . htmlspecialchars($fila['nombre']) . "<br>";
    }
}
