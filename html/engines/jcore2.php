<?php
session_start();

$fconf = '../conf2/jcores.conf';
include('../lib/php/aconf.php');
include('../lib/php/lib.php');


 $mysqli = new mysqli($mysql_host, $mysql_usr, $mysql_psd, $mysql_bd);


$str = join($_POST);

echo<<<JS
alert(`{$str}`);
JS;