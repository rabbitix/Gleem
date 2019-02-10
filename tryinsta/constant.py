import time

KEYWORDS = {
    "UserIdentifier": ["User", "user"],
    "PasswordIdentifier": ["Password", "password"],
    "StartIdentifier": ["Start", "start"],
}

DATATYPE = {
    "likeLastPostIdentifier": ["LikeLastPost", "like_last_post"],
    "FollowIdentifier": ["Follow","follow"],
    "UnFollowIdentifier": ["Unfollow","unfollow"],
    "LikeIdentifier": ["Like"],
}

# this list is spacially made for lexer file
key_words = ["User", "user",
             "Password", "password",
             "Start", "start"]

data_type = ["LikeLastPost", "like_last_post",
             "Follow","follow",
             "Unfollow","unfollow",
             "Like"]


# TODO make it non case sensetive

#TODO IDEA:
# follow from a list of ppl in file!


def to_log(file, text):
    tt = time.localtime(time.time())
    now = "[{0}/{1}/{2} {3}:{4}:{5}] > ".format(tt.tm_year, tt.tm_mon, tt.tm_wday, tt.tm_hour, tt.tm_min, tt.tm_sec)
    with open(file, "a") as log:
        log.write(str(now) + str(text) + '\n')
