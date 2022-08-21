import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cursor = conn.cursor()


def create():
    cursor.execute("""CREATE TABLE IF NOT EXISTS card(
        id INTEGER PRIMARY KEY,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0);""")
    conn.commit()

    ide = []
    while len(ide) < 9:
        ide.append(random.randint(0, 9))

    sum = 8
    copy = ide.copy()
    for i in range(0, len(copy)):
        if i % 2 == 0:
            copy[i] *= 2
            if copy[i] > 9:
                copy[i] -= 9

    for y in copy:
        sum += y

    while True:
        last = random.randint(0, 9)
        if (sum + last) % 10 == 0:
            ide.append(last)
            break

    card_num = '400000' + ''.join([str(i) for i in ide])
    password = ''
    for x in range(4):
        password += str(random.randint(0, 9))

    cursor.execute("INSERT INTO card(number, pin) VALUES (?, ?)", (card_num, password))
    print(f'\nYour card has been created\nYour card number:\n{card_num}\nYour card PIN:\n{password}')


def check_luna(in_num):
    sum_pas = 0
    for x in range(0, len(in_num) - 1):
        if x % 2 == 0:
            y = int(in_num[x]) * 2
            if y > 9:
                y -= 9
        else:
            y = int(in_num[x])
        sum_pas += y

    if (sum_pas + int(in_num[len(in_num) - 1])) % 10 == 0:
        return True


def transfer(num, pas):
    in_num = input('\nTransfer\nEnter card number:\n')
    if check_luna(in_num):
        cursor.execute("SELECT * FROM card WHERE number = ?", (in_num,))
        in_row = cursor.fetchone()
        if in_row is None:
            print('Such a card does not exist.')
        else:
            trans_money = input('Enter how much money you want to transfer:\n')
            if int(trans_money) > row(num, pas)[3]:
                print('Not enough money!')
            else:
                minus = row(num, pas)[3] - int(trans_money)
                plus = in_row[3] + int(trans_money)
                cursor.execute("UPDATE card SET balance = ? WHERE number = ?", (minus, num))
                conn.commit()
                cursor.execute("UPDATE card SET balance = ? WHERE number = ?", (plus, in_num))
                conn.commit()
                print('Success!')
    else:
        print('Probably you made a mistake in the card number. Please try again!')


def cash(num, pas):
    while True:
        print('\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
        user = int(input())
        if user == 1:
            print('Balance:', row(num, pas)[3])
        elif user == 2:
            add = int(input('\nEnter income:\n'))
            new_balance = row(num, pas)[3] + add
            cursor.execute("UPDATE card SET balance = ? WHERE number = ?", (new_balance, num))
            conn.commit()
            print('Income was added!')
        elif user == 3:
            transfer(num, pas)
        elif user == 4:
            cursor.execute("DELETE FROM card WHERE number = ?", (num,))
            conn.commit()
            print('\nThe account has been closed!')
            break
        elif user == 5:
            print('\nYou have successfully logged out!')
            break
        elif user == 0:
            finish()


def row(num, pas):
    cursor.execute("SELECT * FROM card WHERE number = ? AND pin = ?", (num, pas))
    one_row = cursor.fetchone()
    return one_row


def log_in():
    num = input('\nEnter your card number:\n')
    pas = input('Enter your PIN:\n')
    if row(num, pas) is None:
        print('Wrong card number or PIN')
    else:
        print('\nYou have successfully logged in!')
        cash(num, pas)


def finish():
    print('\nBye!')
    conn.commit()
    cursor.close()
    conn.close()
    exit()


while True:
    print("\n1. Create an account\n2. Log into account\n0. Exit """)
    number = int(input())
    if number == 1:
        create()
    elif number == 2:
        log_in()
    elif number == 0:
        finish()
        break
