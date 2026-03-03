from fastapi import FastAPI

app = FastAPI(title="AI Zomato Recommendation Service")

@app.get("/health")
def health():
    return {"status": "ok"}