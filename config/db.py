from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from core.config import settings


if settings.MODE == 'DEV':
  DATABASE_HOST = "bt2gtprzkoxalty9qk10-mysql.services.clever-cloud.com"
  DATABASE_NAME = "bt2gtprzkoxalty9qk10"
  DATABASE_PORT = "3306"
  DATABASE_USERNAME = "ukbaaa6m0jfdoyfc" 
  DATABASE_PASSWORD = "ggBucN7HvMi6UXTB3XGK"
else:
  DATABASE_HOST = "SG-quaint-server-322-9320-mysql-master.servers.mongodirector.com"
  DATABASE_NAME = "MMW-PRO"
  DATABASE_PORT = "3306"
  DATABASE_USERNAME = "sgroot" 
  DATABASE_PASSWORD = "M7AS14lw5MfxG,YV"

engine = create_engine('mysql+pymysql://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD+'@'+DATABASE_HOST+':'+DATABASE_PORT+'/'+ DATABASE_NAME,echo=False, pool_size=30, max_overflow=-1)
meta = MetaData()
meta.reflect(bind=engine)

Session = sessionmaker(bind=engine)

try:
    session = Session()
    for t in meta.sorted_tables:print(t.name) 
    print("Satisfactory Connection")
except SQLAlchemyError as err:
    print("error", err.__cause__)  


