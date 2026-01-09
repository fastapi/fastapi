from fastapi import FastAPI, Header, HTTPException, Depends

app = FastAPI()

API_KEY = "mysecretapikey"

def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/secure-data")
def read_secure_data(api_key: str = Depends(get_api_key)):
    return {"message": "This is secure data"}
