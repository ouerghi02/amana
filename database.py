from sqlmodel import create_engine, Session

database_url = "mysql+pymysql://root:root@localhost/amana_db"
engine = create_engine(database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
