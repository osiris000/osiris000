<?php
session_start();
#session_unset();
$fconf = '../conf2/jcores.conf';
include('../lib/php/aconf.php');
include('../lib/php/lib.php');





if(!$_SESSION["REGUSER"]) die("alert('notreg')");


#echo "alert('".$_SESSION["PERM"] ."');"; 

if($_SESSION["REGUSER_PERM"] >= $USR_PERM_PUBLIC && isset($USR_PERM_PUBLIC)):




if($_POST["action"]=="publicar"):



$JSON_FILE = $PATH_PUBLIC_TXT."/".$_POST["file"];

$data = file_get_contents($JSON_FILE);

if( ! $data) die("alert('nodata_err');");

$data = json_decode($data,true);


$mysqli = new mysqli($mysql_host, $mysql_usr, $mysql_psd, $mysql_bd);
$sql = "select id from edit_files where file_id='".$_SESSION["ARTICLE_ID"]."'";
$rquery = $mysqli->query($sql);
$article_exists =  $rquery->num_rows;



//echo "alert('$article_exists');";



if($article_exists === 0): //no existe articulo en la bd



$sql = "insert into edit_files(user_id,file_id,filecode,format,title,description,time)
 values('".$_SESSION["REGUSER_ID"]."','".$_SESSION["ARTICLE_ID"]."','".$_POST["file"]."','json','".$data["title"]."','".$data["description"]."',".$data["time"].");";


echo "alert(`

$sql

`);";

elseif($article_exists==1):

$sql = "update edit_files set title='".$data["title"]."',description='".$data["description"]."' where user_id='".$_SESSION["REGUSER_ID"]."' && file_id='".$_SESSION["ARTICLE_ID"]."'";

#echo "alert(`{$sql}`);";

else:
	/*error var*/
endif;

if($mysqli->query($sql)){


echo "response_form.innerHTML= `Artículo Publicado`;";

	} else{ die("
	alert(`
	{$mysqli->error} 
	ERRRO`);
	");
  }

//$str = join($rquery);
/*
echo<<<JS
alert(`{$str}

{\$_SESSION["ARTICLE_ID"]}
{\$data["time"]}

`);
JS;
*/

endif;



#fin post action=publicar
endif;

