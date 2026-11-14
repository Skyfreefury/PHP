<?php
// Conexión única a la base "arrivederci".
// Uso desde cualquier página o clase: $bd = BD::conectar();
class BD {
    private const CADENA  = 'mysql:dbname=arrivederci;host=127.0.0.1;port=3307;charset=utf8mb4';
    private const USUARIO = 'root';
    private const CLAVE   = 'root';

    // Guarda el PDO para reutilizarlo: una sola conexión por petición
    private static ?PDO $conexion = null;

    public static function conectar(): PDO {
        if (self::$conexion === null) {
            try {
                self::$conexion = new PDO(self::CADENA, self::USUARIO, self::CLAVE, [
                    // Lanza excepciones en los errores: lo necesita la transacción del pedido (RNF-05)
                    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                    // Cada fila llega como array con los nombres de las columnas
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                ]);
            } catch (PDOException $e) {
                // El detalle técnico no se enseña al usuario
                error_log('Error de conexión: ' . $e->getMessage());
                exit('No se puede conectar con la base de datos. Inténtelo más tarde.');
            }
        }
        return self::$conexion;
    }
}
