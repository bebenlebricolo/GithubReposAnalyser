#!/usr/bin/python

from Traffic import Traffic, TimePeriod
from AuthenticatedUser import AuthenticatedUser
from Utils import Config
from Repos import Repository, get_repos_for_auth_user
import requests
import json

def main() :
    config = Config()
    if not config.read_from_file("config.json"):
        exit(1)
    user = AuthenticatedUser(config.username, config.pat)
    user.fetch()
    repos = get_repos_for_auth_user(user)

    traffic_list=[]
    for repo in repos :
        traffic = Traffic(TimePeriod.Day)
        result = traffic.fetch(user, repo.name)
        if result :
            traffic_list.append({"repo" : repo.name, "traffic" : traffic.to_dict()})

    json_content = json.dumps(traffic_list, indent=4)
    print(json_content)
    with open("TestsResults/full_traffic.json", "w") as file :
        file.write(json_content)


if __name__ == "__main__" :
    main()

