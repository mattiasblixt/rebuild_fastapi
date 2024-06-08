'''
main functon for rest api testing 
'''
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

def get_db():
    '''
    simulate a backend database
    '''
    return {'redhat8':{'2.3.0':{'5':{'local':True},
                                     '4':{'local':False},
									 '3':{'local':False},
									 '2':{'local':False},
									 '1':{'local':False},
									 '':{'local':False},
                                    },
                       '2.2.0':{'27':{'local':True},
                                  '26':{'local':False},
                                  '25':{'local':False},
                                  '24':{'local':False},
                                  '23':{'local':False},
                                  '':{'local':False},
                              },
                      },
            'redhat9':{'2.3.0':{'5':{'local':True},
                                     '4':{'local':False},
									 '3':{'local':False},
									 '2':{'local':False},
									 '1':{'local':False},
									 '':{'local':False},
                                    },
                       '2.2.0':{'27':{'local':True},
                                  '26':{'local':False},
                                  '25':{'local':False},
                                  '24':{'local':False},
                                  '23':{'local':False},
                                  '':{'local':False},
                              },
                     },
           }

def get_release_info(linux_os:str, version=None, patch=None):
    '''
    data return
    '''
    dict_data = get_db()
    if version is None:
        return dict_data.keys()

    if linux_os not in dict_data:
        raise ValueError(f"{linux_os} not supported")
    else:
        return_dict = {'os': linux_os,
                    'version': None,
                    'patch': None,
                    }
    if version is not None:
        if version not in dict_data[linux_os]:
            raise ValueError(f"{version} is not availible for OS {linux_os}")
        return_dict['version'] = version
    if version is not None:
        if patch not in dict_data[linux_os][patch]:
            raise ValueError(f"{patch} is not availible for {version} with OS {linux_os}")
        return_dict['patch'] = patch

    return return_dict

@app.get("/platforms")
def get_api_platforms():
    '''
    REST API endpoint platforms
    '''
    return {"platforms": list(get_db().keys())}

@app.get("/versions", response_class=HTMLResponse)
def get_api_versions():
    '''
    REST API endpoint platforms
    '''
    return """<html><body>missing mandatory platform parameter see
    <a href='/platforms'>/platforms</a> for valid</body></html>"""

@app.get("/versions/{linux_release}")
def get_api_specified_version(linux_release: str, response: Response):
    '''
    REST API endpoint specific version
    '''
    data_dict = get_db()
    if linux_release in data_dict:
        data_dict = data_dict[linux_release]
        return {"versions": list(data_dict.keys())}
    response.status_code = 404
    return {"message": f"OS '{linux_release}' is not supported"}

@app.get("/versions/{linux_release}/{version}")
def get_api_specified_os_and_major(linux_release: str, version:str, response: Response):
    '''
    REST API endpoint specific release and major version
    '''
    data_dict = get_db()
    if linux_release not in data_dict:
        response.status_code = 404
        return {"message": f"OS '{linux_release}' is not supported"}
    data_dict = data_dict[linux_release]
    if version not in data_dict:
        response.status_code = 404
        return {"message": f"Version '{version}' is not availible for OS '{linux_release}'"}
    data_dict = data_dict[version]
    return {"versions": list(data_dict.keys())}

@app.get("/versions/{linux_release}/{version}/{patch}")
def get_api_specified_os_and_version_patch(linux_release: str,
                                           version:str,
                                           patch:str,
                                           response: Response):
    '''
    REST API endpoint specific release and major version
    '''
    data_dict = get_db()
    if linux_release not in data_dict:
        response.status_code = 404
        return {"message": f"OS '{linux_release}' is not supported"}
    data_dict = data_dict[linux_release]
    if version not in data_dict:
        response.status_code = 404
        return {"message": f"Version '{version}' is not availible for OS '{linux_release}'"}
    data_dict = data_dict[version]
    if patch == 'latest':
        patches = list(data_dict.keys())
        return {"patch": max(patches)}
    if patch not in data_dict:
        response.status_code = 404
        return {"message": f"Patch {patch} is not availble for '{version}' on OS '{linux_release}'"}
    return {"patch": f"{patch}"}

@app.get("/{path:path}")
def api_catch_all(path: str, response: Response):
    '''
    Catch-all route for non-existing endpoints
    '''
    response.status_code = 404
    return {"message": f"Endpoint '{path}' not found"}

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
