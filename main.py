'''
main functon for rest api testing 
'''
from fastapi import FastAPI

app = FastAPI()

@app.get("/version")
def get_version():
    '''
    REST API endpoint version
    '''
    return {"version": "1.0"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
