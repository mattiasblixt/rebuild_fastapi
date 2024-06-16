import logging
import sys

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
