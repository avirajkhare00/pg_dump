import os
import sys
import subprocess
from datetime import datetime
import json

def create_pg_dump():

    config_values = json.loads(open('config/config.json',  'r').read())

    DB_USER = config_values['pg_dump_modules']['db_user']
    DB_NAME = config_values['pg_dump_modules']['db_name']

    BACKUP_PATH = config_values['pg_dump_modules']['backup_path']

    FILENAME_PREFIX = config_values['pg_dump_modules']['backup_file_name_prefix']

    now = datetime.now()

    filename = None

    day_of_year = str(now.timetuple().tm_yday).zfill(3)

    filename = '%s.d%s' % (FILENAME_PREFIX, day_of_year)

    destination = r'%s/%s' % (BACKUP_PATH, filename)
    
    #print 'Backing up %s database to  %s' %s (DB_NAME, destination)


    ps = subprocess.Popen(
        ['pg_dump', '-U', DB_USER, '-Fc', DB_NAME, '-f', destination],
        stdout=subprocess.PIPE
    )

    output = ps.communicate()[0]

    for line in output.splitlines():

        print line

    print 'Starting to upload %s on Google Drive...' % filename

    return destination