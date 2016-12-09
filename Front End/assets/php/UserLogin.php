<?php
	$servername = "31.22.17.250";
	$username = "mrrunner_user";
	$password = "password";
	$dbname = "mrrunner_mrrunner";
	
	//Login info for user's scores
	$user = $_POST['username'];
	$pwd = $_POST['password'];
	
	//Connect to database
	$con = mysql_connect($host, $user, $pass);
	$dbs = mysql_select_db($dbname, $con);
	
	//chech for correct password
	$findPwd = mysql_query("SELECT user_password FROM tbl_user WHERE user_name =" . $username);
	$correctPwd = mysql_fetch_row($findPwd);
	if ($correctPwd != $pwd){
		echo "Incorrect User Name or Password!";
	}
	else{
		//Query database for user's scores
		$result = mysql_query("SELECT * FROM TABLE");
		$arr = mysql_fetch_row($result);
	
		//Echo to json
		echo json_decode($array);
	}	
?>