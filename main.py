import uvicorn
from fastapi import FastAPI

from server.routers_init import all_routers


app = FastAPI(
    title="Track Pay"
)

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
