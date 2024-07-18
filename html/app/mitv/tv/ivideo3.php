<?php


$idv = filter_input(INPUT_GET,"v",FILTER_VALIDATE_INT);
$url = filter_input(INPUT_GET,"url",FILTER_VALIDATE_URL);




if($idv){

$mysqli = new mysqli('compostela21.com', 'root', 'c21comdbpsw', 'varias2');



$sql ="select id,image,title,url,description,fuente from videos where id=".$idv;


//echo $sql;

$result = $mysqli->query($sql);
while ($row = mysqli_fetch_object($result)) {
$url = $row->url;
$poster = $row->image;
$id = $row->id;
$fuente = $row->fuente;
$title = $row->title;
}
$mysqli->close();

} elseif($url){ /* URL OK */} 


if($url){

$F = $quality="best";


switch($fuente){
    case 'dailymotion':

   $F = "hls-480-0";

        break;
        
      case 'youtube':

    $F = "18";

        break;
    
        case 'facebook':

    $F = "best";

        break;
    
    
    case 'twitch:stream':
    
    $F = "360p";
   
    break;
    
     case 'PornHub':
    
        $F = "240p";
   $puente=1;
  // $cta = "application/x-mpegurl";
   
   //echo $F;exit;
   
   
    break;
    
    case 'XNXX':
    
    $F = 'hls-360p';
    
    break;
    
    
    case 'XHamster':
    
    $F = "best";
    
    break;
    
    
        
case 'vimeo':
case 'vimeo:ondemand':

$F = "http-360p";
break;

case 'abcnews:video':
        case 'abcnews':
            $F ='PDL_MED';
       
            break;
}

if(preg_match("@^http.+vimeo.+/.+$@is",$url)) {

$F="best";
$puente = 0;

} else if(preg_match("/^http.+dailymotion.com.+$/is",$url)) {

$F="http-380-1";
$puente = 1;

} else if(preg_match("/^http.+ok\.ru.+$/is",$url)) {

$F="low";
$puente = 0;

} 
  
$cmd = "yt-dlp -s -q -f $F --get-url  --get-format --get-thumbnail --get-title  ". $url;

$link =  shell_exec($cmd);

$x = explode("\n",$link);

#print_r($x);
#exit;

$link = trim($x[1]);
$poster = "https://vtwitt.com/im.php?ratio=540&img=".rawurlencode(trim($x[2])) ;

$title = trim($x[0]);

$description = trim($x[4]);

$format = trim($x[3]);



//exit;

//echo $link."---";


$link=trim($link);
       $link = preg_replace("@^(https|http)(.+)$@is","https$2",$link);
       
       $link = preg_replace("@\?br=[0-9]+@is","",$link);
       
} else{
    
    echo "<h1>err:1</h1>";
    exit;
}
//$xl = base64_encode("link=".trim(urlencode($link))); 



/*
$id = @fopen($link,"r");
$mdata = @stream_get_meta_data($id); 
fclose($id);
*/

if(!$id && !$link){

$puente = 0;

$link = "https://www.compostela21.com/img/er404.mp4";

}


if($_REQUEST["x"]=='tunel') $puente = 1;

if($puente==1) $link="https://compostela21.com/ytbdwn.php?ein=".base64_encode("link=".urlencode($link)."&title=".$title);      




if(preg_match("@\.m3u8@si",$link)){
$ct = "application/x-mpegurl";
} else  if( preg_match("@dash@si",$format) ){

$ct = "application/mpd+m3u8";

}  else if(preg_match("@hls@si",$format)){

$ct = "application/x-mpegURL";

} else {
$ct = "video/mp4";
}

//echo $ct;exit;

if($cta) $ct = $cta;

echo "xvd('".trim($link)."','$ct',`".trim($_REQUEST["logo"])."`,escape(`".trim($title)."`),escape(`".trim($description)."`));";



