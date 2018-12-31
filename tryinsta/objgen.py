import constant

from InstagramAPI import InstagramAPI
import time


class IGram:
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
        # self.exe_string = ""
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
        if all[0] in constant.KEYWORDS["UserIdentifier"]:
            username = all[1]
        else:
            self.error("your syntax should start with init the user")
            quit()
        if all[2] in constant.KEYWORDS["PasswordIdentifier"]:
            password = all[3]
        else:
            self.error("after identifying user, you should pass the password! ")

        if all[4] in constant.KEYWORDS["StartIdentifier"]:
            obj = IGram(username, password)
        else:
            self.error("can you ride a car without starting it?!")

        index = 5
        while index < len(all):
            if all[index] == constant.DATATYPE[0] or all[index] == constant.DATATYPE[1]:
                print("should do like last post function ")
            if all[index] == 'FOLLOW':
                print("should do follow function")

            index += 1
        # target_username = ""

        # if all[5] is "like_last_post":
        # target_username = all[6]
        # obj.like_last_post(username=target_username)

        print('s')
