import uvicorn
import os

from logging_config import LOGGING_CONFIG
from settings import Settings

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8555)),
        reload=Settings().debug,
        log_config=LOGGING_CONFIG,
    )