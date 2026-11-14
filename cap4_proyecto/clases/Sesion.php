<?php
class Sesion {
    // Minutos sin actividad antes de cerrar la sesión (RF-13)
    private const MINUTOS = 15;
    public static function comprobar(): void {
        // 1. arrancar la sesión
        session_start();
        // 2. si no existe $_SESSION['id_cliente'] → al login con ?redirigido=1 y exit
        if (!isset($_SESSION['id_cliente'])) {
            header('Location: login.php?redirigido=1');
            exit();
        }
        // 3. si han pasado más de MINUTOS
        if (isset($_SESSION['ultima_actividad']) && (time() - $_SESSION['ultima_actividad'] > self::MINUTOS * 60)) {
            session_unset();
            session_destroy();
            header('Location: login.php?redirigido=1');
            exit();
        }
        // 4. si sigue activa, actualizar $_SESSION['ultima_actividad']
        $_SESSION['ultima_actividad'] = time();
    }
}
