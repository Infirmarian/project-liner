# © Robert Geil 2018
import os
import comutils
import re

def get_lines_from_file(path):
    # no lines if the path doesn't exist or is not a file
    if not os.path.exists(path) or not os.path.isfile(path):
        return 0
    lcount = 0
    with open(path, "r") as f:
        for _ in f:
            lcount += 1
    return lcount


# Returns if a file is hidden (eg begins with a .)
def is_hidden(path):
    return os.path.split(path)[1][0] == "." 

def parse_gitignore(path):
    ignore = {
        "dir":[]
    }
    files = []
    with open(path, "r") as f:
        for line in f:
            if line == "\n":
                continue
            # Find if the line terminates
            count = line.find("#")
            line = line.strip("\n")
            if count > 0 or count == -1:
                if line[0] == "/" or line[-1]=="/":
                    ignore["dir"].append(line.strip("/"))
                else:
                    x=(line.strip("\n").replace(".", "\.").replace("*", ".*"))
                    files.append(x)
    exp = re.compile("|".join(files))
    ignore["files"] = exp
    return ignore
            


def get_all_files(path, use_gitignore, gitignore=None):
    # In the case that a non-existant path is passed, return an empty list
    if not os.path.exists(path):
        return []
    files = []
    if os.path.isdir(path) and not is_hidden(path):
        subdirs = os.listdir(path)
        # Find a gitignore if it exists in the directory
        if ".gitignore" in subdirs and use_gitignore:
           gitignore = parse_gitignore(os.path.join(path, ".gitignore"))
        # This boolean is checked before comparing against the gitignore file
        hasg = gitignore is not None
        for filename in subdirs:
            subpath = os.path.join(path, filename)
            if os.path.isdir(subpath) and not (hasg and filename in gitignore["dir"]):
                files += get_all_files(os.path.join(path, filename), use_gitignore, gitignore=gitignore)
            elif os.path.isfile(subpath) and not (hasg and gitignore["files"].match(filename)):
                files.append(os.path.join(path, filename))
    
    if os.path.isfile(path) and (not use_gitignore or not gitignore["files"].match(filename)):
        return [path]

    return files

def get_code_frequency(path, gitignore = True):
    all_files = get_all_files(path, use_gitignore=gitignore)
    languages = {}
    for name in all_files:
        ftype = comutils.get_language(name)
        if ftype is not None:
            if ftype in languages:
                languages[ftype] += get_lines_from_file(name)
            else:
                languages[ftype] = get_lines_from_file(name)
    return languages
