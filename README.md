Backend - 

	main.py → Fastapi main containing two api paths – getVideos/ and stream/ - to download, split and display videos. The former calls youtube.py, instagram.py and tiktok.py and returns a json response 			
	containing video paths. The latter takes in a video source as a parameter and returns a stream as a response.  

	youtube.py → Uses selenium to scrape youtube links. These links are fed into individual processes to be downloaded and split into individual clips. 

	instagram.py → Uses selenium to scrape instagram links in google videos. These links are fed into individual processes to be downloaded and split into individual clips. 

	tiktok.py → Uses selenium to scrape tiktok links in tiktok’s trending page. These links are fed into individual processes to be downloaded and split into individual clips. 

Frontend -

	Angular application to provide an interface for users to interact with the system. 

	Homepage → Displays the title, a search button to input keyword and logo of platforms currently supported. Once videos have been successfully fetched, a button displays to take user to videos page.

	Videos → Three tabs on the top redirect user to respective platform’s videos. Each platform has ten videos downloaded, and user can select any of the sub-tabs to view videos. 
