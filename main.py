from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberOccupiedError
from telethon.tl.types import InputPhoneContact, User
from telethon.tl.functions.contacts import ImportContactsRequest
import pandas as pd
import time

# Replace the following values with your own credentials in a separate config file or environment variables
api_id = YOUR_API_ID
api_hash = "YOUR_API_HASH"
phone = "YOUR_PHONE_NUMBER"

# Connect to Telegram client
client = TelegramClient(phone, api_id, api_hash)


def add_and_check_contact(phone_number, first_name, last_name):
    """
    Add a contact to your Telegram account and check if the account exists.
    """
    try:
        # Create and import the contact
        contact = InputPhoneContact(client_id=0, phone=phone_number, first_name=first_name, last_name=last_name)
        result = client(ImportContactsRequest([contact]))

        # Get entity to check if it's a valid Telegram user
        user = client.get_entity(phone_number)
        if isinstance(user, User):
            print(f"Account found for name: {first_name} - phone_number: {phone_number}")
        else:
            print(f"No account found for {phone_number}")
    except PhoneNumberOccupiedError:
        print(f"Phone number {phone_number} is already registered.")
    except Exception as e:
        print(f"Error: {e} \n for name: {first_name} - phone_number: {phone_number}")


def read_excel(file_path='EXCEL.xlsx'):
    """
    Read phone numbers and names from an Excel file.
    """
    df = pd.read_excel(file_path)
    info = {}

    for index, row in df.iterrows():
        phone_number = '+98' + str(row['Phone_Number'])
        name = row['Name']
        info[name] = phone_number

    return info


# Start Telegram client
client.start()


def start():
    """
    Main function to start reading contacts and adding them.
    """
    info = read_excel()
    for name in info:
        add_and_check_contact(info[name], name, "user")
        time.sleep(5)


start()

