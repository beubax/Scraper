from selenium import webdriver
from selenium.webdriver.common.by import By
import time

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

driver = scrapeInstagram("bench press")