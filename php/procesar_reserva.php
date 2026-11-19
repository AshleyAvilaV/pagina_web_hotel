<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {

   
    $nombre = trim($_POST['nombre']);
    $email = trim($_POST['email']);
    $telefono = trim($_POST['telefono']);
    $fecha_entrada = $_POST['fecha_entrada'];
    $fecha_salida = $_POST['fecha_salida'];
    $huespedes = $_POST['huespedes'];
    $comentarios = trim($_POST['comentarios']);

    $errores = [];

   
    if (empty($nombre)) {
        $errores[] = "El nombre es obligatorio.";
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errores[] = "El formato del correo no es válido.";
    }

    $hoy = date('Y-m-d');
    if ($fecha_entrada < $hoy) {
        $errores[] = "La fecha de entrada no puede ser en el pasado.";
    }
    if ($fecha_salida <= $fecha_entrada) {
        $errores[] = "La fecha de salida debe ser posterior a la de entrada.";
    }

    if ($huespedes < 1) {
        $errores[] = "Debe haber al menos 1 huésped.";
    }

    
    if (empty($errores)) {
        
       
        $archivo_json = '../data/reservas.json';

        // lee reservas, deberia iniciar con un array vacio
        $reservas = [];
        if (file_exists($archivo_json)) {
            $contenido = file_get_contents($archivo_json);
            $reservas = json_decode($contenido, true);
        }

        
        $nueva_reserva = [
            "id" => count($reservas) + 1,
            "nombre" => $nombre,
            "email" => $email,
            "telefono" => $telefono,
            "fecha_entrada" => $fecha_entrada,
            "fecha_salida" => $fecha_salida,
            "huespedes" => (int)$huespedes,
            "comentarios" => $comentarios
        ];

        
        $reservas[] = $nueva_reserva;

       //para leer en el archivo json
        file_put_contents($archivo_json, json_encode($reservas, JSON_PRETTY_PRINT));

        echo "<h1>¡Reserva Exitosa!</h1>";
        echo "<p>Gracias <strong>$nombre</strong>. Tu reserva ha sido registrada.</p>";
        echo "<br><a href='../reserva.html'>Volver al formulario</a>";
        
    } else {
       
        echo "<h1>Errores en la reserva</h1>";
        echo "<ul>";
        foreach ($errores as $error) {
            echo "<li style='color: red;'>$error</li>";
        }
        echo "</ul>";
        echo "<br><a href='../reserva.html'>Volver e intentar de nuevo</a>";
    }
} else {
    echo "Acceso denegado.";
}
?>