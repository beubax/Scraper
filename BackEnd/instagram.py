import os, glob
from scenedetect import SceneManager, detect, ContentDetector, open_video, split_video_ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import multiprocessing

def search(search_term):
    manager = multiprocessing.Manager()
    paths = manager.dict()
    jobs = []
    dirpath = "videos/instagram"
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
    os.mkdir(dirpath)

    links = scrapeInstagram(search_term)
    i = 0

    for link in links:
        if link is None:
            continue
        i = i + 1
        p = multiprocessing.Process(target=downloadSplit, args=(link, 'video' + str(i), dirpath, paths))
        jobs.append(p)
        p.start()
        if(i == 10):
            break
    
    for proc in jobs:
        proc.join()

    return paths

def downloadSplit(link, name, dirpath, paths):
    path = os.path.join(dirpath, name)
    os.mkdir(path)
    command = 'yt-dlp -f mp4 -o "' + name + '.mp4" ' + link
    os.system(command)
    video = open_video(name + '.mp4')
    scene_manager = SceneManager()
    scene_manager.auto_downscale = True
    scene_manager.add_detector(ContentDetector())
    scene_manager.detect_scenes(video)
    scene_list = scene_manager.get_scene_list()
    routes = []
    if len(scene_list) == 0:
        shutil.copy(name + '.mp4', dirpath + '/' + name + '/1.mp4')
        routes.append("http://127.0.0.1:8000/stream/" + dirpath + "/" + name + "/1.mp4")
    else:
        for time in scene_list:
            starttime = int(int(time[0])/29.97)
            endtime = int(int(time[1])/29.97)
            # if(endtime - starttime) < 5:
            #     continue
            ffmpeg_extract_subclip(name + '.mp4', starttime, endtime, targetname = dirpath + "/" + name + "/" +str(scene_list.index(time)+1)+".mp4")
            routes.append("http://127.0.0.1:8000/stream/" + dirpath + "/" + name + "/" + str(scene_list.index(time)+1)+".mp4")
    os.remove(name + '.mp4')
    paths[name] = routes

def scrapeInstagram(search):
    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"

    options = webdriver.ChromeOptions()
    options.binary_location = binary_location

    driver = webdriver.Chrome(driver_location, options=options)
    query = "https://www.google.com/search?q=" + search + " instagram"
    driver.get(query)
    time.sleep(1)
    element = driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[3]/a')
    element.click()
    time.sleep(1)
    links = []
    for i in range(1, 11):
        links.append(driver.find_element(By.XPATH, '//*[@id="rso"]/div[' + str(i) + ']/div/div/div/video-voyager/div/div[1]/a').get_attribute('href'))
    print(links)  
    driver.quit()
    return links


