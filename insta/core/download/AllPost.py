# 10-07-2022 -> 20-07-2022

import time, requests, urllib.request, json, os, sys
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from insta.Driver import driver
from insta.Util import getNameByUrl, createFolderSimple, moveFileToData
from insta.Util import util
from insta.Util import data as path

MAX_WORKERS = 250
class_img_post = path['Download']['allpost']['url_post']['class']

class ParseJson():

    def convertRequestToUrl(self, requestUrl):
        return str(requests.utils.unquote(requestUrl))

    def extractData(self, data, isFirstApi):
        if(not isFirstApi):
            radice = data['data']['user']['edge_owner_to_timeline_media']['edges']

        if(isFirstApi):
            radice = data['graphql']['user']['edge_owner_to_timeline_media']['edges']


        multi_post = []

        for i in range(len(radice)):
            post = []
            try:
                if(radice[i]['node']['is_video']):
                    url = radice[i]['node']['video_url']
                    name = str(radice[i]['node']['display_url']).split("?")[0].split("/")[-1]
                    post.append([url, name, "mp4"])

                else:
                    url = radice[i]['node']['display_url']
                    name = str(radice[i]['node']['display_url']).split("?")[0].split("/")[-1]
                    post.append([url, name, "jpg"])
            except:
                pass

            try:
                for x in range(len(radice[i]['node']['edge_sidecar_to_children']['edges'])):
                    if ( radice[i]['node']['edge_sidecar_to_children']['edges'][x]['node']['is_video'] ):
                        url = radice[i]['node']['edge_sidecar_to_children']['edges'][x]['node']['video_url']
                        name = str(radice[i]['node']['edge_sidecar_to_children']['edges'][x]['node']['video_url']).split("?")[0].split("/")[-1]
                        post.append([url, name, "mp4"])
                    else:
                        url = radice[i]['node']['edge_sidecar_to_children']['edges'][x]['node']['display_url']
                        name = str(radice[i]['node']['edge_sidecar_to_children']['edges'][x]['node']['display_url']).split("?")[0].split("/")[-1]
                        post.append([url, name, "jpg"])
            except:
                pass

            multi_post.append(post)
        return multi_post

class UtilAllPost():

    parseJson = ParseJson()

    def downloadElement(self, url, folder, name):
        urllib.request.urlretrieve(url, folder+"//"+name)

    def generateHashUrl(self, query_hash, query_profileid, query_first, query_endCursor):
        url =  f'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables=["id":"{query_profileid}","first":{query_first},"after":"{query_endCursor}"]'.replace("[", "{").replace("]", "}")
        return self.parseJson.convertRequestToUrl(url)

    def dumpProfile(self, username):
        driver.get(f"https://www.instagram.com/{username}/?__a=1&__d=dis")
        soup = BeautifulSoup(driver.page_source, "lxml")
        data = json.loads(soup.text)
        endCursor = data['graphql']['user']['edge_felix_video_timeline']['page_info']['end_cursor']
        id = data['graphql']['user']['id']
        return data, id, endCursor
    
utilPost = UtilAllPost()

def main_download_allposts(url):
    
    allMedia = []
    name_by_url = getNameByUrl(url)
    data, query_profileid, query_endCursor = utilPost.dumpProfile(name_by_url)
    isPrivate = data['graphql']['user']['is_private']
    pathFolder = ".\\"+name_by_url+"\\"

    if(isPrivate):
        util.print.string("CANT GET IMAGE")
        driver.close()
        sys.exit(0)

    createFolderSimple(name_by_url)
    query_hash = "69cba40317214236af40e7efa697781d"
    query_first = 30

    urlNextHash = utilPost.generateHashUrl(query_hash, query_profileid, query_first, query_endCursor)
    driver.get(urlNextHash )

    list_hash_media = []
    endCursor = "xx"

    while ( endCursor != "" ):
        soupPage = BeautifulSoup(str(driver.page_source), "lxml").text
        jsonData = json.loads(soupPage)
        endCursor = jsonData["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
        urlNextHash = utilPost.generateHashUrl(query_hash, query_profileid, query_first, endCursor)
        for scrape_url in utilPost.parseJson.extractData(jsonData, isFirstApi=False):
            list_hash_media.append(scrape_url)
        driver.get(urlNextHash)
        util.print.stringAndInt("CURSOR ", endCursor, end=True)
    print("\r")


    dataPost = utilPost.parseJson.extractData(data, isFirstApi=True)
    list_dump_media = []
    for i in range(len(dataPost)):
        post_n = dataPost[i]
        for e in post_n:
            list_dump_media.append(e)

    for post in list_hash_media:
        for media in post:
            allMedia.append(media)

    for media in list_dump_media:
        allMedia.append(media)

    util.print.stringAndInt("DOWNLOAD", len(allMedia))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i in range(len(allMedia)):
            url = allMedia[i][0]
            name = allMedia[i][1]
            type = allMedia[i][2]
            if type == "mp4" and "mp4" not in name:
                name = str(name).replace("jpg", "mp4")
            executor.submit(utilPost.downloadElement, url, pathFolder, name)

    moveFileToData(name_by_url, "POST")
    util.print.stringAndInt("FOLDER : ", str(os.getcwd())+"\\data\\profile\\"+name_by_url+"\\POST\\"+ util.getDateNow() )
    driver.close()
