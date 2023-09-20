from server.routers.auth import router as auth_router
from server.routers.user import router as user_router
from server.routers.payment import router as payment_router
from server.routers.ride import router as ride_router

all_routers = [auth_router, user_router, payment_router, ride_router]