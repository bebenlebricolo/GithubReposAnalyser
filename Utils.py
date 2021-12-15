import json
import os.path

class Config :
    def __init__(self) -> None:
        self.username=""
        self.pat=""
        self.test_repo=""

    def read_from_file(self, filepath : str) -> bool :
        try :
            if os.path.exists(filepath) :
                with open(filepath, 'r') as file :
                    json_content = json.load(file)
                    self.username = json_content["username"]
                    self.pat = json_content["personal access token"]
                    self.test_repo = json_content["test repo"]

        except Exception as error :
            print(error)
            return False
        return True


if __name__ == "__main__" :
    config = Config()
    exit(config.read_from_file("config.json") != True)