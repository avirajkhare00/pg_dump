import os
import sys
import subprocess
from datetime import datetime
from pg_dump_modules.create_pg_dump_module import create_pg_dump
from google_drive_modules.upload_file_to_drive import upload_to_drive


def main():

    upload_to_drive(create_pg_dump())


if __name__ == '__main__':
    main()