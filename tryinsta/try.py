from InstagramAPI import InstagramAPI
import time


# def user(self, bot, update):
#     user = update.message.text
#     self.ig.searchUsername(user)
#     userid = self.ig.LastJson['user']['pk']
#     userPosts = self.ig.getTotalUserFeed(usernameId=userid)
#     self.lastmediaid = userPosts[0]['id']
#
#     # is_private = self.ig.LastJson['user']['is_private']
#     # if is_private:
#     #     bot.sendMessage(chat_id=update.message.chat_id, text="the account is private")
#     #     return ConversationHandler.END
#     # else:
#     # bot.sendMessage(update.message.chat_id,
#     #                 "ok.how many time you want to post that comment to last user post??[enter a number]")
#
#     def comment(self, bot, update):
#         comment = update.message.text
#         if self.count > 10:
#             for i in range(0, self.count):
#                 self.ig.comment(self.lastmediaid, comment)
#                 time.sleep(60)
#
#         self.ig.comment(self.lastmediaid, comment)

class IGram:
    def __init__(self, username = None, password=None):
        if username:
            self.ig = InstagramAPI(username, password)
            self.ig.login()
        else:
            pass

    def start(self):
        pass

    def like_last_post(self, username=None):
        self.ig.searchUsername(username)
        userid = self.ig.LastJson['user']['pk']
        userPosts = self.ig.getTotalUserFeed(usernameId=userid)
        lastmediaid = userPosts[0]['id']
        self.ig.like(lastmediaid)


def main():
    all = []
    txt = ''
    username = ""
    password = ""
    with open('syntax.gl', 'r') as source_code:
        for l in source_code.readlines():
            txt += str(l)

    all = txt.split()
    target_username = ""

    # if all[0] is "User":
    username = all[1]
    # if all[2] is "Password":
    password = all[3]
    # if all[4] is "Start":
    obj = IGram(username, password)
    # if all[5] is "like_last_post":
    target_username = all[6]
    obj.like_last_post(username=target_username)

    print('s')


main()