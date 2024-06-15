from sqlalchemy import create_engine, text
 
db_string = "postgresql://root:root@localhost:5432/postgres"
 
engine = create_engine(db_string)
 
create_user_table_sql = text("""
CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    age INTEGER,
    email VARCHAR(255) UNIQUE NOT NULL,
    job VARCHAR(255)
)
""")
 
create_application_table_sql = text("""
CREATE TABLE IF NOT EXISTS Application (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    lastconnection TIMESTAMP,
    user_id INTEGER REFERENCES Users(id)
)
""")
 
 
def run_sql(query:str):
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(query)
        trans.commit()
 
if __name__ =='__main__':
    #Create user table
    run_sql(create_user_table_sql)
    #Create Application table
    run_sql(create_application_table_sql)