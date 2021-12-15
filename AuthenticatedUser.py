#!/usr/bin/python3

import requests
import json
from Utils import Config

class User:
    def __init__(self) -> None:
         # Parsed from github responses
        self.login = ""
        self.subscriptions_url = ""
        self.organizations_url = ""
        self.repos_url = ""

    def from_json(self, json_content):
        self.subscriptions_url = json_content["subscriptions_url"]
        self.organizations_url = json_content["organizations_url"]
        self.repos_url = json_content["repos_url"]
        self.login = json_content["login"]

    def to_json(self) :
        return json.dumps(self.__dict__)

class AuthenticatedUser(User) :
    def __init__(self, username : str, pat : str) -> None:
        super().__init__()
        self.login = username
        self.pat = pat
        self.publicname = ""
        self.bio =""
        self.private_repos_count = 0
        self.public_repos_count = 0

    def fetch(self) -> None:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token {}".format(self.pat)
        }
        response = requests.get("https://api.github.com/user", headers=headers)
        if response.status_code >= 400:
            print("Caught an error while fetching the authenticated user data")
            print("Status code was : {}".format(response.status_code))
            print("Error message was : {}".format(response.text))
        else :
            json_content = response.json()
            super().from_json(json_content)
            self.publicname = json_content["name"]
            self.bio = json_content["bio"]
            self.public_repos_count = json_content["public_repos"]
            self.private_repos_count = json_content["total_private_repos"]

    def to_json(self, indent : int = 0) :
        return json.dumps(self.__dict__, indent=indent)

    def get_authorization_header(self) -> dict :
        return {"Authorization": "token {}".format(self.pat)}


if __name__ == "__main__" :
    config = Config()
    if not config.read_from_file("config.json") :
        exit(1)

    user = AuthenticatedUser(config.username, config.pat)
    user.fetch()
    with open("TestsResults/authenticated_user.json", "w") as file :
        file.write(user.to_json(indent=4))