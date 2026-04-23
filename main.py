
import random
import string
import mysql.connector
from datetime import datetime

# -------- DATABASE CONNECTION --------
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Qwerty@123",   
        database="password_tool"
    )
    cursor = db.cursor()
except Exception as e:
    print("Database connection failed!")
    print("Error:", e)
    exit()


# -------- PASSWORD GENERATION FUNCTION --------
def generate_password(length, use_upper, use_lower, use_numbers, use_symbols):
    characters = ""

    if use_lower:
        characters += string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*()"

    if characters == "":
        print("❌ Please select at least one option!")
        return None

    password = ""
    for i in range(length):
        password += random.choice(characters)

    return password


# -------- SAVE PASSWORD TO DATABASE --------
def save_to_db(password, length, u, l, n, s):
    query = """
    INSERT INTO passwords (password, length, has_upper, has_lower, has_numbers, has_symbols, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (password, length, u, l, n, s, datetime.now())

    cursor.execute(query, values)
    db.commit()


# -------- VIEW HISTORY --------
def view_history():
    cursor.execute("SELECT * FROM passwords")
    records = cursor.fetchall()

    print("\n----- Saved Passwords -----")
    for row in records:
        print(row)


# -------- MAIN PROGRAM --------
while True:
    print("\n🔐 PASSWORD GENERATOR CLI TOOL")
    print("1. Generate Password")
    print("2. View History")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        try:
            length = int(input("Enter password length: "))
        except:
            print("Invalid input!")
            continue

        upper = input("Include Uppercase? (y/n): ") == "y"
        lower = input("Include Lowercase? (y/n): ") == "y"
        numbers = input("Include Numbers? (y/n): ") == "y"
        symbols = input("Include Symbols? (y/n): ") == "y"

        password = generate_password(length, upper, lower, numbers, symbols)

        if password:
            print("\n✅ Generated Password:", password)

            save = input("Save to database? (y/n): ")
            if save == "y":
                save_to_db(password, length, upper, lower, numbers, symbols)
                print("💾 Saved successfully!")

    elif choice == "2":
        view_history()

    elif choice == "3":
        print("Exiting...")
        break

    else:
        print("Invalid choice!")
