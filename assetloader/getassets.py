'''
/*
 * getassets.py
 * 
 * by joseyose, Oct 2021
 *
 * Implementation of the FindAssets class which inherits from a dict, so the 
 * data returned when calling the function is a dictionary. It will contain 
 * the name of the asset including the extension and the path where it's found.
 *
 * This will raise an exception if the directory provided by the user does 
 * not exist.
 *
 */
'''

import os
import sys

class FindAssets(dict):
    """This class handles the finding of assets in the user provided path"""
    def __init__(self, directory):
        """inits FindAssets"""
        self.find_assets(directory)

    def find_assets(self, directory):
        """Finds any asset in the provided directory.

        Args:
            directory ([str]): A path to a directory to look in

        Raises:
            Exception: If the directory provided does not exist
        """

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

                    name = i
                    
                    info["path"] = path
                    info["fullname"] = name
                    info["type"] = ext

                    self[name] = info
        else:
            raise Exception(f"{directory} does not exist!")

def main():
    """Handles the main logic for launching this file directly"""
    count = len(sys.argv)
    if count > 1:
        directory = sys.argv[1]
        FindAssets(directory=directory)
    else:
        sys.stderr.write("Usage: python3 ./getassets.py directory")


if __name__ == "__main__":
    main()