# 10-07-2022 -> 20-07-2022

import urllib.request, time, os
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import insta.Driver as Driver
from insta.Driver import driver
from insta.Util import util
from insta.Util import data as path
from insta.Util import getNameByUrl, createFolderSimple, moveFileToData

MAX_WORKERS = 250

class_rectProfile = path['Download']['Story']['Rect']['rectProfile']['class']
class_NextArrow = path['Download']['Story']['Arrow']['next']['class']
class_PrevArrow = path['Download']['Story']['Arrow']['prev']['class']
class_ImgSrc = path['Download']['Story']['Extract']['img_src']['class']
class_VideSrc = path['Download']['Story']['Extract']['video_src']['class']
class_ElementStory = path['Download']['Story']['InfoStory']['element_story']['class']
class_ElementStoryWithWidth = path['Download']['Story']['InfoStory']['element_story_width']['class']


def getSoup():
    return BeautifulSoup(str(driver.page_source), "lxml")


class Arrow:
    def checkIfExist(self, isNext: bool):
        if(isNext):
            arrowType = class_NextArrow
        else:
            arrowType = class_PrevArrow
        if Driver.check_element_exit_class(arrowType):
            return "exist"
        else: 
            return 0

    def clickOnIt(self,  isNext: bool, delay: float):
        if(isNext):
            arrowType = class_NextArrow
        else:
            arrowType = class_PrevArrow
        Driver.click_element_class(arrowType, delay)

class Extract:

    def imgUrl(self):
        url_img = getSoup().find("img", class_ = class_ImgSrc)
        return url_img['src']

    def videoUrl(self):
        url_video = getSoup().find("video", class_ = class_VideSrc)
        return url_video['src']

class InfoStory:

    def getWidthStory(self):
        soup = getSoup()
        post = soup.find_all("div", class_ = class_ElementStoryWithWidth)
        try:
            return round(float(str(post).split(" ")[-1].split("%")[0].replace(" ", "")), 2)
        except:
            return 0.00

    def getActualStory(self):
        soup = getSoup()
        posts = soup.find_all("div", class_ = class_ElementStory)
        maxPost = len(posts)
        actualPost = 0
        for i in range(maxPost):
            if(len(posts[i]) == 2):
                actualPost = i
        return actualPost, maxPost

class UtilStory():

    arrow = Arrow()
    extract = Extract()
    infoStory = InfoStory()

    def downloadElement(self, url, folder, name):
        urllib.request.urlretrieve(url, folder+"//"+name)

    def getNameUrl(self, url):
        a = urlparse(url)
        return os.path.basename(a.path)

    def downloadList(self, url, listSrc):
        createFolderSimple(getNameByUrl(url))
        folderPath = getNameByUrl(url)
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for i in range(len(listSrc)):
                url = listSrc[i][1]
                nameUrl = self.getNameUrl(url)
                if(listSrc[i][2] == "video"):
                    executor.submit(self.downloadElement, url, folderPath, nameUrl.replace("jpg", "mp4"))
                else:
                    executor.submit(self.downloadElement, url, folderPath, nameUrl.replace("mp4", "jpg"))

utilStory = UtilStory()

def mainStory(url):

    Driver.getPage(url, 3)
 
    util.print.string("Click on story")
    time.sleep(3)
    Driver.click_element_class(class_rectProfile, 2)

    while utilStory.arrow.checkIfExist(isNext = False) != 0 :
        utilStory.arrow.clickOnIt(isNext = False, delay=0.5)

    url_element = []
    
    while utilStory.arrow.checkIfExist(isNext = True) != 0 :
        
        width = utilStory.infoStory.getWidthStory()
        actualStory = utilStory.infoStory.getActualStory()
        actualPost = actualStory[0] + 1
        maxPost = actualStory[1]
        util.print.TwostringAndInt("Get story : ", actualPost, " width : ", width, end=True)

        if width > 10:
            try: srcVideo = utilStory.extract.videoUrl()
            except: srcVideo = "" 

            try: srcImg = utilStory.extract.imgUrl()
            except: srcImg = ""  

            if(len(srcVideo) != 0):
                url_element.append([actualPost, srcVideo, "video"])
            else:
                url_element.append([actualPost, srcImg, "img"])

            utilStory.arrow.clickOnIt(isNext = True, delay = 0.3)

    print('\r')
    util.print.stringAndInt("Stories find : ", len(url_element))

    utilStory.downloadList(url, url_element)

    nameProfile = getNameByUrl(url)
    category = "STORY"
    moveFileToData(getNameByUrl(url), category)
    util.print.stringAndInt("FOLDER : ", str(os.getcwd())+"\\data\\profile\\"+nameProfile+"\\"+category+"\\"+util.getDateNow() )

    driver.close()