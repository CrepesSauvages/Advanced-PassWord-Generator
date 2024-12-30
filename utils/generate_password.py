import random
import string
import logging
import argparse
import pyperclip
import json
import csv

def generate_password(length=12, min_uppercase=1, min_digits=1, min_special_chars=1):
    logging.info('Generating password...')
    if length < (min_uppercase + min_digits + min_special_chars):
        raise ValueError("Password length must be at least equal to the sum of minimum required character types.")

    password = []
    password += [random.choice(string.ascii_uppercase) for _ in range(min_uppercase)]
    password += [random.choice(string.digits) for _ in range(min_digits)]
    password += [random.choice(string.punctuation) for _ in range(min_special_chars)]
    
    remaining_length = length - len(password)
    all_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    password += [random.choice(all_characters) for _ in range(remaining_length)]
    random.shuffle(password)
    return ''.join(password)