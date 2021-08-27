import os, shutil
from datetime import datetime

print("My working path is ", os.getcwd())
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M")

originName = 'esp-rssi-measurements-sqlite.db'
newName = 'esp-rssi-measurements-sqlite_'+timestamp+'.db'

print("originName: ", originName)
print("newName: ", newName)

os.rename(os.getcwd()+'/'+originName, os.getcwd()+'/'+newName)

shutil.move(os.getcwd()+'/'+newName, os.getcwd()+'/DB_records/'+newName)