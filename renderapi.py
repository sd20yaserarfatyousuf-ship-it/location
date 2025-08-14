from fastapi import FastAPI, Request

app = FastAPI()

latest_location = {}

@app.post("/location")
async def receive_location(req: Request):
    data = await req.json()
    latest_location["lat"] = data.get("latitude")
    latest_location["lon"] = data.get("longitude")
    print("Received:", latest_location)
    return {"status": "ok"}

@app.get("/get-location")
async def get_location():
    return latest_location
