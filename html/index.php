<?php
// File path to read the configuration data
$filePath = 'txt/wificonfig_.txt';

$token = '';

// Check if the file exists and is readable
if (file_exists($filePath) && is_readable($filePath)) {
    // Read the contents of the file into an array
    $dataArray = file($filePath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    
    // Extract the last line as the token
    if (!empty($dataArray)) {
        $token = trim($dataArray[count($dataArray) - 1]); // Get the last line
    }
} else {
    echo "Unable to read the configuration file.";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFi Configuration</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <form id="formWifi" action="/txt/connect.php" method="post">
        <h1>Connect WiFi</h1>
        <label for="ssid">SSID:</label>
        <input type="text" id="ssid" name="ssid" placeholder="ssid" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password"  placeholder="password" required><br>
        <label for="token">Token Line:</label>
        <input type="text" id="token" name="token" value="<?php echo htmlspecialchars($token); ?>" placeholder="token" required><br>
        <input type="submit" value="Submit">
    </form>
</body>
<script>
    document.getElementById('formWifi').onsubmit = function() {
        document.getElementById('form').style.display = 'block';
    };
</script>
</html>
