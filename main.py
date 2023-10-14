import uvicorn
from fastapi import FastAPI

from server.routers_init import all_routers

import firebase_admin
from firebase_admin import credentials

app = FastAPI(
    title="Track Pay"
)


firebase_cred = credentials.Certificate("track-pay.json")
firebase_app = firebase_admin.initialize_app(firebase_cred)



for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
