<?php
    include('header.php');
?>
<style>
    /* Estilo minimalista solo para esta página, por encima del tema del resto del sitio */
    header, form, p {
        background: none;
        backdrop-filter: none;
        -webkit-backdrop-filter: none;
        border: none;
        box-shadow: none;
    }
    header h1 {
        background: none;
        color: #222;
    }
    header p {
        color: #555;
    }
    body {
        background: #fafafa;
        animation: none;
    }
    h2 {
        font-size: 1.3em;
        font-weight: 600;
        border-bottom: 1px solid #ddd;
        color: #222;
    }
    form {
        display: block;
        max-width: 360px;
        margin: 20px 0;
    }
    form label {
        display: block;
        margin-bottom: 6px;
        color: #333;
    }
    form input[type="text"] {
        width: 100%;
        padding: 8px 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 1em;
        color: #222;
        background: #fff;
    }
    form button {
        margin-top: 10px;
        padding: 8px 16px;
        border: 1px solid #333;
        border-radius: 4px;
        background: #fff;
        color: #333;
        cursor: pointer;
    }
    form button:hover {
        background: #333;
        color: #fff;
    }
    p {
        padding: 8px 0;
        font-weight: normal;
        color: #222;
    }
</style>
<h2>Comprobador de palíndromos</h2>
<form action="palindromo.php" method="get">
    <label for="cadena">Palabra o frase:</label>
    <input type="text" name="cadena" id="cadena" placeholder="Ej: Anita lava la tina">
    <button type="submit">Verificar</button>
</form>

<?php
    if (isset($_GET['cadena']) && $_GET['cadena'] !== '') {
        $cadena = $_GET['cadena'];
        $cadena = strtolower($cadena);
        $cadena = str_replace(" ", "", $cadena);
        $invertido = strrev($cadena);

        function esPalindromo($cadena, $invertido) {
            if ($cadena == $invertido) {
                echo "<p>✅ La cadena es un palíndromo.</p>";
            } else {
                echo "<p>❌ La cadena no es un palíndromo.</p>";
            }
        }
        esPalindromo($cadena, $invertido);
    } elseif (isset($_GET['cadena'])) {
        echo "<p>⚠️ Cadena vacía, debe escribirse una cadena para verificar si es palíndromo.</p>";
    }
?>
