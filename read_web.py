'''
testbed for developing checkmk application versions
'''

import re
import json
import os
import sys
import datetime
import logging
from pprint import pformat
import requests
# https://www.delftstack.com/howto/python/python-logging-to-file-and-console/

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
    logging.debug('entering find_matching_braces_with_positions')
    stack = []
    brace_positions = []  # List to store start and end positions of braces
    logging.debug('working with string of length %s', len(in_str))
    for i, char in enumerate(in_str):
        if char == '{':
            stack.append(i)
        elif char == '}':
            if stack:
                start_index = stack.pop()
                brace_positions.append((start_index, i+1))  # Add start and end positions
            else:
                logging.warning("Unmatched closing brace at index (%s)", i)
    if stack:
        logging.warning("Unmatched opening braces at indices: (%s)", stack)

    sorted_brace_positions = sorted(brace_positions, key=lambda x: x[0])
    logging.debug('leaving find_matching_braces_with_positions')
    return sorted_brace_positions


def get_master_pair_list(in_list) -> list:
    '''
    function that returns outer pairs from nestled ones.
    '''
    master_pairs:list = []
    first_pair:int = in_list[0][1]
    master_pairs.append((0,first_pair))
    logging.debug('first master pair ends at: %s', first_pair)
    for _, item in enumerate(in_list):
        if list(item)[0] > first_pair:
            logging.debug('adding new master pair: (%s,%s)', first_pair+1, item[1])
            master_pairs.append((first_pair+1, item[1]))
            first_pair = item[1]
    logging.debug('all master pairs: %s',master_pairs)
    return master_pairs


def handle_base_case(in_str:str) -> dict:
    '''
    handles the bascase of dict in string format
    '''
    grep_str = r'''([a-z0-9-.]*):([a-z0-9-._]*)'''
    logging.debug('in handle_base_case')
    logging.debug('in_str: %s', in_str)
    regex_result = re.findall(pattern=grep_str,
                       string=in_str)

    ret_dict = {}
    for item in regex_result:
        my_key = item[0]
        my_val = item[1]
        ret_dict.update({my_key:my_val})
        logging.debug('''adding, key: '%s' val: '%s' ''', my_key, my_val)

    return ret_dict


def rm_outer_curly_braces(in_str:str) -> str:
    '''
    removed the first and last char of a string
    '''
    if in_str[0] == '{' and in_str[-1] == '}':
        return in_str[1:-1]
    return in_str

def str_to_dict(in_str:str) -> dict:
    '''
    Now working - 2024-07-14!!
    '''
    logging.debug('entering str_to_dict')
    logging.debug('length of string: %s,\nin_str:  \'%s\' ',len(in_str), in_str)
    pairs = find_matching_braces_with_positions(in_str)
    logging.debug('%s pairs found, details: %s ', len(pairs), pairs)
    if len(pairs) > 0:
        master_pairs = get_master_pair_list(pairs)
        ret_dict = {}
        for item in master_pairs:
            logging.debug('working on master pair %s', item)
            active_sub_str = in_str[item[0]:item[1]]
            logging.debug('details %s', active_sub_str)
            logging.debug('pair_lenght: %s', len(active_sub_str))

            match = re.match(r'''^(\w{3,}):{''', active_sub_str)
            if match:
                clean_key = match.group(1)
                logging.debug('clean_key %s', clean_key)
                rest = active_sub_str[len(clean_key)+1:]
                rest = rm_outer_curly_braces(rest)
                logging.debug('rest: %s', rest)
                ret_dict[clean_key] = str_to_dict(rest)
        return ret_dict
    logging.debug('will handle basecase')
    return handle_base_case(in_str)


def count_dicts(in_text, target_word):
    '''
    my test
    '''
    return in_text.lower().count(target_word.lower())

def my_cleaner(intext:str):
    '''
    deo
    '''
    first = intext.replace('&quot;','')
    first = insert_char_at_position(first,'',-1)
    write_file('first.txt',first)
    print_dict = str_to_dict(first)
    logging.debug("my_cleaner %s", print_dict)
    return print_dict

def check_file_age(file_path: str, max_age:int = 24) -> bool:
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


def write_to_json(in_dict:dict, path:str) -> None:
    '''
    simepl function to write dict to json
    '''
    try:
        with open(file=path,
                  mode='w',
                  encoding='UTF-8') as convert_file:
            convert_file.write(json.dumps(in_dict, default=str))
    except PermissionError as exept:
        logging.error('permission denied: %s',exept )
        raise PermissionError("permission denied") from exept


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
        # break
    write_to_json(versions_dict,'versions_dict.json')
    logging.info(pformat(versions_dict,indent=4))


def get_major_version(in_str):
    '''
    returns the major wersion of checmk based upon in string
    '''
    version_regex = r'\d\.\d\.\d'
    line_regex = re.match(version_regex,in_str)
    return line_regex.group()

def worker():
    '''
    does all the heavy lifting
    '''
    file_path='request.txt'
    if not check_file_age(file_path=file_path):
        write_file(file_path=file_path, data=get_checkmk_version_data())

    response_text = read_file(file_path=file_path)
    refine_checkmk_data(response_text)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
                        format='%(asctime)s %(name)s %(levelname)s %(lineno)d %(message)s',
                        handlers=[logging.FileHandler("read_web.log"),
                                  logging.StreamHandler(sys.stdout)],
                        )
    worker()
    