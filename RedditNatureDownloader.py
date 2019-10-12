import urllib
import os
import time
import json
import praw

def run_downloader():
    instance = create_instance()
    config = load_config()
    subreddit = instance.subreddit("earthporn")
    if not (os.path.isdir(config['Path'])):
        os.mkdir(config['Path'])
    while (True):
        for id,post in enumerate(subreddit.hot(limit=config['Top Posts'])):
            print(id,post)
            output_file = config['Path']+'//'+post.id+'.jpg'
            if not os.path.isfile(output_file):
                urllib.request.urlretrieve(post.url,output_file)
        time.sleep(config['Update time'])

def create_instance():
    try:
        with open('data.json','r') as data:
            json_data = json.load(data)

        try:
            secret = json_data["secret"]
            client_id = json_data["client_id"]
            user_agent = json_data["user_agent"]
        except:
            print("Error fetching client data")
            exit()
    except FileNotFoundError:
        print("data.json file missing.")
        exit()

    try:
        instance = praw.Reddit(client_id=client_id,user_agent=user_agent,client_secret=secret)
        return instance
    except praw.exceptions.ClientException:
        print("Client side error, make sure API information is correct")
    except praw.exceptions.APIException:
        print("Server side exception with PRAW, try again later")

def load_config():
    try:
        with open('config.json','r') as config:
            json_config = json.load(config)

            try:
                folder_path = json_config["Path"]
            except KeyError:
                folder_path = "pictures"
            try:
                update_time = json_config["Update time"]
                if update_time < 120:
                    update_time = 600
                    print("Minimum update timer must be at least 2 minutes, continuing with 10 minute updates")
            except KeyError:
                update_time = 600
            try:
                top_post_count = json_config["Top Posts"]
                if  0 < top_post_count > 100:
                    top_post_count = 20
                    print("Top posts must be > 0 and < 100, continuing with top 20 posts")
            except KeyError:
                top_post_count = 20

            return {'Path':folder_path,'Update time':update_time,'Top Posts':top_post_count}

    except FileNotFoundError:
        config = {'Path':'pictures','Update time':600,'Top Posts':20}
        with open('config.json','w') as outputfile:
            json.dump(config,outputfile)
            print("config.json missing, new config created")
        return config

if __name__ == "__main__":
    run_downloader()



