import sqlite3

# Initialize connection
connection = sqlite3.connect('src/data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

# Run the query
cursor.execute(create_table)

user = (1, 'jose', '12345')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# Insert multiple rows
users = [
    (2, 'rolf', '1234'),
    (3, 'anne', '123456'),
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
