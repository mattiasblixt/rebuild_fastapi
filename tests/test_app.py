'''
tests/test_app.py
'''

from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

def test_get_platforms():
    '''
    testing get all API endpoint versions
    '''
    supported_linux = ['redhat8','redhat9',
                   ]
    response = client.get("/platforms")
    assert response.status_code == 200
    assert response.json() == {"platforms": supported_linux}

def test_get_specific_version_ok():
    '''
    testing get specific API endpoint versions (with value)
    '''
    os_relase = 'redhat8'
    versions = ['2.3.0','2.2.0',]
    response = client.get(f"/versions/{os_relase}")
    assert response.status_code == 200
    assert response.json() == {"versions": versions}

def test_get_specific_version_fail():
    '''
    testing get specific API endpoint versions (with non existing OS)
    '''
    fail = 'dont_exists'
    response = client.get(f"/versions/{fail}")
    assert response.status_code == 404
    assert response.json() == {"message": f"OS '{fail}' is not supported"}

def test_get_specific_os_version_patch_ok():
    '''
    testing get specific API endpoint versions (with non existing OS)
    '''
    os_relase = 'redhat8'
    version = '2.3.0'
    patch = 5
    response = client.get(f"/versions/{os_relase}/{version}/{patch}")
    assert response.status_code == 200
    assert response.json() == {"patch": f"{patch}"}

def test_get_specific_os_version_patch_fail():
    '''
    testing get specific API endpoint versions (with non existing OS)
    '''
    os_relase = 'redhat8'
    version = '2.3.0'
    patch = '-1'
    response = client.get(f"/versions/{os_relase}/{version}/{patch}")
    assert response.status_code == 404
    assert response.json() == {"message": f"Patch {patch} is not availble for '{version}' on OS '{os_relase}'"}

def test_get_non_existing_endpoint_fail():
    '''
    testing API endpoint versions with value
    '''
    endpoint = 'dead_endpoint'
    response = client.get(f"/{endpoint}")
    assert response.status_code == 404
    assert response.json() == {"message": f"Endpoint '{endpoint}' not found"}

if __name__ == "__main__":
    pytest.main(["-v", "test_app.py"])
