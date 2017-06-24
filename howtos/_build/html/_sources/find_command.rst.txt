Find Command
=====================

1. Change permission of all files in current directory tree to 644
::

  find ./ -type f -exec chmod 644 {} \;

2. Change permission of all folders in current directory tree to 755
::

  find ./ -type d -exec chmod 755 {} \;

3. Find files consuming size greater than 100 MB in a single drive
::

  find / -xdev -size +100000k

4. Find folder taking up all inodes
::

  find / -xdev -printf '%h\n' | sort | uniq -c | sort -k 1 -n

5. Delete a file using inode number
::

  find . -inum [inode-number] -exec rm -i {} \;
