<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <h1>Welcome to my website</h1>
    <p>This is a simple HTML document.</p>

    <?php
    // This is a PHP block$
    $servername = "db";
    $username = "blog";
    $password = "password";
    $dbname = "blog";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    echo "Database server IP: " . gethostbyname($servername);

    ?>
</body>

</html>