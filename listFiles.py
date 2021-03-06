import fnmatch
import os
import time
from glob import glob
from os import chdir
from datetime import datetime, timedelta


def last_sunday():  # UD Bauru Rule - Servers reboot every Sunday, so let's don't delete sunday files
    local_time = datetime.today().weekday()
    if local_time == 0:  # 0 is monday. Last sunday is -1 day
        is_deletable = datetime.now() - timedelta(days=1)
    elif local_time == 1:  # 1 is tuesday. Last sunday is -2 days
        is_deletable = datetime.now() - timedelta(days=2)
    elif local_time == 2:  # 2 is wednesday. Last sunday is -3 days
        is_deletable = datetime.now() - timedelta(days=3)
    elif local_time == 3:  # 3 is thursday. Last sunday is -4 days
        is_deletable = datetime.now() - timedelta(days=4)
    elif local_time == 4:  # 4 is friday. Last sunday is -5 days
        is_deletable = datetime.now() - timedelta(days=5)
    elif local_time == 5:  # 5 is saturday. Last sunday is -6 days
        is_deletable = datetime.now() - timedelta(days=6)
    else:  # 6 is sunday. Last sunday is -7 days.
        is_deletable = datetime.now() - timedelta(days=7)
    return is_deletable


def write_log(deleted_files):
    with open('log_deleted_files.txt', 'a+') as log_file:
        log_file.seek(0)
        data = log_file.read(100)
        if len(data) > 0:
            log_file.write('\n')
        log_file.write("Executed: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')
        log_file.write("List of removed temp files: " + '\n')
        for reg in deleted_files:
            log_file.write(reg)
            log_file.write('\n')


directory = '//sgu/sgu/SGU'  # Set here your SGU folder
chdir(directory)
archives = []
tempFiles = glob('*.CDX') + glob('*.DBF') + glob('*.FPT')  # Extensions that are junk files

for file in tempFiles:
    if fnmatch.fnmatch(file, 'GX*'):  # All junk files starts with 'GX'
        if len(file) == 12:  # 'GX------.---' == 12 positions
            date_hour_file = (datetime.strptime(time.ctime(os.path.getctime(file)), "%a %b %d %H:%M:%S %Y"))
            localtime = time.asctime(time.localtime(time.time()))

            # The second "IF" remove all temp files since the last sunday.
            # If your Unimed want to remove only the files since last 7 days, comment
            # the first "IF" and uncomment the last one.

            # if date_hour_file <= (date_hour_file - timedelta(days=7)):
            if date_hour_file <= last_sunday():
                archives.append(file)
                os.remove(file)

write_log(archives)
print("Deleted Files: ")
print(archives)
