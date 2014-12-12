Running the demo application
============================

Simply download the repository and change directory into the demoApp directory. Then run 
```
sudo ./chroot-setup
``` 
to copy the necessary files to a /jail directory where we can modify permissions on copies of files rather than the originals. Change directories to /jail/AutoPS and run 
```
sudo python permissionsHelper.py
``` 
After that finishes executing, "cd .." and then run "sudo python repl.py" to spawn the client interface.

Config.txt
==========

There are some main components for specifying a configuration file. All lines have a prefix noting what the purpose of the line is ("Chroot: ", "Whitelist: ", etc). To specify a whitelist simply use the whitelist prefix followed by a comma separated list of things to not zero out permissions of when the Permissions Helper component runs. You can also specify a chroot directory using the chroot prefix. The other parts of the configuration file relate to actually specifying the design of the system. It is composed of blocks noting "groups". A group is a collection of processes that should run as the same user id. This is done by simply writing a line saying "Group" followed by an optional "Run as" prefix saying what uid it should run as. Then we list Process sections, which follows the form of a process prefix followed by the location of the file to run. The lines following are comma separated entries noting the files it needs read, write, and execute access to. All of those comma separated lists are optional. Below is an example configuration file. Note that all paths listed should be relative to the chroot directory if specified, else absolute paths.

```
Chroot: /jail/
Whitelist: dev/, usr/

Group
Run as: 60000
Process: foo.py
Reads: file1.txt
Writes: db1.db

Process: bar.py
Reads: file2.txt, file3.txt
Executes: testProgram

Group
Process: baz.sh
```

AutoPSMonitor
=============

Fanotify allows the user to set a directory as a mount point to watch.

Use the following command to set a mount point:
```
sudo mount --bind <dir> <dir>
```

Then run:
```
sudo ./logger
```

Output is created in logger's parent directory, in map.txt and log.txt.
map.txt contains (pid, process name) pairs in the format:
```
<pid>: <process name>
```
log.txt contains file access events in the format:
```
<filename> <"read"/"modified"/"opened"/"closed"> by process <pid>.
```

Visualization
=============

After fanotify is run, simply run:
```
python viewer.py
```

This will parse the fanotify logs to generate a view.html page, which will be automatically opened in a new tab in the user’s default browser.
