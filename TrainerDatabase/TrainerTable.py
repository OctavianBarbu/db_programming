from dateutil.parser import parse
import mysql.connector as mysql
from datetime import datetime





# connecting to the database using connect() method
# 3 parametrii: host , user, password
def create_structure():

    conn = mysql.connect(host="localhost", user='root', password='', database='')
    #cursor = conn.cursor() # creating an instance of 'cursor' class which is used to execute the SQL statements in python
    with conn.cursor() as c:
        c.execute("CREATE DATABASE IF NOT EXISTS trainers")
        c.execute('''CREATE TABLE IF NOT EXISTS trainers.trainer(
                    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                    name VARCHAR(25) NOT NULL,
                    email VARCHAR(30) NOT NULL,
                    location VARCHAR(20) NOT NULL,
                    contract VARCHAR(40) NOT NULL,
                    password TEXT NOT NULL
                    );
                  ''')
        c.execute('''
                    CREATE TABLE IF NOT EXISTS trainers.session(
                    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
                    hours INT NOT NULL,
                    start_date TIMESTAMP NOT NULL,
                    stop_date TIMESTAMP NOT NULL,
                    order_number VARCHAR(40) NOT NULL,
                    base_price DECIMAL(10.0) NOT NULL,
                    group_id TEXT NOT NULL,
                    is_paid BOOLEAN NOT NULL DEFAULT 0,
                    trainer_id INT NOT NULL,
                    CONSTRAINT fk_trainer_id FOREIGN KEY (trainer_id) REFERENCES trainer(id)
                    );
                  ''')
    conn.close()

def show_menu1():
    print("1.Login")
    print("2.Register")
    print("3.Exit")

def show_menu2():
    print("1.Add new training session")
    print("2.Get upcoming training sessions")
    print("3.Get unpaid training sessions")
    print("4.Generate bill")
    print("5.Get total pay by year")
    print("6.Logout")
    print("7.Exit")

create_structure()
conn = mysql.connect(host="localhost", user='root', password='', database='trainers')


user_logged = None
while True:
    if user_logged is None:
        show_menu1()
        choice = int(input("Choose: "))

        if choice == 3:
            break
        elif choice == 1:
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            with conn.cursor() as c:
                c.execute("SELECT id FROM trainer WHERE email = %s AND password = %s;",(email,password))
                result = c.fetchone()

                if result:
                    user_logged = result[0]
                else:
                    print("The email or password you entered is incorrect")

        elif choice == 2:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            location = input("Enter your location: ")
            contract = input("Enter your contract no: ")
            password = input("Enter a password: ")

            with conn.cursor() as c:
                c.execute(
                    "INSERT INTO trainer (name, email, location, contract, password)  VALUES (%s, %s, %s, %s, %s );",
                    (name, email, location, contract, password))
                conn.commit()

    else:
        show_menu2()
        choice = int(input("Choose: "))

        if choice == 7:
            break
        elif choice == 6:
            user_logged = None
        elif choice == 1:
            hours = int(input("Enter hours"))
            start_date = parse(input("Enter start date: "))
            stop_date = parse(input("Enter stop date: "))
            order_number = input("Enter order number: ")
            base_price = float(input("Enter base price: "))
            group_id = input("Enter group id: ")
            trainer_id = int(input("Enter trainer id: "))

            with conn.cursor() as c:
                c.execute(
                    "INSERT INTO session (hours, start_date, stop_date, order_number, base_price, group_id, trainer_id)  VALUES (%s, %s, %s, %s, %s, %s, %s );",
                    (hours, start_date, stop_date, order_number, base_price, group_id, user_logged))
                conn.commit()
        elif choice == 2:
            with conn.cursor() as c:
                c.execute("SELECT * FROM session WHERE start_date > %s AND trainer_id = %s;",(datetime.now(), user_logged))
                results = c.fetchall()
                for result in results:
                    print(result)

        elif choice == 3:
            with conn.cursor() as c:
                c.execute("SELECT * FROM session WHERE is_paid = 0 AND trainer_id = %s", (user_logged,))
                results = c.fetchall()
                for result in results:
                    print(f'Your unpaid sessions are: ID ->{result[0]} \nNumber of Hours->{result[1]} '
                          f'\nStart day->{result[2]} \nEnd day->{result[3]} \nOrder no.->{result[4]} '
                          f'\nBase price->{result[5]} \nGroup Id->{result[6]} \nIs Paid->{result[7]} '
                          f'\nTrainer Id->{result[8]}')


        elif choice == 4:
            with conn.cursor() as c:
                c.execute("SELECT * FROM session WHERE is_paid = 0 AND trainer_id = %s", (user_logged,))
                results = c.fetchall()

                for result in results:
                    c.execute("UPDATE session SET is_paid = 1 WHERE id = %s", (result[0],))
                conn.commit()

        elif choice == 5:
            year = int(input("Enter the year you want billed: "))
            with conn.cursor() as c:
                c.execute("SELECT SUM(hours*base_price) FROM session "
                          "WHERE is_paid=1 AND trainer_id=%s AND start_date BETWEEN %s AND %s "
                          "AND stop_date BETWEEN %s AND %s", (user_logged, datetime(year,1,1,0,0,0), datetime(year,12,31,23,59,59),datetime(year,1,1,0,0,0), datetime(year,12,31,23,59,59)))
                result = c.fetchone()
                print(f"The total bill for year {year} is {result[0]} EUR!")
conn.close()








