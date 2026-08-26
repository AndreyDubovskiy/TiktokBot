PATH_SAVED = "saved/"
import os
import pickle

#LIST_POSTS = {}
# {"name":{"text": str,
#          "urls": [str],
#          "photos": [str],
#           "videos": [str]
#          }}

def preload_config():
    if os.path.exists("save.bin"):
        read_ini()
    else:
        write_ini()

def write_ini(LIST_POSTS):
    config = {}
    config["LIST_POSTS"] = LIST_POSTS
    with open('save.bin', 'wb') as configfile:
        pickle.dump(config, configfile)

def read_ini():
    LIST_POSTS = None
    with open('save.bin', 'rb') as configfile:
        config = pickle.load(configfile)
        LIST_POSTS = config.get("LIST_POSTS", None)
    return LIST_POSTS

def get_ini():
    if os.path.exists("save.bin"):
        return read_ini()
    else:
        write_ini({})
        return read_ini()



class SaveManager:
    def get_list_posts(self):
        return get_ini()

    def save_list_posts(self, LIST_POSTS):
        write_ini(LIST_POSTS)



static_save_manager = SaveManager()