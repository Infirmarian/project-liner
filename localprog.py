# © Robert Geil 2018

import os

def get_lines_from_file(path):
    # no lines if the path doesn't exist or is not a file
    if not os.path.exists(path) or not os.path.isfile(path):
        return 0
    lcount = 0
    with open(path, "r") as f:
        for _ in f:
            lcount += 1
    return lcount

