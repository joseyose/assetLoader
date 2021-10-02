import os
import sys

class FindAssets(dict):
    def __init__(self, directory):
        self.find_assets(directory)

    def find_assets(self, directory):

        if os.path.isdir(directory):
            assets = os.listdir(directory)
            assets.sort()
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
        else:
            raise Exception(f"{directory} does not exist!")

if __name__ == "__main__":
    count = len(sys.argv)
    if count > 1:
        directory = sys.argv[1]
        FindAssets(directory=directory)
    else:
        sys.stderr.write("Usage: python3 ./geometry_finder.py directory")
