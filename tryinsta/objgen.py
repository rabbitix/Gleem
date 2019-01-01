from constant import *
import instagram


class Comp(object):
    def __init__(self):
        self.values = ""

    def translate(self, token_type=None, operation=None, value=None):
        self.values += value + ' '
        return self.values

    def show_error(self, msgtxt=None):
        print("\033[33m============ ERROR ============\033[0m")
        print('\033[31m' + msgtxt)
        print("\033[33m===============================\033[0m")

    def compile(self, values):
        all_vals = []
        username = ""
        password = ""
        all_vals = values.split()
        # check that start of the file works well! and is what we want
        if all_vals[0] in KEYWORDS["UserIdentifier"] and \
                all_vals[2] in KEYWORDS["PasswordIdentifier"] and \
                all_vals[4] in KEYWORDS["StartIdentifier"]:
            # check for `user` keyword
            if all_vals[0] in KEYWORDS["UserIdentifier"]:
                username = all_vals[1]
            else:
                self.show_error("your syntax should start with init the user")
                quit()
            # check for `password` keyword
            if all_vals[2] in KEYWORDS["PasswordIdentifier"]:
                password = all_vals[3]
            else:
                self.show_error("after identifying user, you should pass the password! ")
                quit()
            # check for `start` keyword
            if all_vals[4] in KEYWORDS["StartIdentifier"]:
                print("should start here!")
                # igobj = instagram.IGram(username, password)
            else:
                self.show_error("can you ride a car without starting it?!")
                quit()
        else:
            self.show_error("you didnt use the correct structure for the start of the syntax")
            quit()
        index = 5
        while index < len(all_vals):
            if all_vals[index] in DATATYPE["likeLastPostIdentifier"]:
                print("should do like last post function ")
                # igobj.like_last_post(all_vals[index+1])
                index += 2

            elif all_vals[index] in DATATYPE["FollowIdentifier"]:
                print("should do follow function")
                index += 2
                # igobj.follow_user(all_vals[index+1])

            # if all_vals[index] in DATATYPE["LikeIdentifier"]:
            #     print(" should do liking function")

            else:
                index += 1
