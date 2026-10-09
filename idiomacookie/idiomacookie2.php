<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>This page are written in English</h1>
    <a href="idiomacookie.php?idioma=es">Español</a>
    <a href="idiomacookie2.php?idioma=en">English</a>
    <?php
    //el valor idioma por defecto es español, aqui comprobamos
    // si existe la cookie y si no existe la creamos con un valor de es
        if(!isset($_COOKIE['idioma'])){
            setcookie('idioma', 'es', time()+3600*24);
        }
        if(isset($_GET['idioma'])){
            setcookie('idioma',$_GET['idioma'], time()+3600*24);
        }
        if(isset($_COOKIE['idioma'])){
        if($_COOKIE['idioma']== 'es'){
            header('Location: idiomacookie.php');
        }
        // if($_COOKIE['idioma']== 'en'){
        //     header('Location: idiomacookie2.php');
        // }
    }
    ?>
</body>
</html>


