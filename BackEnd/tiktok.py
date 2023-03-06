import os, glob
from scenedetect import SceneManager, detect, ContentDetector, open_video, split_video_ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import multiprocessing

def search(search_term):
    manager = multiprocessing.Manager() #Process manager
    paths = manager.dict() #Shared dictionary among all the processes
    jobs = []

    #Delete any previous contents existing in folder
    dirpath = "videos/tiktok" 
    if os.path.exists(dirpath) and os.path.isdir(dirpath): 
        shutil.rmtree(dirpath)
    os.mkdir(dirpath)

    #Function to scrape tiktok webpage and return links
    links = scrapeTiktok(search_term)
    print(links)
    
    i = 0
    for link in links:
        if link is None: #Some links do not scrape properly
            continue
        i = i + 1
        p = multiprocessing.Process(target=downloadSplit, args=(link, 'video' + str(i), dirpath, paths)) #Declare a new process which downloads and splits the video
        jobs.append(p) #Append to job list
        p.start() #Start the process

        if(i == 10): #Downloads 10 videos
            break
    
    #Waits for processes to finish their task and then joins with main process
    for proc in jobs: 
        proc.join()

    return paths

#Function to download and split the video
def downloadSplit(link, name, dirpath, paths):
    #Create a separate folder for each video
    path = os.path.join(dirpath, name) 
    os.mkdir(path)

    #Run command in terminal
    command = 'yt-dlp -f mp4 -S vcodec:h264 -o "' + name + '.mp4" ' + link
    os.system(command)

    #Opens video and detects list of scene changes
    video = open_video(name + '.mp4')
    scene_manager = SceneManager()
    scene_manager.auto_downscale = True
    scene_manager.add_detector(ContentDetector())
    scene_manager.detect_scenes(video)
    scene_list = scene_manager.get_scene_list()

    routes = [] #List to store video routes
    
    #If video contains just one scene, entire video is copied to the destination folder
    if len(scene_list) == 0:
        shutil.copy(name + '.mp4', dirpath + '/' + name + '/1.mp4')
        routes.append("http://127.0.0.1:8000/stream/" + dirpath + "/" + name + "/1.mp4") #Route to access the video
    else:
        for time in scene_list:
            #Frame/FPS = Time
            starttime = int(int(time[0])/29.97) 
            endtime = int(int(time[1])/29.97)

            #Extract subclips from original video
            ffmpeg_extract_subclip(name + '.mp4', starttime, endtime, targetname = dirpath + "/" + name + "/" +str(scene_list.index(time)+1)+".mp4")
            routes.append("http://127.0.0.1:8000/stream/" + dirpath + "/" + name + "/" + str(scene_list.index(time)+1)+".mp4") #Route to access the video

    os.remove(name + '.mp4')
    paths[name] = routes #Add routes list to dictionary shared among all processes

#Function to scrape video URLs
def scrapeTiktok(search):
    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"

    options = webdriver.ChromeOptions()
    options.binary_location = binary_location

    driver = webdriver.Chrome(driver_location, options=options) #Initializing selenium chromedriver
    query = "https://www.tiktok.com/tag/" + search + "?lang=en" #Fetches page with provided search term
    driver.get(query)

    links = []
    for i in range(1, 11):
        links.append(driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[' + str(i) + ']/div[1]/div/div/a').get_attribute('href')) #XPATH of video url
          
    driver.quit() #Close the chrome webdriver
    return links


