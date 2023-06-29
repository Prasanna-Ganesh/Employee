class Config(object):
    Debug = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:postgres@localhost/employee"
    )
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = "prasanna"
