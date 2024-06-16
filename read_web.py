'''
testbed for developing checkmk application versions
'''

import re
import os
import sys
import datetime
import logging
import ast
# https://www.delftstack.com/howto/python/python-logging-to-file-and-console/
import requests

def conv_ux_timestamp(unixtime:int) -> datetime.datetime:
    '''
    converts unix timestamp to datetime
    '''
    return datetime.datetime.fromtimestamp(unixtime)

def insert_char_at_position(in_str: str, char: str, position: int) -> str:
    '''
    helper function to insert a char at a position
    '''
    if position > 0:
        return in_str[:position] + char + in_str[position + 1:]
    return in_str[:-1] + char

def find_matching_braces_with_positions(in_str:str) -> list[tuple]:
    '''
    Finds matching braces in the input string and returns their start and end positions.

    Args:
        in_str (str): Input string containing braces.

    Returns:
        list[tuple]: List of tuples representing start and end positions of matching braces.
    '''
    stack = []
    brace_positions = []  # List to store start and end positions of braces

    for i, char in enumerate(in_str):
        if char == '{':
            stack.append(i)
        elif char == '}':
            if stack:
                start_index = stack.pop()
                brace_positions.append((start_index, i+1))  # Add start and end positions
            else:
                print(f"Unmatched closing brace at index {i}")
    if stack:
        print(f"Unmatched opening braces at indices: {stack}")

    return brace_positions

def remove_chars(in_string: str, removables=None) -> str:
    '''
    Removes specified characters from the input string.

    Args:
        in_string (str): The input string.
        removables (list, optional): List of characters to remove.
        Defaults to None (removes '{' and '}').

    Returns:
        str: The modified string with specified characters removed.
    '''
    if removables is None:
        removables = ['{', '}']

    translation_table = str.maketrans('', '', ''.join(removables))
    cleaned_string = in_string.translate(translation_table)

    return cleaned_string

def handle_base_case(in_str:str) -> dict:
    '''
    PEP 8
    '''
    logging.debug('in handle_base_case (%s)', in_str)
    first_semicolon = in_str.index(':')
    my_key = remove_chars(in_str[:first_semicolon])
    my_val = remove_chars(in_str[first_semicolon+1:])
    logging.debug('''key: '%s' val: '%s' ''', my_key, my_val)
    return {my_key:my_val}

def make_key_and_value(in_str:str, in_list:list) -> tuple[str,str]:
    '''
    PEP8
    '''
    my_val = in_str[in_list[0][0]+1:in_list[0][1]-1]
    my_key = remove_chars(in_str.replace(my_val,''),[':','}','{'])
    return my_key, my_val

def str_to_dict(in_str:str) -> dict:
    '''
    take 3
    '''
    logging.debug('str_to_dict start %s', in_str)
    in_dicts = find_matching_braces_with_positions(in_str)
    sorted_in_dicts = sorted(in_dicts, key=lambda x: x[0])
    logging.debug('dicts found in value part: %s (%s)', len(sorted_in_dicts), sorted_in_dicts)

    if len(sorted_in_dicts) <= 1:
        commas = in_str.count(',')
        logging.debug('commas: %s ', commas)
        if len(sorted_in_dicts) == 0:
            return handle_base_case(in_str)
        if len(sorted_in_dicts) == 1:
            logging.debug('''1 '{''}' pair found in sorted_in_dicts''')
            if sorted_in_dicts[0][0] == 0:
                logging.debug('entry lack key')
                return sub_key_looper(in_str)
            my_key, my_val = make_key_and_value(in_str,sorted_in_dicts)
            if commas == 0:
                logging.debug('''key: '%s' val: '%s' ''',my_key,  my_val)
                return {my_key:str_to_dict(my_val)}
            return {my_key:sub_key_looper(my_val)}

    if len(sorted_in_dicts) == 2:
        my_key, my_val = make_key_and_value(in_str,sorted_in_dicts)
        logging.debug('''key: '%s' val: '%s' ''',my_key,  my_val)
        return {my_key:str_to_dict(my_val)}

    master_key:str = ''
    key_value_collection = {}
    for no, item in enumerate(sorted_in_dicts):
        if no == 0:
            master_key = remove_chars(in_str[:item[0]],[':','}','{'])
            logging.debug('master_key %s', master_key)
        else:
            if (no % 2) == 0:
                logging.debug('even')
                sub_key = in_str[sorted_in_dicts[no-1][1]:sorted_in_dicts[no][0]]
            else:
                logging.debug('odd')
                sub_key = in_str[sorted_in_dicts[no-1][0]:sorted_in_dicts[no][0]]
            sub_key = remove_chars(sub_key,[':','}','{',','])
            logging.debug('sub_key: %s',sub_key)
            logging.debug('no:%s - %s ',no, item)
            value = in_str[item[0]:item[1]]
            logging.debug('value: \'%s\'',value)
            key_value_collection.update({sub_key:str_to_dict(value)})
    return {master_key:key_value_collection}

