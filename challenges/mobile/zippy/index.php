<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$upload_dir = "/var/www/html/uploads/";

if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0777, true);
}

$flag ="cc_ctf{zip_slip_the_creds_and_dip}";
file_put_contents("/var/www/html/flag.txt", $flag);

if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_FILES["zipfile"])) {
    $zip_file = $_FILES["zipfile"]["tmp_name"];
    
    $zip = new ZipArchive;
    if ($zip->open($zip_file) === TRUE) {
        // Debug output
        echo "Zip contents:\n";
        for ($i = 0; $i < $zip->numFiles; $i++) {
            echo "File[$i]: " . $zip->getNameIndex($i) . "\n";
        }
        
        $zip->extractTo($upload_dir);
        $zip->close();
        echo "\nFile uploaded and extracted successfully";
    } else {
        echo "Failed to process zip file";
    }
    exit();
}

if (isset($_GET['file'])) {
    $requested_file = $_GET['file'];
    $file_path = $upload_dir . $requested_file;
    
    echo "Attempting to read: " . $file_path . "\n";
    
    if (file_exists($file_path)) {
        header('Content-Type: text/plain');
        echo file_get_contents($file_path);
    } else {
        echo "File not found. Tried to read: " . $file_path;
    }
    exit();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>File Upload Challenge</title>
</head>
<body>
    <h1>Zip File Upload</h1>
    <form action="" method="post" enctype="multipart/form-data">
        <input type="file" name="zipfile" accept=".zip">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
