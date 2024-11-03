<?php
function isInternetAvailable() {
    $connected = @fsockopen("www.google.com", 80);
    return $connected ? true : false;
}

function getClientIP() {
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        return $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        return explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0];
    }
    return $_SERVER['REMOTE_ADDR'];
}

if (isset($_POST['ssid']) && isset($_POST['password'])) {
    $ssid = htmlspecialchars(trim($_POST['ssid']));
    $password = htmlspecialchars(trim($_POST['password']));
    $token = htmlspecialchars(trim($_POST['token']));
    // Write signal to indicate process start
    file_put_contents("signal.txt", "1");
    // Create or overwrite wificonfig_.txt
    if ($file = fopen("wificonfig_.txt", "w")) {
        fwrite($file, $ssid . "\n");
        fwrite($file, $password . "\n");
        fwrite($file, $token . "\n");
        fclose($file);
        
    
    } else {
        echo "Error writing to configuration file.";
        exit;
    }
    sleep(5); 
    file_put_contents("signal.txt", "0");
} else {
    echo "Both SSID and password are required.";
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connecting</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f8ff;
            font-family: Arial, sans-serif;
            color: #333;
        }

        h1 {
            font-size: 3rem;
            font-weight: bold;
            color: red;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div>
        <h1>Try Again</h1>
	 <a href="../index.php">Back</a>    
</div>
</body>
</html>
