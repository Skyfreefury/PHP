<?php
// Misma transacción que transaccion.php, pero con MongoDB.
// Requisito: MongoDB tiene que funcionar como replica set (aunque sea de un solo nodo).
require __DIR__ . '/../../vendor/autoload.php';

try {
    $cliente = new MongoDB\Client("mongodb://localhost:27017/?directConnection=true");
    $usuarios = $cliente->libroservidor->usuarios;
    echo "Conexión realizada con éxito<br>";

    // Equivale al UNIQUE de MySQL: no puede haber dos usuarios con el mismo nombre
    $usuarios->createIndex(['nombre' => 1], ['unique' => true]);

    // comenzar la transacción
    $sesion = $cliente->startSession();
    $sesion->startTransaction();

    try {
        $doc = ['nombre' => 'Fernando', 'clave' => '33333', 'rol' => 1];
        $usuarios->insertOne($doc, ['session' => $sesion]);

        // se repite la inserción
        // falla porque el nombre es unique
        $usuarios->insertOne($doc, ['session' => $sesion]);

        // si hubiera ido bien
        $sesion->commitTransaction();
        echo "Transacción confirmada<br>";
    } catch (MongoDB\Driver\Exception\Exception $e) {
        echo "Error: " . $e->getMessage();
        // deshace el primer cambio
        $sesion->abortTransaction();
        echo "<br>Transacción anulada<br>";
    }
} catch (MongoDB\Driver\Exception\Exception $e) {
    echo 'Error con MongoDB: ' . $e->getMessage();
}

// comprobar que Fernando no se ha guardado
echo "Usuarios con nombre Fernando: " . $usuarios->countDocuments(['nombre' => 'Fernando']) . "<br>";
