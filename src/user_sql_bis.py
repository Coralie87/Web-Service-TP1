from sqlalchemy import create_engine, text
import random
from faker import Faker
from datetime import datetime
from flask import Flask, jsonify


fake=Faker()
print(fake.name())

app=Flask(__name__)
 
db_string = "postgresql://root:root@localhost:5432/postgres"
 
engine = create_engine(db_string)

@app.route("/user", methods=["GET"])
def get_users():
    users=run_sql_with_result("SELECT * FROM users")
    data = []
    for row in users:
        user={
            "id": row[0],
            "firstname": row[1],
            "lastname": row[2],
            "age": row[3],
            "email": row[4],
            "job": row[5],
        }
        data.append(user)
    return jsonify(data)


 
create_user_table_sql = """
CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    age INTEGER,
    email VARCHAR(255) UNIQUE NOT NULL,
    job VARCHAR(255)
)
"""
 
create_application_table_sql = """
CREATE TABLE IF NOT EXISTS Application (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    lastconnection TIMESTAMP,
    user_id INTEGER REFERENCES Users(id)
)
"""
 
 
def run_sql(query: str):
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(text(query))
        trans.commit()

def run_sql_with_result(query: str):
    with engine.connect() as connection:
        trans = connection.begin()
        result = connection.execute(text(query))
        trans.commit()
        return result

def populate_tables():
    apps = ["Facebook", "Instagram", "Tiktok", "Twitter", "Snapchat"]
    for _ in range(100):
        firstname = fake.first_name()
        lastname = fake.last_name()
        age = random.randrange(18, 50)
        email = fake.email()
        job = fake.job().replace("'", "")
        print(firstname, lastname, age, email, job)

        insert_user_query = f"""
            INSERT INTO users (firstname, lastname, age, email, job)
            VALUES ('{firstname}', '{lastname}', '{age}', '{email}', '{job}' )
            RETURNING id
        """
        user_id=run_sql_with_result(insert_user_query).scalar()
        #create 1 to 5 apps from the apps list
        #Get the current timestamp
        num_apps = random.randint(1, 5)
        for i in range(num_apps):
            username=fake.user_name()
            lastconnection=datetime.now()
            app_name=random.choice(apps)
            sql_insert_app=f"""
            INSERT INTO Application (appname, username, lastconnection, user_id)
            VALUES ('{app_name}', '{username}', '{lastconnection}', '{user_id}')
        """
        run_sql(sql_insert_app)


 
if __name__ =='__main__':
    #Create user table
    #run_sql(create_user_table_sql)
    #Create Application table
    #run_sql(create_application_table_sql)
    #populate_tables()
    app.run(host="0.0.0.0", port=8081, debug=True)