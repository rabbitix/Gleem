from constant import *
import instagram


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
        # check that start of the file works well! and is what we want
        if all[0] in KEYWORDS["UserIdentifier"] and \
                all[2] in KEYWORDS["PasswordIdentifier"] and\
                all[4] in KEYWORDS["StartIdentifier"]:
            # check for `user` keyword
            if all[0] in KEYWORDS["UserIdentifier"]:
                username = all[1]
            else:
                self.error("your syntax should start with init the user")
                quit()
            # check for `password` keyword
            if all[2] in KEYWORDS["PasswordIdentifier"]:
                password = all[3]
            else:
                self.error("after identifying user, you should pass the password! ")
                quit()
            # check for `start` keyword
            if all[4] in KEYWORDS["StartIdentifier"]:
                igobj = instagram.IGram(username, password)
            else:
                self.error("can you ride a car without starting it?!")
                quit()

        index = 5
        while index < len(all):
            if all[index] in DATATYPE["likeLastPostIdentifier"]:
                print("should do like last post function ")
            if all[index] in DATATYPE["FollowIdentifier"]:
                print("should do follow function")
            if all[index] in DATATYPE["LikeIdentifier"]:
                print(" should do liking function")

            index += 1
