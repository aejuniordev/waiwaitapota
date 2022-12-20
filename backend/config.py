import os


config = dict(
    DB_URL=os.environ.get('DB_URL', "mongodb://mongo"),
    DB_PORT=os.environ.get('DB_PORT', 27017),
    DB_NAME=os.environ.get('DB_NAME', "waiwaitapota"),
    DB_USER=os.environ.get('DB_USER', ""),
    DB_PASSWORD=os.environ.get('DB_PASSWORD', "")
)