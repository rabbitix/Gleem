from InstagramAPI import InstagramAPI
import time
# import constant
# from objgen import Comp as x
# cc = x()

class IGram:  # class for instagram part
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
        try:
            self.ig.like(last_media_id)
        except:
            print("can not like last post. maybe its a private account!")
            #TODO add this error to log
            # constant.to_log(cc.main_log,"can not like last post. maybe its a private account!")

    def follow_user(self, username):
        self.ig.searchUsername(username)
        user_id = self.ig.LastJson['user']['pk']
        self.ig.follow(user_id)

    def unfollow_user(self, username):
        self.ig.searchUsername(username)
        user_id = self.ig.LastJson['user']['pk']
        self.ig.unfollow(user_id)
