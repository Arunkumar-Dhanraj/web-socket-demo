# Importing necessary modules
import os  
from dotenv import load_dotenv
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker, declarative_base 

# Loading database connection details from a .env file
load_dotenv()

# Retrieving database connection details from environment variables
host = os.getenv("HOST") 
user = os.getenv("DATABASE")  
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")  

# Constructing the database connection URL
url = f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"

# Creating a SQLAlchemy engine for interacting with the database
engine = create_engine(url)

# Creating a session maker for managing database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating a base class for defining database models
Base = declarative_base()

# Function to get a new database session
def get_db():
    # Creating a new database session
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
