from constant import *
import instagram
from random import randint


class Comp:
    def __init__(self):
        self.log_file = "def.txt"
        self.values = ""

    def translate(self, token_type=None, operation=None, value=None):
        self.values += value + ' '
        return self.values

    def show_error(self, msgtxt=None):
        print("\033[33m============ ERROR ============\033[0m")
        print('\033[31m' + msgtxt)
        print("\033[33m===============================\033[0m")

    main_log = ""
    def compile(self, values):

        all_vals = []
        username = ""
        password = ""
        all_vals = values.split()
        # check that start of the file works well! and is what we want
        if all_vals[2] in KEYWORDS["UserIdentifier"] and \
                all_vals[4] in KEYWORDS["PasswordIdentifier"] and \
                all_vals[0] in KEYWORDS["StartIdentifier"]:
            # check for `user` keyword
            if all_vals[2] in KEYWORDS["UserIdentifier"]:
                username = all_vals[3]
            else:
                self.show_error("your syntax should start with init the user")
                quit()
            # check for `password` keyword
            if all_vals[4] in KEYWORDS["PasswordIdentifier"]:
                password = all_vals[5]
            else:
                self.show_error("after identifying user, you should pass the password! ")
                quit()
            # check for `start` keyword
            if all_vals[0] in KEYWORDS["StartIdentifier"]:
                print("should start here!")
                self.log_file = str(all_vals[1]) + ".txt"
                main_log = str(all_vals[1]) + ".txt"

                igobj = instagram.IGram(username, password)
            else:
                self.show_error("can you ride a car without starting it?!")
                quit()
        else:
            self.show_error("you didnt use the correct structure for the start of the syntax")
            quit()
        index = 6

        to_log(self.log_file, "started new session")
        to_log(self.log_file, "user name: {0}".format(username))
        to_log(self.log_file, "password: {0}".format(password))
        to_log(self.log_file, "started")

        # After pass first of syntax
        while index < len(all_vals):
            if all_vals[index] in DATATYPE["likeLastPostIdentifier"]:
                igobj.like_last_post(all_vals[index + 1])
                to_log(self.log_file, "Liking last post of {0}".format(all_vals[index + 1]))
                index += 2

            elif all_vals[index] in DATATYPE["FollowIdentifier"]:
                # print("should do follow function")
                to_log(self.log_file, "Following user {0}".format(all_vals[index + 1]))
                igobj.follow_user(all_vals[index + 1])
                time.sleep(randint(1.2, 6.5))
                index += 2
            elif all_vals[index] in DATATYPE["UnFollowIdentifier"]:
                # print("should do unfollow function")
                to_log(self.log_file, "Unfollow user {0}".format(all_vals[index + 1]))
                igobj.unfollow_user(all_vals[index + 1])
                time.sleep(randint(1, 6))
                index += 2

            # if all_vals[index] in DATATYPE["LikeIdentifier"]:
            #     print(" should do liking function")

            else:
                index += 1
