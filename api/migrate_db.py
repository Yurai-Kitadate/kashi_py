from sqlalchemy import create_engine

from api.models.transaction import Base as Transaction_Base
from api.models.user import Base as User_Base

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Transaction_Base.metadata.drop_all(bind=engine)
    Transaction_Base.metadata.create_all(bind=engine)
    User_Base.metadata.drop_all(bind=engine)
    User_Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()