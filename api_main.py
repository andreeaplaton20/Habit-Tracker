import uvicorn

if __name__ == "__main__":
    print("Starting API")
    uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=True)