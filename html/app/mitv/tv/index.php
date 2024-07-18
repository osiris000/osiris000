<?php
//include 'logeador.php';

//header("location:https://compostela21.com/tv/app.php?".$_SERVER["QUERY_STRING"]) ; 

//exit;

parse_str(base64_decode($_REQUEST["z"]));


$hack = $_REQUEST["hack"] ; 

if($url) $_REQUEST["url"] = $url ;
if($img) $_REQUEST["img"] = $img ;
if($web) $_REQUEST["web"] = $web ;
if($mod) $_REQUEST["mod"] = $mod ;
if($xscard) $_REQUEST["xscard"] = $xscard ;
if($desc) $_REQUEST["desc"] = $desc ;
elseif($hack) $desc = $hack ; 
else $desc = $web ; 

$url = filter_var($_REQUEST["url"],FILTER_VALIDATE_URL);
$web = filter_var($_REQUEST["web"],FILTER_VALIDATE_URL);

if(!$url && !$z){

/*DEFAULT INDEX TV */

$url = "../channels/main/ultrafast.m3u8";
$web = $_SERVER["SERVER_PROTOCOL"]."://".$_SERVER["SERVER_NAME"]."".$_SERVER["PHP_SELF"];
$xscard = "Free Tv";
$desc = "Cine TV 1";
$img = "https://www.compostela21.com/videojs/elementos/_1_Tv/cineTv.png&ratio=420";
}


if($web) $ttcard = $web ;
else $title = $url;

#echo "<script>alert('$url')</script>";

if(!$_RESQUEST["mod"]) $mod = "ydl";
else $mod = $_RESQUEST["mod"] = "hrq";

if(!$_REQUEST["img"]) $im = $url;
else {
	$im = $_REQUEST["img"];
	$mod = "hrq";
}


?>
<!DOCTYPE html>
<html lang="es">
    <head><meta charset="utf-8">
        <title><?=$_REQUEST["xscard"]?></title>
        <meta name="viewport" content="initial-scale=1, maximum-scale=1">
    <script src="//cdn.jsdelivr.net/npm/hls.js@latest"></script>
    
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">       
        <meta name="keywords" content="">
        <meta name="viewport" content="initial-scale=1, maximum-scale=1">
        
<meta property="twitter:card" content="summary_large_image">  
<meta property="og:locale" content="es_ES">
<meta property="og:type" content="article">
<meta property="og:site_name" content="vtwitt.com" />


<?php




$pt = " ".date("d/m/Y h:i:s")." ";
if($_REQUEST["xscard"]) $description .= $_REQUEST["xscard"] ;   
?>
<meta property="og:title" content="<?=$pt?> 👇 <?=$ttcard?>">
<meta property="og:description" content="<?=$desc?>">
<meta property="og:image" content="https://vtwitt.com/jsa/media/im.php?ratio=640&mod=<?=$mod?>&img=<?=$im?>">

      
<?php


if($_REQUEST["img"]){

$_REQUEST["img"] = urldecode($_REQUEST["img"]);

$getImg=<<<JS

p = `{$_REQUEST["img"]}`

JS;

}



?>
<?php
$sourcevideo=<<<SV
        <div  style="padding:10px;width:640px;max-width:100%;max-height:100vw;height:auto;float:left" >

<video poster="$row->image" loop id="video_w_$row->id"  style="width:100%;max-width:100%;max-height:100%;height:flex" controls></video>


</div>


<div style="position:fixed;right:10px;top:5px;width:320px;text-align:center;font-family:arial;font-size:13px;color:#aa44bd">

HW!!

</div>


<div style="border:solid 0px red;position:relative;height:flex;display:inline-block;margin:10px;width:flex;text-align:center;padding:10px;" id='pub_disp'>

<div style="paddingn:10px;width:320px;position:relative;">
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-3185107427297382"
     data-ad-slot="1119731952"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>

</div>

<script>


  var video = document.getElementById('video_w_$row->id');
 function xvd(videoSrc,ct,p,t,d){


$getImg

//document.title = unescape(t)

video.preload = "metadata"
video.type = ct
video.poster = p

if (video.canPlayType(ct)) {
  video.src = videoSrc;

  } else if (Hls.isSupported()) {
  var hls = new Hls();
  hls.loadSource(videoSrc);
  hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
     console.log('Manifest loaded, found ' + data.levels.length + ' quality level');
    });
   
      hls.attachMedia(video);
}  
   
   
video.preload = true ;
video.play();
video.volume=0.3
video.controls = true;



}
    
</script>

 </div>
SV;


$host= $_SERVER["HTTP_HOST"];
$urlhref= $_SERVER["REQUEST_URI"];

?>


     
        
        <script type="text/javascript" src="https://www.compostela21.com/tec/ajax/lib/hxr.js"></script>
       
               <script type="text/javascript" src="https://platform-api.sharethis.com/js/sharethis.js#property=6168f3274564d200122a7e54&product=inline-share-buttons" async="async"></script>
      
        <style>body{margin:0;background:inherit;}</style>
   
<body>   
   
    <div class="sharethis-inline-share-buttons"></div>
     
<?php


echo '<div style="width:100%;height:40px;display:inline-block" id="a1">';
echo "<div style='float:left;z-index:11;margin:5px;'><a style='text-decoration:none;color:#AA1222' href='javascript:void(0)' onclick='document.getElementById(\"a1\").style.display = `none`'><b>Cerrar Animación</b></a></div>";
echo file_get_contents("https://vtwitt.com/jsa/media/records/baner-h-2.html"); 

echo '</div>';

       

echo<<<HTML

$sourcevideo
HTML;


$_REQUEST["url"] ? $url = $_REQUEST["url"] : $v = $_REQUEST["v"] ;

if($v) $url = "v=".$url ;
else $url = "url=".$url ;

?>   
                 

   

  <script type="text/javascript">

ajaxReturn("<?=$url?>","","/tv/ivideo3.php","GET","function");
           
  </script>
       
</body></html>
