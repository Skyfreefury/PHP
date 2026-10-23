<?php
    // Archivo compartido: cualquier script del CRUD hace require('conexion_mongo.php')
    // y recibe $usuarios, la colección libroservidor.usuarios ya lista.
    require __DIR__ . '/../../../vendor/autoload.php';

    try {
        $cliente = new MongoDB\Client('mongodb://localhost:27017/?directConnection=true');
        $usuarios = $cliente->libroservidor->usuarios;

        // Igual que el UNIQUE de MySQL: no puede haber dos usuarios con el mismo nombre
        $usuarios->createIndex(['nombre' => 1], ['unique' => true]);
    } catch (MongoDB\Driver\Exception\Exception $e) {
        echo "Error de conexión con MongoDB: " . htmlspecialchars($e->getMessage());
        exit;
    }
