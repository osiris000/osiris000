<?php
session_start();
$_SESSION["PSW"] = false;
if($_REQUEST["PSW"]=="yourpassword") $_SESSION["PSW"] =1;
if(!$_SESSION["PSW"]) {print("
<center>
<h1><form action='index.php' method='post'>
<input name='x' type='password' value='Insert Password' width='160'
onclick=\"x.value=''\">
<input type='submit' value='enviar'>
</form>
Login de Acceso
</h1>
</center>
";exit();}
else phpinfo();
?>
