from models import Base
from connection import engine
from sqlalchemy import inspect

def init_database():
    inspector = inspect(engine)

    #Verify if the table already exists
    if inspector.has_table('expenses'):
        print("Table already exists, no action needed")
    
    else: 
        print("Table doesn't exist. Creating table")
        Base.metadata.create_all(bind=engine) # Create all tables that is on "base" (models.py)


if __name__ == "__main__":
    init_database()