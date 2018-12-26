# © Robert Geil 2018

ending_dictionary = {
        "py":"Python",
        "js":"JavaScript",
        "java":"Java",
        "cs":"C#",
        "cpp":"C++",
        "html":"HTML",
        "css":"CSS",
        "c":"C",
        "rb":"Ruby",
        "go":"Go"
    }
# Returns the language of a program, and None if a language cannot be
# determined
def get_language(path):
    pos = path.rfind(".")
    ending = path[pos+1:]
    return ending_dictionary.get(ending)

