<?php
session_start();
$fconf = "gen.app.conf";
include "parse_ini.php";
if(isset($_REQUEST["PSW"])) {
if($_REQUEST["PSW"]=="yourpassword") $_SESSION["PSW"] =1;
}
if(!$_SESSION["PSW"]) {
echo<<<XE
<center>
<h1><form action='index.php' method='post'>
<input name='PSW' type='password' value='Insert Password' width='160'
onclick="x.value=''">
<input type='submit' value='enviar'>
</form>
Login de Acceso
</h1>
</center>
XE;
exit();
} else phpinfo();
?>
