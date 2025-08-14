from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔁 Replace these with your actual GitHub Pages origins
# e.g. https://arfat.github.io and/or https://arfat.github.io/location-capture
origins = [
    "https://sd20yaserarfatyousuf-ship-it.github.io",
    "https://sd20yaserarfatyousuf-ship-it.github.io/location"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)




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


