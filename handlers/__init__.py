from aiogram import Router

from . import admin, booking, start


def get_main_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(booking.router)
    router.include_router(admin.router)
    return router
