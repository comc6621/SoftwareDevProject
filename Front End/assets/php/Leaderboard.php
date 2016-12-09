<?php
	$servername = "31.220.17.250";
	$username = "mrrunner_user";
	$password = "password";
	$dbname = "mrrunner_mrruneer";
	
	//Connect to database
	$con = mysql_connect($host, $user, $pass) or die('Could not connect to database!');
	$dbs = mysql_select_db($dbname, $con);
	
	//Query database for user's scores
	$result = mysql_query("SELECT TOP 10 user_id, high_score, max_dist, longest_time
							FROM tbl_pStats
							ORDER BY high_score DESC");
	$arr = mysql_fetch_row($result);
	
	//Echo to json
	echo json_decode($arr);		
?>