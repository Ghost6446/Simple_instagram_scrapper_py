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

class_rectHigh = path['Download']['Highlights']['Rect']['rectProfile']['class']
class_listHigh = "_acaz"
class_textSingolHigh = "x1lliihq"
class_NextArrow = path['Download']['Highlights']['Arrow']['next']['class']
class_PrevArrow = path['Download']['Highlights']['Arrow']['prev']['class']
class_ImgSrc = path['Download']['Highlights']['Extract']['img_src']['class']
class_VideSrc = path['Download']['Highlights']['Extract']['video_src']['class']
class_ElementHigh = path['Download']['Highlights']['InfoHigh']['element_story']['class']
class_ElementHighWithWidth = path['Download']['Highlights']['InfoHigh']['element_story_width']['class']


def getSoup():
    return BeautifulSoup(str(driver.page_source), "lxml")

class Arrow:
    
    def checkIfExist(self, isNext: bool):
        if(isNext):
            arrowType = class_NextArrow
        else:
            arrowType = class_PrevArrow
        if Driver.click_element_class(arrowType):
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
        url_img = getSoup().find_all("img", attrs={"class": class_ImgSrc})
        for e in url_img:
            if e != None:
                return e['src']

    def videoUrl(self):
        url_video = getSoup().find_all("video", attrs={"class": class_VideSrc})
        for e in url_video:
            if e != None:
                return e['src']

class InfoHigh:
    
    def getWidth(self):
        soup = getSoup()
        post = soup.find_all("div", attrs={"class": class_ElementHighWithWidth})
        try:
            return round(float(str(post).split(" ")[-1].split("%")[0].replace(" ", "")), 2)
        except:
            return 0.00

    def getActualPost(self):
        soup = getSoup()
        posts = soup.find_all("div", attrs={"class": class_ElementHigh})
        maxPost = len(posts)
        actualPost = 0
        for i in range(maxPost):
            if(len(posts[i]) == 2):
                actualPost = i
        return actualPost, maxPost

class UtilHigh():

    arrow = Arrow()
    extract = Extract()
    infoStory = InfoHigh()

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

utilHigh = UtilHigh()

def mainHigh(url):

    Driver.getPage(url, 3)

    soup = getSoup()
    listClassHigh =  soup.find_all("li", attrs={"class": class_listHigh})

    list_name_storie = []
    for e in listClassHigh:
        element = e.find_all_next("span", attrs={"class": class_textSingolHigh})
        for i in range(len(element)):
            list_name_storie.append(element[i].text)

    list_stories = list(dict.fromkeys(list_name_storie))
    util.print.stringAndInt("Categories find :", len(list_stories))
    util.print.List("Stories", list_stories)

    util.print.string("Click on high")
    driver.find_element_by_class_name("_aams").click()
    time.sleep(9)

    url_element = []
    while utilHigh.arrow.checkIfExist(isNext = True) != 0 :
        width = utilHigh.infoStory.getWidth()
        actualStory = utilHigh.infoStory.getActualPost()
        actualPost = actualStory[0]+1
        maxPost = actualStory[1]
        util.print.ThreeStringAndInt("Page: ", actualPost, "of: ", maxPost, " width: ", width, end=True)

        if width > 8:
            srcVideo = utilHigh.extract.videoUrl()
            srcImg = utilHigh.extract.imgUrl()
            try:
                if(len(srcVideo) > 10):
                    url_element.append([actualPost, srcVideo, "video"])
            except:
                url_element.append([actualPost, srcImg, "img"])
            utilHigh.arrow.clickOnIt(isNext = True, delay = 0.3)

    print('\r')
    util.print.stringAndInt("Stories find : ", len(url_element))

    utilHigh.downloadList(url, url_element)

    nameProfile = getNameByUrl(url)
    category = "IGTV"
    moveFileToData(getNameByUrl(url), category)
    util.print.stringAndInt("FOLDER : ", str(os.getcwd())+"\\data\\profile\\"+nameProfile+"\\"+category+"\\"+util.getDateNow() )

    driver.close()
