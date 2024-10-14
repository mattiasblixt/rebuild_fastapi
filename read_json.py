'''
test to make a json read function
'''

import json
import logging
import pandas as pd
from pprint import pformat

logging.basicConfig(level=logging.INFO,
                    #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
                    format='%(asctime)s %(name)s %(levelname)s %(lineno)d %(message)s',
                    handlers=[#logging.FileHandler("read_web.log"),
                                logging.StreamHandler()],
                    )

def read_json(path):
    '''
    simple  function to read json to dict
    '''
    try:
        with open(file=path,
                encoding='UTF-8') as file_handler:
            return json.load(file_handler)
    except PermissionError as exept:
        logging.error('permission denied: %s',exept )
        raise PermissionError("permission denied") from exept

def main():
    '''
    main function
    '''
    read_dict = read_json('versions_dict.json')
    list_of_list = []
    major_ver = list(read_dict.keys())
    for major in major_ver:
        app_version_dict = read_dict[major]
        patches_list = list(app_version_dict.keys())
        #logging.debug('major: %s patches: %s', major, patches_list)
        for patch in patches_list:
            #logging.info(version_dict[patch])
            active_patch_dict = app_version_dict[patch]
            release_date = active_patch_dict.get('release_date','')
            is_daily_release = active_patch_dict.get('is_daily_release','')
            app_edition_dict = active_patch_dict.get('versions',dict)
            editions_list = list(app_edition_dict.keys())
            #logging.info('%s %s %s', major, patch, editions_list)
            for edition in editions_list:
                active_app_dict = active_patch_dict['versions'][edition]
                #logging.info(active_app_dict)
                os_list = list(active_app_dict.keys())
                #logging.info(os_list)
                for os in os_list:
                    active_os = active_app_dict[os]
                    # logging.info(active_os)
                    for lkey, lval in active_os.items():
                        row = [major,
                               patch,
                               release_date,
                               is_daily_release,
                               edition,
                               cmk_edition_common_name(edition),
                               os,
                               lkey,
                               os_edition_common_name(lkey),
                               lval]
                        list_of_list.append(row)
    logging.info(pformat(list_of_list))

def cmk_edition_common_name(in_str: str)-> str:
    '''
    retunrs common name of versions
    '''
    cmk_editions = {'cee':'Enterprise',
                    'cre':'Raw',
                    'cfe':'',
                    'cfe_32':'',
                    'cee_32':'Enterprise (32)',
                    'cre_32':'Raw (32)',
                    'cce':'Cloud',
                    'cme':'MSP',
    }
    try:
        return cmk_editions[in_str]
    except KeyError:
        return ''

def os_edition_common_name(in_str: str)-> str:
    '''
    returns common names of OS relases
    '''
    os_editions = {'el5':'Enterprise Linux 5',
                   'el6':'Enterprise Linux 6',
                   'el7':'Enterprise Linux 7',
                   'el8':'Enterprise Linux 8',
                   'el9':'Enterprise Linux 9',

    }
    try:
        return os_editions[in_str]
    except KeyError:
        return ''

if __name__ == "__main__":
    main()
