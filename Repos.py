#!/usr/bin/python3
import requests
from AuthenticatedUser import AuthenticatedUser, User
from Licenses import License
from Utils import Config
import json

class Repository :
    def __init__(self) -> None:
        self.name=""
        self.url=""
        self.id=0
        self.private=False
        self.full_name=""
        self.description=""
        self.url=""
        self.license=None
        self.visibility="public"
        self.default_branch="main"
        self.owner=None

    def to_json(self, indent : int = 0) -> str:
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=indent)

def get_repos_for_auth_user(user : AuthenticatedUser) -> list[Repository] :
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization" : user.get_authorization_header()["Authorization"]
    }
    response = requests.get("https://api.github.com/user/repos", headers=headers)

    repos = []
    if response.status_code >= 400:
        print("Caught an error while listing repositories for the authenticated user")
        print("Status code was : {}".format(response.status_code))
        print("Error message was : {}".format(response.text))
    else :
        json_content = response.json()
        for fetched_repo in json_content :
            repo = Repository()
            repo.name = fetched_repo["name"]
            repo.id = fetched_repo["id"]
            repo.full_name = fetched_repo["full_name"]
            repo.private = fetched_repo["private"]
            repo.url = fetched_repo["url"]

            repo.owner = User()
            repo.owner.from_json(fetched_repo["owner"])

            if fetched_repo["license"] is not None :
                repo.license = License()
                repo.license.from_json(fetched_repo["license"])
            repo.visibility = fetched_repo["visibility"]
            repo.default_branch = fetched_repo["default_branch"]

            repos.append(repo)
    return repos

if __name__ == "__main__" :
    config = Config()
    if not config.read_from_file("config.json"):
        exit(1)
    user = AuthenticatedUser(config.username, config.pat)
    user.fetch()
    repos = get_repos_for_auth_user(user)
    json_content = json.dumps(repos, default=lambda o: o.__dict__, indent=4)
    print(json_content)
    with open("TestsResults/repos_testing.json", "w") as file :
        file.write(json_content)

