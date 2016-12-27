<?php
header("Content-Type: text/html; charset=utf-8");
$con = mysql_connect("localhost","logger","13142k34");

if (!$con) {
  die('Could not connect: ' . mysql_error());
}

mysql_select_db("testdb", $con);

$result = mysql_query("SELECT * FROM Data");

while($row = mysql_fetch_array($result)) {
  echo $row['Pulses']. "\n";
}

mysql_close($con);
?> 
