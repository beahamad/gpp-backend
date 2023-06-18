from flask_sqlalchemy import SQLAlchemy

class DatabaseManager:
    _db = None

    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls._db = SQLAlchemy()
        return cls._db
