<!-- We are going to fetch the password, and IP from the GCP Cloud SQL -->

<html>
<head><title>Welcome to my excellent blog</title></head>
<body>
<h1>Welcome to my excellent blog</h1>
<?php
 $dbserver = "CLOUDSQLIP"; // Cloud SQL database IP
$dbuser = "blogdbuser"; // SQL user role's name other than root
$dbpassword = "DBPASSWORD"; // Cloud SQL database password
// In a production environment, we would not store the MySQL
// password in the document root. Instead, we would store it in a
// configuration file elsewhere on the web server VM instance.
$conn = new mysqli($dbserver, $dbuser, $dbpassword);
if (mysqli_connect_error()) {
        echo ("Database connection failed: " . mysqli_connect_error());
} else {
        echo ("Database connection succeeded.");
}
?>
</body></html>

<!-- End -->