# plan:
# get list of n64 games
#go through list. if game has achievements and is not a ~hack, create json file.
#go through json files. remove unimportant information, add image information.

import json
import urllib.request
import os.path
import os
import glob
import shutil
import copy

user = input("Please enter your retroachievements user name: ")
api = input("Please enter your retroachievements API key: ")
game_list_url = "https://ra.hfc-essentials.com/game_list.php?user=" + user + "&key=" + api + "&console=2&mode=json"
game_achievements_url = "https://ra.hfc-essentials.com/game_info_extended.php?user=" + user + "&key=" + api + "&game="
json_mode= "&mode=json"
file_path = "/N64_achievements_cache/"
new_file_path = "/N64_all_achievements/"


def get_games():
    urllib.request.urlretrieve(game_list_url, "game_list.json") 
    with open ("game_list.json", "r") as file:
            lines = file.readlines()

        
    with open("game_list.json", "w") as file:

        for line in lines:
            if line == "		[\n" or line == "		]\n":
                pass
            else:
                file.write(line)

def get_achievements():
    a=0
    list = []

    with open("game_list.json", "r") as file:
        data = json.load(file)        
    if not os.path.exists(os.path.abspath(os.getcwd() + file_path)):
        os.makedirs(os.path.abspath(os.getcwd() + file_path))
    print("Loading " + str(len(data["game"])) + " entries. This will take a few minutes:")
    for i in data["game"]:
        
   # for testing with local files:     
   # for filename in os.listdir(os.path.abspath(os.getcwd()) + "/N64_achievements_cache - Kopie"):
   #     with open(os.path.abspath(os.getcwd() + "/N64_achievements_cache - Kopie/" + filename), "r") as file:
   #         achievements = json.load(file)
        
        with urllib.request.urlopen(game_achievements_url + i["ID"] + json_mode) as ach_list:
            achievements = json.loads(ach_list.read().decode())
         
        if achievements["Achievements"] is not None and "~" not in achievements["Title"]:
            list.append(achievements)    
        a+=1
        print("Reading: " + str(a) + "/" + str(len(data["game"])))
    
    return list
        
def remove_header(json_file2):
    json_file = copy.deepcopy(json_file2)
    json_file.pop("ID")
    json_file.pop("Title")
    json_file.pop("ConsoleID")    
    json_file.pop("ForumTopicID")
    json_file.pop("Flags")
    json_file.pop("ImageIcon")
    json_file.pop("ImageTitle")    
    json_file.pop("ImageIngame")
    json_file.pop("ImageBoxArt")    
    json_file.pop("Publisher")    
    json_file.pop("Developer")    
    json_file.pop("Genre")    
    json_file.pop("Released")    
    json_file.pop("IsFinal")    
    json_file.pop("ConsoleName")    
    json_file.pop("RichPresencePatch")    
    json_file.pop("NumAchievements")    
    json_file.pop("NumDistinctPlayersCasual")    
    json_file.pop("NumDistinctPlayersHardcore")    
    
    return json_file
                
def adjust_achievements(json_file2, crc):
    json_file = copy.deepcopy(json_file2)

    for entry in json_file["Achievements"]:
        
        json_file["Achievements"][entry]["release_per_platform_id"] = "n64_" + crc
        json_file["Achievements"][entry].pop("NumAwarded")
        json_file["Achievements"][entry].pop("NumAwardedHardcore")
        json_file["Achievements"][entry]["name"] = json_file["Achievements"][entry].pop("Title")
        json_file["Achievements"][entry]["description"] = json_file["Achievements"][entry].pop("Description")
        json_file["Achievements"][entry]["api_key"] = json_file["Achievements"][entry].pop("ID")
        json_file["Achievements"][entry].pop("Points")
        json_file["Achievements"][entry].pop("TrueRatio")
        json_file["Achievements"][entry].pop("Author")
        json_file["Achievements"][entry].pop("DateModified")
        json_file["Achievements"][entry].pop("DateCreated")
        json_file["Achievements"][entry]["image_url_unlocked"] = "https://s3-eu-west-1.amazonaws.com/i.retroachievements.org/Badge/" + json_file["Achievements"][entry]["BadgeName"] + ".png"
        json_file["Achievements"][entry]["image_url_locked"] = "https://s3-eu-west-1.amazonaws.com/i.retroachievements.org/Badge/" + json_file["Achievements"][entry]["BadgeName"] + "_lock.png"
        json_file["Achievements"][entry].pop("BadgeName")
        json_file["Achievements"][entry].pop("DisplayOrder")
        json_file["Achievements"][entry].pop("MemAddr")
        
    with open(os.path.abspath(os.getcwd()) + "/N64_achievements_cache/" + crc + ".json", "w+") as file:  
        json.dump(json_file, file)

                
def multiply_file(json_file):
    with open ("ListOfCRC_AchievementGames.json", "r") as file:
        CRC_List = json.load(file)        
    
    for title in CRC_List["Games"]:        

        if json_file["Title"] == title["Title"]:
            for crc in title["CRC"]:
                e = remove_header(json_file)
                adjust_achievements(e, crc)
                    
    
            
def change_files():
    get_games()
    list = get_achievements()
    for entry in list:
        multiply_file(entry)
        
change_files()

    




    
