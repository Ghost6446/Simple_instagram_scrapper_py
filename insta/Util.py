# 3/07/2022 - 6/07/2022

# General import
import os, shutil, yaml
from datetime import datetime, date


class colors:

    reset='\033[0m'
    bold='\033[01m'

    class fg:

        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'

class Print():

    def getTimeNow(self):
        return datetime.now().strftime("%H:%M:%S")

    def getDateNow(self):
        return str(date.today().strftime("%d/%m/%Y")).replace("/" , '.')

    def stringTime(self):
        return colors.fg.lightblue + "INFO  " + colors.fg.yellow + "[ " + colors.fg.green + self.getTimeNow() + colors.fg.yellow + " ]"

    def string(self, string, end=False):
        if end:
            print(self.stringTime() + colors.fg.blue + "   -->   " + colors.fg.yellow + string + colors.reset, end="\r")
        else:
            print(self.stringTime() + colors.fg.blue + "   -->   " + colors.fg.yellow + string + colors.reset)

    def stringAndInt(self, string, intCounter, end=False):
        if end:
            print(self.stringTime() + colors.fg.blue + "   -->   " +  string + colors.fg.yellow +" [" + colors.fg.red , intCounter , colors.fg.yellow +"]" + colors.reset, end="\r")
        else:
            print(self.stringTime() + colors.fg.blue + "   -->   " +  string + colors.fg.yellow +" [" + colors.fg.red , intCounter , colors.fg.yellow +"]" + colors.reset)

    def TwostringAndInt(self, string, intCounter, string_2, intCounter_2, end=False):
        if end:
            print(self.stringTime() + colors.fg.blue + "   -->   " +  string + colors.fg.red , intCounter , colors.fg.blue + string_2 + colors.fg.red , intCounter_2 , colors.fg.green, colors.reset, end="\r")
        else:
            print(self.stringTime() + colors.fg.blue + "   -->   " +  string + colors.fg.red , intCounter , colors.fg.blue + string_2 + colors.fg.red , intCounter_2 , colors.fg.green, colors.reset)

    def ThreeStringAndInt(self, string, counter, string_2, counter_2, string_3, counter_3, end=False):
        if end:
            print(self.stringTime() + colors.fg.blue + "   -->   " +  string + colors.fg.red , counter , colors.fg.green + "; " + colors.fg.blue + string_2 + colors.fg.red , counter_2 , colors.fg.green + "; " + colors.fg.blue + string_3 + colors.fg.red , counter_3, colors.reset, end="\r")
        else:
            print(self.stringTime() + colors.fg.blue + "   -->   " +  string + colors.fg.red , counter , colors.fg.green + "; " + colors.fg.blue + string_2 + colors.fg.red , counter_2 , colors.fg.green + "; " + colors.fg.blue + string_3 + colors.fg.red , counter_3, colors.reset)

    def Matrix(self, matrix):
        s = self.stringTime() + colors.fg.blue + "   -->   " + colors.fg.yellow

        for i in range(len(matrix)):
            s += colors.fg.blue + matrix[i][0] + colors.fg.yellow +  " [ " + colors.fg.lightred + matrix[i][1] + colors.fg.yellow + " ]; " + "\n"

        print(s + colors.reset)

    def List(self, s, list):
    
        s = self.stringTime() + colors.fg.blue + "   -->   " + colors.fg.yellow + s  + " : <<" 

        for i in range(0,len(list)):
            s += colors.fg.yellow +  " [ " + colors.fg.lightred + list[i] + colors.fg.yellow + " ],"

        print(s + " >>" + colors.reset)

class Util():

    print = Print()
    
    def getTimeNow(self):
        return datetime.now().strftime("%H:%M:%S")

    def getDateNow(self):
        return str(date.today().strftime("%d/%m/%Y")).replace("/" , '.')
    
util = Util()
with open('.\\insta\\path\\Selector.yaml') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

def removeFile(pathFile):
    if os.path.exists(pathFile):
        os.remove(pathFile)

def getNameByUrl(url):
    return str(url).split("www.instagram.com")[1].replace("/", "")

def createFolder(url):
    os.makedirs(getNameByUrl(url),exist_ok=True)

def getAllFileInAFolder(path):
    return os.listdir(path)
    
def createFolderSimple(name):
    os.makedirs(name,exist_ok=True)

def createArchive(url, format):
    shutil.make_archive(getNameByUrl(url), format, getNameByUrl(url))
    shutil.copy2(getNameByUrl(url)+"."+format , ".\\data\\profile\\"+getNameByUrl(url)+"_"+util.getDateNow()+"."+format)
    shutil.rmtree('.\\'+getNameByUrl(url))
    os.remove(getNameByUrl(url)+"."+format)

def moveFileToData(nameTempFolder, nameCategory):

    util.print.string("Move content from temp to data")
    sourcePath = nameTempFolder
    destPath = r".\\data\\profile\\"+nameTempFolder+"\\"+nameCategory+"\\"+util.getDateNow()
    os.makedirs(destPath,exist_ok=True)
    for element in os.listdir(sourcePath):
        shutil.move(sourcePath+"\\"+element,destPath+"\\"+element)
    shutil.rmtree(sourcePath, ignore_errors=True)
