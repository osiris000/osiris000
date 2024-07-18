<?php
#include 'logeador.php';

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

$url = "https://tv.vtwitt.com/mitv/live/live2.m3u8";
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




<?php


$REQUEST=<<<REQUEST

<script>


 RQ = true

onload = function () {



 ajax("url=$url&logo=$img","","ivideo3.php","GET");


}

</script>

REQUEST;




echo<<<CP

<!DOCTYPE html>
<html lang="es">
    <head><meta charset="utf-8">
        <title>{$_REQUEST["xscard"]}</title>
        {$REQUEST}
        <meta name="viewport" content="initial-scale=1, maximum-scale=1">
        <script data-ad-client="ca-pub-3185107427297382" async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
        <meta name="keywords" content="">
        <meta name="viewport" content="initial-scale=1, maximum-scale=1">
<meta property="twitter:card" content="summary_large_image">  
<meta property="og:locale" content="es_ES">
<meta property="og:type" content="article">
<meta property="og:site_name" content="vtwitt.com" />
<meta property="og:title" content="{$xscard} 👇 {$desc}">
<meta property="og:description" content="{$desc}">
<meta property="og:image" content="https://vtwitt.com/jsa/media/im.php?ratio=360&mod={$mod}&img={$im}">
<script src="load.js"></script></head>
<!-- Google tag (gtag.js) -->

<script async src="https://www.googletagmanager.com/gtag/js?id=G-2VS3W0WSYF"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-2VS3W0WSYF');
</script>
 
<body></body>
</html>



CP;








