from litestar import Litestar
from litestar.exceptions import LitestarException


class LitestarLoggerNotConfiguredError(LitestarException):
    def __init__(self) -> None:
        super().__init__("Litestar logger is not configured")


async def log_on_startup(app: Litestar) -> None:
    """Log the app configuration when the app starts."""
    if app.logger is None:
        raise LitestarLoggerNotConfiguredError

    if app.debug:
        app.logger.info("App running in DEBUG mode")
    else:
        app.logger.info("App running in PRODUCTION mode")
