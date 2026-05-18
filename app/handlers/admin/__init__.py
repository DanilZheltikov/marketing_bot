from aiogram import Router

from .admin_panel import router as admin_panel_router
from .mailing_stats import router as mailing_stats_router
from .post import router as admin_post_router
from core.config import settings
from core.middlewares import AdminMiddleware


admin_router = Router(name='admin')

admin_router.message.outer_middleware(AdminMiddleware(settings.admin))
admin_router.callback_query.outer_middleware(AdminMiddleware(settings.admin))

admin_router.include_routers(
    admin_panel_router,
    admin_post_router,
    mailing_stats_router,
)
