import mysql.connector as mysql
import datetime


def create_structure():
    conn = mysql.connect(
        host="localhost",
        user="root",
        password="Superpuff001!",
        database="",
    )

    with conn.cursor() as c:
        c.execute("CREATE DATABASE IF NOT EXISTS shop;")
        c.execute("""
            CREATE TABLE IF NOT EXISTS shop.utilizator (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nume TEXT NOT NULL,
                email TEXT NOT NULL,
                parola TEXT NOT NULL
            );
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS shop.produs (
                id INT PRIMARY KEY AUTO_INCREMENT,
                denumire TEXT NOT NULL,
                cantitate INT NOT NULL,
                pret DECIMAL(8, 2) NOT NULL 
            );
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS shop.istoric (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                produs_id INT NOT NULL,
                data TIMESTAMP NOT NULL,
                cantitatea_cumparata INT NOT NULL,
                CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES shop.utilizator(id),
                CONSTRAINT fk_produs_id FOREIGN KEY(produs_id) REFERENCES shop.produs(id)
            );
        """)

    conn.close()


create_structure()

conn = mysql.connect(host="localhost", user='root', password='Superpuff001!', database='shop')

def show_menu_1():
    print("1. Login")
    print("2. Register")
    print("0. Exit application")


def show_menu_2():
    print("1. Show product list")
    print("2. Buy product")
    print("3. Show history")
    print("4. Logout")
    print("5. Add Product")
    print("0. Exit application")

def show_product_list():
    print('-' * 20)
    with conn.cursor() as c:
        c.execute("SELECT * FROM produs;")
        results = c.fetchall()
        print("Our products are: ")
        for result in results:
            print("\t-", result[1])
    print('-' * 20)

def buy_product():
    id = int(input("Wich product would you like to buy?: "))
    cantitate = int(input("Insert quantity: "))
    with conn.cursor() as c:
        c.execute("SELECT * FROM produs WHERE id=%s AND cantitate>=%s", (id, cantitate))
        result = c.fetchone()
        if result:
            c.execute("UPDATE produs SET cantitate = cantitate - %s WHERE id=%s", (cantitate, id))
            c.execute("INSERT INTO istoric (user_id, produs_id, data, cantitatea_cumparata) VALUES (%s, %s, %s, %s);",
                      (user_logged, id, datetime.datetime.now(), cantitate))
            conn.commit()

user_logged = None
while True:
    if user_logged is None:
        show_menu_1()
        choice = int(input("Choose: "))

        if choice == 0:
            break
        elif choice == 1:
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            with conn.cursor() as c:
                c.execute("SELECT id FROM utilizator WHERE email = %s AND parola = %s;",(email,password))
                result = c.fetchone()

                if result:
                    user_logged = result[0]
                else:
                    print("The email or password you entered is incorrect")

        elif choice == 2:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter a password: ")

            with conn.cursor() as c:
                c.execute(
                    "INSERT INTO utilizator (nume, email, parola)  VALUES (%s, %s, %s);", (name, email, password))
                conn.commit()

    else:
        show_menu_2()
        choice = int(input("Choose: "))

        if choice == 0:
            break

        elif choice == 4:
            user_logged = None

        elif choice == 1:
            show_product_list()

        elif choice == 2:
            buy_product()

        elif choice == 5:
            denumire = input("Denumire: ")
            cantitate = int(input("Cantitate: "))
            pret = int(input("Pret: "))
            with conn.cursor() as c:
                c.execute(f"INSERT INTO produs(denumire, cantitate, pret) VALUES ('{denumire}','{cantitate}','{pret}');")
                conn.commit()

        elif choice == 3:
            with conn.cursor() as c:
                c.execute(
                    "SELECT p.denumire, p.pret, i.cantitatea_cumparata, i.data FROM istoric i INNER JOIN produs p ON i.produs_id = p.id WHERE i.user_id = %s;", (user_logged,)
                )
                results = c.fetchall()
                for result in results:
                    print(f"Ati cumparat {result[2]} {result[0]} in data de {result[-1]} in valoare de {result[1]*result[2]}")


