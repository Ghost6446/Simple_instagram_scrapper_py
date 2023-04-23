from Insta import InstaClass

username = "xxxxxxxx"
urlProfile = f"https://www.instagram.com/{username}/"
numberPost = 5
hashtag_list = ['sun']
pageScoll = 7
delaySwitchImage = 6
delayFolloweMin = 20
delayFolloweMax = 30
MaxLike = 999
MaxFollower = 999

insta = InstaClass()
insta.download.story(url=urlProfile)


    
