from sqlmodel import SQLModel,create_engine,Session

SQL_URL = "sqlite:///dabbawala.db"
engine = create_engine(SQL_URL,echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session