
import sys
import os
import requests
from bs4 import BeautifulSoup
import colorama

#------------ MACRO'S -------------------------

DEFAULT_PARSER = 'html.parser'
LEGAL_TAGS = ['p','a','ul','ol','li']
HYPERLINK_TAG = 'a'
EXIT_CMD = 'exit'
BACK_CMD = 'back'
NO_DOT_ERR = 'Error: URL dont contain a dot'
USAGE_ERR = "Error Usage: args should be <dir>"
SUCCESS_STATUS_CODE = 200
URL_ERR = "Error: unable to open URL"


# ----------- functions ------------------------

# check if the given str start with https and add it if not
def check_https(my_str) -> str:
    if my_str.startswith("https://"):
        return my_str
    return "https://" + my_str

#print and proccess the given URL source code
def show_page(name, full_file_name):
    request = requests.get(check_https(name))
    if not request.status_code == SUCCESS_STATUS_CODE:
        print(URL_ERR)
        return
    soup = BeautifulSoup(request.content, DEFAULT_PARSER)
    content_list = soup.find_all(LEGAL_TAGS)
    with open(full_file_name, 'w') as f:
        for data in content_list:
            if data.name == HYPERLINK_TAG:
                print(colorama.Fore.BLUE + data.text)
            else:
                print(data.text)
            f.write(data.text)

# show the URL page with show_page() and save to history
def enter_page(my_str, history_stack):
    full_file_name = os.path.join(full_path, my_str)
    show_page(my_str,full_file_name)
    history_stack.append((my_str,full_file_name))


# text based browser
# get a url's from the user show them ans save them into a given directory
def browse(my_str):
    history_stack = []
    while (my_str != EXIT_CMD):  # get user input until he want to exit
        my_str = input()
        if my_str == EXIT_CMD:
            break
        elif my_str == BACK_CMD:
            if len(history_stack) > 1:
                name, full_name = history_stack.pop(-2) #the last one before current page
                show_page(name, full_name)
        elif not ('.' in my_str):
            print(NO_DOT_ERR)
        else:
            enter_page(my_str, history_stack)


# ----------------------------------------------

if __name__ == '__main__':

    # handling arguments from CMD
    args = sys.argv

    if (len(args) != 2):  # check the num of args
        print(USAGE_ERR)
        exit()

    path = os.getcwd()  # create a directory
    full_path = os.path.join(path, args[1])

    try:
        os.mkdir(full_path)
    except:
        print("dir exist already")
    my_str = ""
    browse(my_str)
