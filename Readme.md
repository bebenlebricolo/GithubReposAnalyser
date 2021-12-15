# Index
- [Index](#index)
- [Github Repos Analyser](#github-repos-analyser)
- [Authentication](#authentication)
- [Repositories listing for an authenticated user](#repositories-listing-for-an-authenticated-user)

# Github Repos Analyser
This repository was an attempt to use the Github rest api in order to fetch various data belonging to an user.
For instance, it can be used to fetch some information about a user, like the number of repositories, its contributions, listing all repositories and so on.

I wrote those pieces of code in the sole purpose to retrieve the traffic data from the repositories (because I thought it would be neat to geat traffic information of all repositories without having to manually check any individual repo).

# Authentication
Authentication is performed through the use of a personal access token, which should have been created before using this python tools.
For testing purposes, the configuration is held by a file called `config.json` at the same folder level as the other scripts and is fetched by the tests.
So to try it out for yourself, simply provide your own version of `config.json`.
An example is available under [Examples/config.json.example](Examples/config.json.example).

```json
{
    "username" : "nobody",
    "personal access token" : "blahblahblah"
}
```

# Repositories listing for an authenticated user
This is the test performed by the script `Repos.py`  when launched as a standalone script.
It first fetches the config from `config.json` and then sends few requests to Github rest api in order to list all the repositories linked to the authenticated user.
Data is then parsed and partial data is extracted from the received list.
The resulting data model is then written down into the `TestsResults` folder and looks like this :
```json
[
    {
        "name": "3D-printing",
        "url": "https://api.github.com/repos/bebenlebricolo/3D-printing",
        "id": xxxxx,
        "private": false,
        "full_name": "bebenlebricolo/3D-printing",
        "description": "",
        "license": null,
        "visibility": "public",
        "default_branch": "master",
        "owner": {
            "login": "bebenlebricolo",
            "subscriptions_url": "https://api.github.com/users/bebenlebricolo/subscriptions",
            "organizations_url": "https://api.github.com/users/bebenlebricolo/orgs",
            "repos_url": "https://api.github.com/users/bebenlebricolo/repos"
        }
    },
    {
        "name": "AvrAsyncCore",
        "url": "https://api.github.com/repos/bebenlebricolo/AvrAsyncCore",
        "id": xxxxxx,
        "private": false,
        "full_name": "bebenlebricolo/AvrAsyncCore",
        "description": "",
        "license": {
            "key": "gpl-3.0",
            "name": "GNU General Public License v3.0",
            "spdx_id": "GPL-3.0",
            "url": "https://api.github.com/licenses/gpl-3.0",
            "node_id": "MDc6TGljZW5zZTk="
        },
        "visibility": "public",
        "default_branch": "main",
        "owner": {
            "login": "bebenlebricolo",
            "subscriptions_url": "https://api.github.com/users/bebenlebricolo/subscriptions",
            "organizations_url": "https://api.github.com/users/bebenlebricolo/orgs",
            "repos_url": "https://api.github.com/users/bebenlebricolo/repos"
        }
    },
    ...
]
```