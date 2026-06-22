from fastapi import FastAPI
app = FastAPI(title="LeadRadar AI API")

@app.get("/")
def root():
    return {"message":"LeadRadar AI Backend Running"}
