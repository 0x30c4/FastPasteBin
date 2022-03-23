from os import environ

title = "Fast Paste Bin"
origins = ["https://pastebin.0x30c4.dev"]
db_url = environ["DB_URL"]
BIN_UPLOAD = environ["UPLOAD_BIN"]
APP_URL = environ["APP_URL"]
APP_URL_INDEX = environ["APP_URL_INDEX"]
APP_URL_UBIN = environ["APP_URL_UPLOAD"]

LOG_INI = environ["LOG_INI"]

version = environ["VERSION"]

description = '''
## Why Use FastPasteBin?
This is a simple Paste Bin service made with the FastApi and PostGresDB.
The main focuses was to create a Paste Bin that you can use from your terminal
and also which is fast and easy to use.

You can upload your **code/message/error output/encrypted message** here to
quicly share it with others to use or view it.

It also has an API end-point.
'''

help_text = f"TL;DR: echo Hello world | curl -F 'file=@-' {APP_URL}"

terms_of_service = "https://pastebin.0x30c4.dev/terms"

license_info = {
        "name": "MIT License",
        "url": "https://raw.githubusercontent.com/0x30c4/FastPasteBin/main/LICENSE",
    }
contact = {
        "name": "Sanaf",
        "url": "https://0x30c4.dev",
        "email": "sanaf@0x30c4.dev",
    }
