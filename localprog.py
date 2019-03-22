# © Robert Geil 2018
import os
import comutils
import subprocess

def get_lines_from_file(path):
    # no lines if the path doesn't exist or is not a file
    if not os.path.exists(path) or not os.path.isfile(path):
        return 0
    lcount = 0
    with open(path, "r") as f:
        for _ in f:
            lcount += 1
    return lcount

def get_git_tracked_files(path):
    try:
        process = subprocess.check_output(["./sample.sh {}".format(path)], shell=True)
        x = process.decode().split("\n")[1:]
        x.remove("")
        for i in range(0, len(x)):
            x[i] = os.path.join(path, x[i])
        return (x)
    except Exception as e:
        print("Error, likely that git repository doesn't exist")
        print(e)
        return []


# Returns if a file is hidden (eg begins with a .)
def is_hidden(path):
    return os.path.split(path)[1][0] == "." 


def get_all_files(path, use_gitignore=False):
    # In the case that a non-existant path is passed, return an empty list
    if not os.path.exists(path):
        return []
    if use_gitignore:
        return get_git_tracked_files(path)
    files = []
    if os.path.isdir(path) and not is_hidden(path):
        subdirs = os.listdir(path)
        # This boolean is checked before comparing against the gitignore file
        for filename in subdirs:
            subpath = os.path.join(path, filename)
            if os.path.isdir(subpath):
                files += get_all_files(os.path.join(path, filename))
            elif os.path.isfile(subpath):
                files.append(os.path.join(path, filename))
    
    if os.path.isfile(path):
        return [path]

    return files

def get_code_frequency(path, gitignore = True):
    if not os.path.exists(path):
        return {"ErrorStatus":1, "error":"Please enter a valid path"}
    proj_analysis = {
        "ProjectTitle":os.path.split(path)[1],
        "Type":"local",
        "languages":{}
    }
    all_files = get_all_files(path, gitignore)
    if len(all_files) == 0 and gitignore:
        return {"ErrorStatus":1, "error":"There doesn't seem to be a git repository in this folder"}
    for name in all_files:
        ftype = comutils.get_language(name)
        if ftype is not None:
            if ftype in proj_analysis["languages"]:
                proj_analysis["languages"][ftype] += get_lines_from_file(name)
            else:
                proj_analysis["languages"][ftype] = get_lines_from_file(name)
    proj_analysis["ErrorStatus"] = 0
    return proj_analysis
