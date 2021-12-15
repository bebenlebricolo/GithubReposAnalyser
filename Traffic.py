#!/usr/bin/python3

from enum import Enum
from typing import AbstractSet
from AuthenticatedUser import AuthenticatedUser
from Repos import Repository
import requests
import json
from Utils import Config


class TimePeriod(Enum):
    Day = "day"
    Week = "week"

class Clone :
    def __init__(self) -> None:
        self.timestamp = ""
        self.count = 0
        self.uniques = 0

    def from_json(self, json_content : dict) -> bool :
        try :
            self.timestamp = json_content["timestamp"]
            self.count = json_content["count"]
            self.uniques = json_content["uniques"]
        except Exception as error :
            print("Caugt error while reading clones from parsed content")
            print(error)
            return False
        return True

class Traffic :
    def __init__(self, timeperiod : TimePeriod) -> None:
        self.count = 0
        self.uniques = 0
        self.clones = list()
        self.timeperiod = timeperiod

    def fetch(self, user : AuthenticatedUser, reponame : str) -> bool :
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization" : user.get_authorization_header()["Authorization"]
        }
        url = "https://api.github.com/repos/{}/{}/traffic/clones?per={}".format(user.login, reponame, self.timeperiod.value)
        response = requests.get(url, headers=headers)

        if response.status_code >= 400:
            print("Caught an error while listing repositories for the authenticated user")
            print("Status code was : {}".format(response.status_code))
            print("Error message was : {}".format(response.text))
        else :
            json_content = response.json()
            self.count = json_content["count"]
            self.count = json_content["uniques"]
            for fetched_clone in json_content["clones"] :
                clone = Clone()
                if not clone.from_json(fetched_clone):
                    return False
                self.clones.append(clone)
        return True

    def to_dict(self) -> dict :
        clones_dict=[]
        for clone in self.clones :
            clones_dict.append(clone.__dict__)
        thisdict = {
            "count" : self.count,
            "uniques" : self.uniques,
            "clones" : clones_dict,
            "timeperiod" : self.timeperiod.value
        }
        return thisdict

    def to_json(self, indent=0) -> str :
        return json.dumps(self.to_dict(), indent=indent)

if __name__ == "__main__" :
    config = Config()
    if not config.read_from_file("config.json"):
        exit(1)
    user = AuthenticatedUser(config.username, config.pat)
    user.fetch()
    traffic = Traffic(TimePeriod.Day)
    result = traffic.fetch(user, config.test_repo)

    json_content = traffic.to_json(indent=4)
    print(json_content)
    with open("TestsResults/traffic_testing.json", "w") as file :
        file.write(json_content)