def sub_key_looper(in_str:str):
    '''
    deo
    '''
    sub_dicts = {}
    logging.debug('sub_key_looper: %s',in_str)
    sub_pairs = in_str.split(',')
    for item in sub_pairs:
        logging.debug('working on item %s', item)
        sub_dicts.update(str_to_dict(remove_chars(item)))
    return sub_dicts

def my_cleaner(intext:str):
    '''
    deo
    '''
    first = intext.replace('&quot;','')
    first = insert_char_at_position(first,'',-1)
    #logging.info("first '%s'",first)
    print_dict = str_to_dict(first)
    logging.info("my_cleaner %s", print_dict)
    return print_dict

def age_check(file_path: str, max_age:int = 24) -> bool:
    '''
    Function to check the age of a file.
    Returns True if the file age is under max_age hours
    False otherwise.
    '''

    try:
        modification_time = os.path.getmtime(file_path)
        modification_datetime = datetime.datetime.fromtimestamp(modification_time)
        current_datetime = datetime.datetime.now()
        file_age = current_datetime - modification_datetime
        return_val = file_age.total_seconds() < max_age * 3600
        if return_val:
            specific = 'under'
            # logging.info('file: %s is under %sh old', file_path, max_age)
        else:
            specific = 'over'
        logging.info('file: %s is %s %sh old', file_path, specific, max_age)
        return return_val
    except FileNotFoundError:
        logging.info("File '%s' not found.",file_path)
        return False


def write_file(file_path: str, data):
    '''
    Simple write to file function.
    Handles the possibility of disk full or permission issues.
    Returns a string indicating success or failure.
    '''
    try:
        with open(file_path, "w", encoding='UTF-8') as filehandler:
            filehandler.write(data)
        return "File written successfully."
    except PermissionError:
        return "Permission denied."
    except OSError as e:
        return f"Error writing to file: {e}"


def read_file(file_path: str) -> str:
    '''
    Simple read from file function.
    Returns the content of the file as a string.
    If the file is not found, returns "File not found."
    '''
    try:
        with open(file_path, "r", encoding='UTF-8') as filehandler:
            return filehandler.read()
    except FileNotFoundError:
        return "File not found."


def get_checkmk_version_data():
    '''
    function to webscrape the checkmk.com webpage to collect all
    checkmk application versions released  
    '''

    url = "https://checkmk.com/download/archive#checkmk-2.3.0"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
        # Raise an exception if the response status code is not 200
    except requests.RequestException as e:
        logging.info("Error fetching data from %s: %s",url, e)
        raise ValueError(f"Error fetching data from {url}") from e


def refine_checkmk_data(in_data):
    '''
    handle the data
    '''
    pattern = r"""<checkmk-version
                  \s*handle="(.*)"
                  \n.*:is-daily="(.*)"
                  \n.*\s*notes=.*
                  \n\s*:version="{(.*)&quot;date&quot\;\:(\d*)\}\"\>
                  \s*<\/checkmk-version>
               """

    reg_exp_grep = re.compile(pattern, re.VERBOSE)

    version_matches = re.finditer(reg_exp_grep, in_data)

    versions_dict = {}
    for match in version_matches:
        handle_grep = match.group(1)
        is_daily_grep = match.group(2)
        version_grep = match.group(3)
        unix_grep = match.group(4)
        major_version = get_major_version(handle_grep)
        if major_version not in versions_dict:
            versions_dict[major_version] = {}
        patch = handle_grep.replace(major_version,'')
        patch = patch.replace('-','')
        versions_dict[major_version][patch] = {'release_date':conv_ux_timestamp(int(unix_grep)),
                                               'is_daily_release':is_daily_grep,
                                               'versions':my_cleaner(version_grep),
                                               }
        break

    logging.info(versions_dict)

def get_major_version(in_str):
    '''
    returns the major wersion of checmk based upon in string
    '''
    version_regex = r'\d\.\d\.\d'
    line_regex = re.match(version_regex,in_str)
    return line_regex.group()

if __name__ == "__main__":
    #logging = logging.getlogging(__name__)
    logging.basicConfig(level=logging.INFO,
                        #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
                        format='%(asctime)s %(name)s %(levelname)s %(lineno)d %(message)s',
                        handlers=[logging.FileHandler("read_web.log"),
                                  logging.StreamHandler(sys.stdout)],
                        )
    FILE_PATH='request.txt'
    if not age_check(file_path=FILE_PATH):
        write_file(file_path=FILE_PATH, data=get_checkmk_version_data())

    RESPONSE_TEXT = read_file(file_path=FILE_PATH)
    refine_checkmk_data(RESPONSE_TEXT)
