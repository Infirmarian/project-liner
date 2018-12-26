# © Robert Geil 2018

ending_dictionary = {
        "py":"Python",
        "js":"JavaScript",
        "java":"Java",
        "cs":"C#",
        "cpp":"C++",
        "html":"HTML",
        "css":"CSS"
    }
# Returns the language of a program, and None if a language cannot be
# determined
def get_language(url):
    pos = url.rfind(".")
    ending = url[pos+1:]
    return ending_dictionary.get(ending)

