import os

# konfigurasi global (ENV)
## konfigurasi aplikasi
APP_DEBUG_BOOL = os.getenv("APP_DEBUG_BOOL", "True")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = os.getenv("APP_PORT", "54321")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "f0Rm_C4mP41gN")
APP_STATIC_FOLDER = os.getenv("APP_STATIC_FOLDER", "static")