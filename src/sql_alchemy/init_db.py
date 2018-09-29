from app import db
from tables import *

if __name__ == "__main__":    
    """ Initialize schema in mysql database """
    db.create_all()
