from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


MENU_LAYOUT = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""


def user_input():
    return input('> ')


def no_tasks():
    print('Nothing to do!\n')


def today_tasks():
    today = datetime.today().date()
    print(f"Today {today.strftime('%d %b')}:")
    rows = session.query(Table).filter(Table.deadline == today).all()
    if len(rows) == 0:
        no_tasks()
    else:
        state = True
        task_number = 1
        for row in rows:
            print(f"{task_number}. {row.task}")
            task_number += 1
            state = False
        if state:
            no_tasks()
        else:
            print()


def week_tasks():
    today = datetime.today().date()
    for day in range(7):
        rows = session.query(Table).filter(Table.deadline == today).all()
        row_number = 1
        print(f"{today.strftime('%A %d %b')}:")
        if rows:
            for row in rows:
                print(f"{row_number}. {row.task}")
            print()
        else:
            no_tasks()
        today += timedelta(days=1)


def all_tasks():
    rows = session.query(Table).all()
    row_number = 1
    for row in rows:
        print(f"{row_number}. {row.task}. {datetime.strftime(row.deadline, '%d %b')}")
        row_number += 1
    if rows:
        print()
    else:
        print("There is no planned tasks.\n")


def missed_tasks():
    print('Missed tasks:')
    rows = session.query(Table).filter(Table.deadline < datetime.today()).all()
    if not rows:
        print('Nothing is missed!')
        print()
        return
    row_number = 1
    for row in rows:
        print(f"{row_number}. {row.task}. {datetime.strftime(row.deadline, '%d %b')}")
        row_number += 1
    print()


def delete_task():
    print('Choose the number of the task you want to delete:')
    rows = session.query(Table).order_by(Table.deadline)
    row_number = 1
    for row in rows:
        print(f"{row_number}. {row.task}. {datetime.strftime(row.deadline, '%d %b')}")
        row_number += 1
    print()
    row_to_delete = int(user_input())
    session.delete(rows[row_to_delete-1])
    session.commit()
    print('The task has been deleted!')
    print()


def add_task():
    print('Enter task')
    new_task = user_input()
    print('Enter deadline')
    task_deadline = user_input()
    try:
        date_object = datetime.strptime(task_deadline, '%Y-%m-%d')
        new_row = Table(task=new_task, deadline=date_object)
        session.add(new_row)
        session.commit()
    except ValueError:
        print('Date is invalid!')
        print()
        return
    print('The task has been added!\n')


def exit_menu():
    print('Bye!')


def processor():
    print(MENU_LAYOUT)
    choice = user_input()
    print()
    if choice == '1':
        today_tasks()
    elif choice == '2':
        week_tasks()
    elif choice == '3':
        all_tasks()
    elif choice == '4':
        missed_tasks()
    elif choice == '5':
        add_task()
    elif choice == '6':
        delete_task()
    elif choice == '0':
        exit_menu()
        return
    else:
        print('Input was incorrect.')
    processor()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    processor()
