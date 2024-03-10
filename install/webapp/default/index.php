<?php
session_start();
$_SESSION["ADM"] = false;
if($_REQUEST["x"]=="123454321") $_SESSION["ADM"] =1;
if(!$_SESSION["ADM"]) {print("
<center>
<h1><form action='index.php' method='post'>
<input name='x' type='password' value='Insert Password' width='160'
onclick=\"x.value=''\">
<input type='submit' value='enviar'>
</form>
Login de Acceso
</h1>
</center>
");phpinfo();exit();}

?>
