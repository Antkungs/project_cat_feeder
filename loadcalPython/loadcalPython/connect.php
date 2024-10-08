<?php
header('Content-Type: application/json');
function isInternetAvailable() {
    $connected = @fsockopen("www.google.com", 80);
    if ($connected) {
        fclose($connected);
        return true;
    }
    return false;
}
if(isset($_POST['ssid']) && isset($_POST['password'])) {
    $ssid = $_POST['ssid'];
    $password = $_POST['password'];

    $fileSignal = fopen("signal.txt", "w");
    fwrite($fileSignal, 1);
    fclose($fileSignal)

    $file = fopen("wificonfig_.txt", "w");
    if($file) {
        fwrite($file, $ssid . "\n");
        fwrite($file, $password);
        fclose($file);
        sleep(10);

        $signalPage = "signalPage.txt";
        $signalPage = fopen($signalPage, "r");
        if ($signalPage) {
            $file_size = filesize($file_path);
            if ($file_size > 0) {
                $content = fread($signalPage, $file_size);
            } else {
                $content = ''; 
            }
            fclose($signalPage);
            
            $content = trim($content);    
            if ($content === 'can') {
                header("Location: ip_address.html");
            } elseif ($content === 'cant') {
                header("Location: cantConnect.html");
            }
            exit();
        }
        else {
            echo "Both SSID and password are required.";
        }
    
}
}

?>

