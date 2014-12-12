import os
import sys

num_tests = 5
proc_count = 0
proc_id = 0
db_names = ['bank.db', 'cred.db', 'userstring.db']

for i in range(num_tests):
    proc_count += 1
    pid = os.fork()
    if pid == 0: #child
        proc_id = proc_count
        break
    else: #parent
        if proc_count == num_tests:
            sys.exit(0)

def access_dbs(mode):
    for db in db_names:
        print str(proc_id) + ": Try to access " + db + " with mode " + mode
        try:
            f = open(db, mode)
            f.close()
            print str(proc_id) + ": Accessed: " + db
        except IOError:
            print str(proc_id) + ": Permission denied: " + db

if proc_id == 1:
    print str(proc_id) + ": Test 1: uid with no permissions"
    os.setuid(12468)
    access_dbs('r')
    access_dbs('w')
elif proc_id == 2:
    print str(proc_id) + ": Test 2: uid with permission to bank.db"
    os.setuid(61001)
    access_dbs('r')
    access_dbs('w')
elif proc_id == 3:
    print str(proc_id) + ": Test 3: uid with permission to cred.db"
    os.setuid(61000)
    access_dbs('r')
    access_dbs('w')
elif proc_id == 4:
    print str(proc_id) + ": Test 4: uid with permission to userstring.db"
    os.setuid(61002)
    access_dbs('r')
    access_dbs('w')
