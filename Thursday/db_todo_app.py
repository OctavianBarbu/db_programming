from dateutil.parser import parse
import mysql.connector as mysql
from datetime import datetime

def create_structure():

    conn = mysql.connect(host="localhost", user='root', password='Superpuff001!', database='')
    with conn.cursor() as c:
        c.execute("CREATE DATABASE IF NOT EXISTS db_tasks")
        c.execute('''CREATE TABLE IF NOT EXISTS db_tasks.tasks(
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    task TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT 0
                    );
                  ''')

    conn.close()

create_structure()

def show_menu():
    print("1.Show task list")
    print("2.Mark task as done")
    print("3.Add new task")
    print("4.Exit")

def show_tasks():
    print('-' * 20)
    with conn.cursor() as c:
        c.execute("SELECT * FROM tasks WHERE done = 0 order by id;")
        results = c.fetchall()
        print("Unfinished tasks for today:")
        for result in results:
            print("\t-", result[1])
    print('-' * 20)


def mark_as_done():
    choice = int(input("enter completed task id: "))
    with conn.cursor() as c:
        c.execute("SELECT id FROM tasks WHERE done = 0")
        result1 = c.fetchall()
        c.execute("UPDATE tasks SET done = 1 WHERE id = %s", (choice,))
        conn.commit()
        c.execute("SELECT id FROM tasks WHERE done = 0")
        result2 = c.fetchall()

    if len(result2) < len(result1):
        print("------- IT WORKED! -------")
    else:
        print("------ DIDN'T WORK! -------")

def add_task():
    task_name = input("Enter task name: ")
    with conn.cursor() as c:
        c.execute(
            "INSERT INTO tasks (task)  VALUES (%s);", (task_name,))
        conn.commit()


conn = mysql.connect(host="localhost", user='root', password='Superpuff001!', database='db_tasks')

while True:
    show_menu()
    choice = int(input("\tWhich option would you like to choose?: "))
    if choice == 4:
        break
    elif choice == 3:
        add_task()
    elif choice == 2:
        mark_as_done()
    elif choice == 1:
        show_tasks()

conn.close()