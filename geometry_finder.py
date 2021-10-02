import os
import pprint

DIRECTORY = r"E:\assets\vegetation\AM171\abc"

class FindAssets(dict):
    def __init__(self, directory=DIRECTORY):
        print("Running FindAssets constructor")
        self.find_assets(directory)

    def find_assets(self, directory):
        assets = os.listdir(directory)
        for i in assets:
            if (i.endswith("abc") or i.endswith("fbx")
                                  or i.endswith("obj")
                                  or i.endswith("bgeo.sc")):
                info = {}
                name, ext = os.path.splitext(i)
                path = os.path.join(directory, i)

                info["path"] = path
                info["name"] = name
                info["type"] = ext

                self[name] = info

    # def check(self):
    #     pprint.pprint(self)
    #     # print(self)


if __name__ == "__main__":
    FindAssets().find_assets()
