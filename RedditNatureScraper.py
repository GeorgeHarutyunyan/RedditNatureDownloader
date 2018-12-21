from bs4 import BeautifulSoup
import urllib
import os
import time
import configparser
import json
import requests

def RedditNatureScraper():
    with open('data.json','r') as data:
        json_data = json.load(data)

    folder_path = json_data[0]["Path"]
    check_interval = json_data[0]["Interval"]
   # print(folder_path)
    #print(check_interval)

if __name__ == "__main__":
    RedditNatureScraper()



