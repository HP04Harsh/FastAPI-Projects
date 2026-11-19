from sqlmodel import SQLModel, create_engine, Session

sqlite_url = "sqlite:///rangmunch.db"
engine = create_engine(sqlite_url, echo=True)  # echo=True logs generated SQL queries

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency Injection for Database Sessions
def get_session():
    with Session(engine) as session:
        yield session