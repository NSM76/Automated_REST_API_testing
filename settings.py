import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

not_valid_email = 'iujnon@mail.ru'
not_valid_password = "HjJKkLll"