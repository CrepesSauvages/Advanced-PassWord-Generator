import random
import string
import logging
import argparse
import pyperclip
import json
import csv
from utils.generate_password import generate_password

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_input(prompt, default=True):
    while True:
        user_input = input(prompt).lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        elif user_input == '':
            return default
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def get_password_length():
    while True:
        try:
            length = int(input("Enter the desired password length (min 8): "))
            if length < 8:
                print("Password length should be at least 8 characters.")
            else:
                return length
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_password_requirements():
    min_uppercase = int(input("Minimum number of uppercase letters: "))
    min_digits = int(input("Minimum number of digits: "))
    min_special_chars = int(input("Minimum number of special characters: "))
    return min_uppercase, min_digits, min_special_chars

def save_password(password, filename="password.txt"):
    save = validate_input("Save password to file? (y/n): ", False)
    if save:
        with open(filename, "w") as file:
            file.write(password)
        print(f"Password saved to {filename}")
    else:
        print("Password not saved")

def copy_password_to_clipboard(password):
    copy = validate_input("Copy password to clipboard? (y/n): ", False)
    if copy:
        pyperclip.copy(password)
        print("Password copied to clipboard")

def check_password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    strength = "Weak"
    if length >= 12 and has_upper and has_lower and has_digit and has_special:
        strength = "Strong"
    elif length >= 8 and (has_upper or has_lower) and (has_digit or has_special):
        strength = "Moderate"
    
    return strength

def save_password_to_history(password, history_file="password_history.txt"):
    with open(history_file, "a") as file:
        file.write(password + "\n")
    logging.info(f"Password saved to history file: {history_file}")

def export_passwords_to_json(passwords, filename):
    with open(filename, 'w') as file:
        json.dump(passwords, file, indent=4)
    logging.info(f"Passwords exported to JSON file: {filename}")

def export_passwords_to_csv(passwords, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Password"])
        for password in passwords:
            writer.writerow([password])
    logging.info(f"Passwords exported to CSV file: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Password Generator')
    parser.add_argument('-l', '--length', type=int, default=0, help='Password length')
    parser.add_argument('-u', '--min-uppercase', type=int, default=1, help='Minimum number of uppercase letters')
    parser.add_argument('-d', '--min-digits', type=int, default=1, help='Minimum number of digits')
    parser.add_argument('-s', '--min-special', type=int, default=1, help='Minimum number of special characters')
    parser.add_argument('-f', '--file', action='store_true', help='Save password to file')
    parser.add_argument('-c', '--clipboard', action='store_true', help='Copy password to clipboard')
    parser.add_argument('-m', '--multiple', type=int, help='Generate multiple passwords')
    parser.add_argument('-o', '--output', type=str, help='Output file name')
    parser.add_argument('-b', '--batch', type=str, help='Batch mode: specify a JSON file with parameters')
    parser.add_argument('-e', '--export', type=str, choices=['json', 'csv'], help='Export passwords to JSON or CSV file')
    args = parser.parse_args()

    logging.info('Starting password generation process')

    passwords = []

    if args.batch:
        with open(args.batch, 'r') as file:
            batch_params = json.load(file)
        for params in batch_params:
            length = params.get('length', 12)
            min_uppercase = params.get('min_uppercase', 1)
            min_digits = params.get('min_digits', 1)
            min_special_chars = params.get('min_special', 1)
            password = generate_password(length, min_uppercase, min_digits, min_special_chars)
            passwords.append(password)
            print(f"Generated password: {password}")
            print(f"Password strength: {check_password_strength(password)}")
            save_password_to_history(password)
            if params.get('file', False):
                filename = params.get('output', "password.txt")
                save_password(password, filename)
            if params.get('clipboard', False):
                copy_password_to_clipboard(password)
    else:
        if args.length == 0:
            print("Interactive mode:")
            length = get_password_length()
            min_uppercase, min_digits, min_special_chars = get_password_requirements()
        else:
            length = args.length
            min_uppercase = args.min_uppercase
            min_digits = args.min_digits
            min_special_chars = args.min_special

        password = generate_password(length, min_uppercase, min_digits, min_special_chars)
        passwords.append(password)
        print(f"Generated password: {password}")
        print(f"Password strength: {check_password_strength(password)}")
        save_password_to_history(password)

        if args.file or validate_input("Save password to file? (y/n): ", False):
            filename = args.output if args.output else "password.txt"
            save_password(password, filename)
        if args.clipboard or validate_input("Copy password to clipboard? (y/n): ", False):
            copy_password_to_clipboard(password)
            
        num_passwords = args.multiple or (int(input("Enter the number of passwords to generate: ")) if validate_input("Generate multiple passwords? (y/n): ", False) else 0)

        for _ in range(num_passwords):
            password = generate_password(length, min_uppercase, min_digits, min_special_chars)
            passwords.append(password)
            print(f"Generated password: {password}")
            print(f"Password strength: {check_password_strength(password)}")
            save_password_to_history(password)
            if args.file or validate_input("Save password to file? (y/n): ", False):
                filename = args.output if args.output else "password.txt"
                save_password(password, filename)
            if args.clipboard or validate_input("Copy password to clipboard? (y/n): ", False):
                copy_password_to_clipboard(password)

    if args.export:
        export_filename = args.output if args.output else f"passwords.{args.export}"
        if args.export == 'json':
            export_passwords_to_json(passwords, export_filename)
        elif args.export == 'csv':
            export_passwords_to_csv(passwords, export_filename)

    logging.info('Password generation process completed')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
