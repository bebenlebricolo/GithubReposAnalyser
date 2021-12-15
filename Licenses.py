
import json


class License:
    def __init__(self) -> None:
        self.key = ""
        self.name=""
        self.spdx_id=""
        self.url=""
        self.node_id=""

    def from_json(self, json_content):
        self.key = json_content["key"]
        self.name = json_content["name"]
        self.spdx_id = json_content["spdx_id"]
        self.url = json_content["url"]
        self.node_id = json_content["node_id"]

    def to_json(self, indent : int = 0) -> str:
        return json.dumps(self.__dict__, indent=indent)