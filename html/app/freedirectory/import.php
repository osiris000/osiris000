<?php
set_time_limit(0);

echo "IS";


include $_SERVER["DOCUMENT_ROOT"]."/lib-util2.php";

$_REQUEST["url"] ? $url = $_REQUEST["url"] : die("Not Url") ; 
$_REQUEST["path"] ? $path = $_REQUEST["path"] : die("Path Error") ; 
$_REQUEST["option"] ? $option = $_REQUEST["option"] : die("Option fail") ;

$ext = pathinfo($url)["extension"] ;
$fname = pathinfo($url)["filename"] ; 

 
switch($ext){

/*extensions disabled*/

case 'php':
case 'py':
case 'perl':
case 'cgi':

die("<h3>Protect Discover</h3>");

break;


default:
break;
} 
 
 
switch($option){

case 'ydl':

    $cd = "cd /var/www/vhosts/compostela21.com/vtwitt.com/jsa/media/$path && " ;
//    $uid = md5($url);
    $exec = " --exec 'php /var/www/vhosts/compostela21.com/vtwitt.com/jsa/util/postp.php' " ;
   // echo $cd;
    $url = filter_var($url, FILTER_CALLBACK, array('options' => 'escapeshellarg'));
   
   
    $id = popen("$cd yt-dlp -f best  --write-description --write-info-json --restrict-filenames --write-thumbnail $exec $url","r") ;
    while($fr = fread($id,255)){
   echo $fr."<br>"; 
   echo str_pad('',4096)."\n";  
    }

  
  pclose($id);
  echo "EXIT youtube-dl";
 exit;

break;

default:
break;
}


switch($ext){

case 'gif':
case 'jpg':
case 'jpeg':
case 'mp4':
case 'webm':
case 'mp3':
case 'png':
case 'jpeg':
case 'webp':
case 'svg':
case 'pdf':
case 'txt':
case 'html':


$fname = format_title_for_url($fname);

$fname = $path.$fname.".".$ext;

$fname = str_replace('../',"",$fname);

$x = file_get_contents($url);

if($x) {



$id = fopen($fname,"w") or die("writeError");
fwrite($id,$x);
fclose($id);


echo "<a href='https://vtwitt.com/jsa/media/".$fname."' target='_blank'>".$fname."</a>";
} else echo "Not FGC";
break;

default:

echo "$fname<br>"."$ext extensión no permitido";

break;

}

//echo $_REQUEST["path"];

//print_r($data);

?>
