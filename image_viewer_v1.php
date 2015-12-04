<!DOCTYPE html>
<!-- 
Photo Viewer
View all images in a directory by hovering over buttons.
This allows you to stay on the same page rather than clicking the back button every time you want to see a different image.
Image name can not have any spaces!!

Created by Brian Blaylock
Date: November 30, 2015

-->
<head>
<title>Image Viewer</title>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script> <!--Open site with this header-->

<script>
function change_picture(img_name){
		document.getElementById("display_img").src = img_name;
		document.getElementById("display_img").style.width= '98%';
		if (img_name=='http://home.chpc.utah.edu/~u0553130/MS/June18_HRRR/windseries/snipped_lake/TS_locations.png'){
			document.getElementById("display_img").style.height='550px';
			document.getElementById("display_img").style.width='500px';
		}
	}
function empty_picture(img_name){
	document.getElementById("display_img").src = img_name;
	document.getElementById("display_img").style.width= '40%';
}

</script>
</head>


<body>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/sitemenu.js"></script>	
<br>
<h1 align="center" style="font-family:Garamond">Image Viewer</h1>

<div style="background-color:#f5f5f5; width:85%; margin-left:auto; margin-right:auto;">	
	
	
<!-- PHP for getting file names in the directory-->
	<?php
			$dir =  getcwd();

			// open this directory 
			$myDirectory = opendir($dir);

			// get each entry, but only if it contains the Station Identifier
			while($entryName = readdir($myDirectory)) {
				if (strpos($entryName,".png") !== false or strpos($entryName,".jpg") !== false or strpos($entryName,".gif") !== false or strpos($entryName,".GIF") !== false or strpos($entryName,".PNG") !== false or strpos($entryName,".JPG") !== false){
					$dirArray[] = $entryName;
				}
				
			}
		
			// close directory
			closedir($myDirectory);
			
			//sort directory array by alphabetical order
			sort($dirArray);					
			
			//	count elements in array
			$indexCount	= count($dirArray);
			//echo $dir;
			//echo "<br>";
			// The server path to public_html directory
			//echo substr($dir,0,53);
			// The path after public_html. Will use this for creating the URL path to the image
			echo substr($dir,53);
			$img_URL_dir = substr($dir,53);

	?>
			
<!--Area for sounding plot images to appear-->
<div align="center">
		
		<br>
		<!--PHP for creating buttons and image-->
			<?php
			// loop through the array of files and display a link to the image

							
			for($index=0; $index < $indexCount; $index++) {
				$extension = substr($dirArray[$index], -3);
				if ($extension == 'jpg' or $extension == 'gif' or $extension == 'png'){ // list only jpg, gif, and png images
					
						//if sounding exists, then make green button
						$new_image = 'http://home.chpc.utah.edu/~u0553130/'.$img_URL_dir.'/'.$dirArray[$index].'';
						echo 
							'
							<input style="height:25px;"type="button" value="'.$dirArray[$index].'" onmouseover=change_picture("'.$new_image.'");>
							';
					
				}	
			}
			
			?>
		<br><br><img class="style1" id="display_img" style="width:50%" src="./images/empty.jpg" alt="empty"><br><br>

	</div>
</div>
<br>
	<br>

<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteclose.js"></script>

</body>
</html>
