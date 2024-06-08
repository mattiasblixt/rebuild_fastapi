# test_app.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_version():
    '''
    testing API enpoint version
    '''
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0"}

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "test_app.py"])
