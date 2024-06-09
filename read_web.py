'''
testbed for developing checkmk application versions
'''

import re
import requests

def get_checkmk_versions():
    '''
    function to webscrape the checkmk.com webpage to collect all
    checkmk application versions released  
    '''
    base_url = 'checkmk.com/download/archive#'

    app_version = 'checkmk-2.3.0'

    url = f"https://{base_url}{app_version}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        # Raise an exception if the response status code is not 200
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")

    reg_exp_grep = r'<checkmk-version\n\s*handle="(.*)"'

    version_matches = re.finditer(reg_exp_grep,response.text)

    version_grep = r'\d\.\d\.\d'
    versions_dict = {}
    for match in version_matches:
        active_result = match.group(1)
        line_regex = re.match(version_grep,active_result)
        major_version = line_regex.group()
        if major_version not in versions_dict:
            versions_dict[major_version] = {}
        patch = active_result.replace(major_version,'')
        patch = patch.replace('-','')
        versions_dict[major_version][patch] = {}

    print(versions_dict)



# with open("myfile.txt", "w", encoding='UTF-8') as filehandler:
#     filehandler.write(content)
# print(content)

if __name__ == "__main__":
    get_checkmk_versions()
