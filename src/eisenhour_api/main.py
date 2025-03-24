import uvicorn
from src.eisenhour_api.infra.fastapi.app import app

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()