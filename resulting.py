import VkAgent
import OkAgent
import Ya
import requests
import os
import json
import Token
import Ya
import Agent
import hashlib
from pprint import pprint

if __name__ == '__main__':
    FILE_DIR1 = "Vladimir"
    PATH_DIR1 = os.path.join(os.getcwd(), FILE_DIR1)
    vladimir = VkAgent(Token.TOKEN_VK, "9958238")
    pprint(vladimir.photos_info())
    vladimir.files_downloader(FILE_DIR1)
    michel_load = Ya.YaUploader(Token.TOKEN_YA)
    michel_load.upload(PATH_DIR1)

    FILE_DIR = "Евгений"
    ok1 = OkAgent("542417581551")
    ok1.files_downloader(FILE_DIR)
    PATH_DIR = os.path.join(os.getcwd(), FILE_DIR)
    ok1_load = Ya.YaUploader(Token.TOKEN_YA)
    ok1_load.upload(PATH_DIR)