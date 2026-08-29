from .crop_router import router as crop_router
from .yield_router import router as yield_router
from .advisory_router import router as advisory_router
from .weather_router import router as weather_router

__all__ = ["crop_router", "yield_router", "advisory_router", "weather_router"]
