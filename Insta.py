from insta.core.download.AllPost import main_download_allposts
from insta.core.download.Highlights import mainHigh
from insta.core.download.Story import mainStory


class Download():
    def post(self, url: str):
        main_download_allposts(url=url)
    def story(self, url: str):
        mainStory(url)
    def highlights(self, url: str):
        mainHigh(url=url)

class InstaClass():
    download = Download()
