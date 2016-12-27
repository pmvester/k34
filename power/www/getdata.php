<?php
header("Content-Type: text/html; charset=utf-8");
$con = mysql_connect("localhost","logger","13142k34");

if (!$con) {
  die('Could not connect: ' . mysql_error());
}

mysql_select_db("housedb", $con);

$result = mysql_query("SELECT * FROM Data WHERE timestamp > DATE_SUB(CURDATE(), INTERVAL 7 DAY)");

while($row = mysql_fetch_array($result)) {
  $uts=strtotime($row['timestamp']);
  $date=date("l, F j Y H:i:s",$uts); 
  echo $date . "\t" . $row['power'] . "\n";
}

mysql_close($con);
?> 
