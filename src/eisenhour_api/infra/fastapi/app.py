from fastapi import FastAPI

class EisenhourAPI(FastAPI):
    def __init__(self):
        super().__init__()

app = EisenhourAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
