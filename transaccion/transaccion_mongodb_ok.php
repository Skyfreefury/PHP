<?php
// Transacción con MongoDB que SÍ se completa: dos usuarios con nombres distintos.
// Se pueden cambiar los nombres en la URL: transaccion_mongodb_ok.php?nombre1=Marta&nombre2=Sergio
require __DIR__ . '/../../vendor/autoload.php';

$nombre1 = $_GET['nombre1'] ?? 'Marta';
$nombre2 = $_GET['nombre2'] ?? 'Sergio';

try {
    $cliente = new MongoDB\Client("mongodb://localhost:27017/?directConnection=true");
    $usuarios = $cliente->libroservidor->usuarios;
    echo "Conexión realizada con éxito<br>";

    // no puede haber dos usuarios con el mismo nombre
    $usuarios->createIndex(['nombre' => 1], ['unique' => true]);

    // comenzar la transacción
    $sesion = $cliente->startSession();
    $sesion->startTransaction();

    try {
        $usuarios->insertOne(['nombre' => $nombre1, 'clave' => '33333', 'rol' => 1], ['session' => $sesion]);
        echo "Insertado " . htmlspecialchars($nombre1) . "<br>";
        $usuarios->insertOne(['nombre' => $nombre2, 'clave' => '33333', 'rol' => 1], ['session' => $sesion]);
        echo "Insertado " . htmlspecialchars($nombre2) . "<br>";

        // las dos inserciones han ido bien: se guardan
        $sesion->commitTransaction();
        echo "Transacción confirmada<br>";
    } catch (MongoDB\Driver\Exception\Exception $e) {
        echo "Error: " . $e->getMessage();
        $sesion->abortTransaction();
        echo "<br>Transacción anulada<br>";
    }

    // mostrar cómo queda la colección
    echo "<br>Usuarios en la colección:<br>";
    foreach ($usuarios->find() as $u) {
        echo "- " . htmlspecialchars($u['nombre']) . "<br>";
    }
} catch (MongoDB\Driver\Exception\Exception $e) {
    echo 'Error con MongoDB: ' . $e->getMessage();
}
