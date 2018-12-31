from constant import *

from InstagramAPI import InstagramAPI
import time


class IGram: # class for instagram part
    def __init__(self, username=None, password=None):
        if username:
            self.ig = InstagramAPI(username, password)
            self.ig.login()
        else:
            pass

    def start(self):
        pass

    def like_last_post(self, username=None):
        self.ig.searchUsername(username)
        user_id = self.ig.LastJson['user']['pk']
        user_posts = self.ig.getTotalUserFeed(usernameId=user_id)
        last_media_id = user_posts[0]['id']
        self.ig.like(last_media_id)


class Comp(object):
    def __init__(self):
        self.values = ""

    def translate(self, token_type=None, operation=None, value=None):
        self.values += value + ' '
        return self.values

    def error(self, msgtxt=None):
        print("============ ERROR ============")
        print(msgtxt)
        print("===============================")

    def compile(self, values):
        all = []
        username = ""
        password = ""
        all = values.split()
        # check that start of the file works well!


        if all[0] in KEYWORDS["UserIdentifier"]:
            username = all[1]
        else:
            self.error("your syntax should start with init the user")
            quit()

        if all[2] in KEYWORDS["PasswordIdentifier"]:
            password = all[3]
        else:
            self.error("after identifying user, you should pass the password! ")
            quit()

        if all[4] in KEYWORDS["StartIdentifier"]:
            obj = IGram(username, password)
        else:
            self.error("can you ride a car without starting it?!")
            quit()


        index = 5
        while index < len(all):
            if all[index] == DATATYPE[0] or all[index] == DATATYPE[1]:
                print("should do like last post function ")
            if all[index] == 'FOLLOW':
                print("should do follow function")

            index += 1
