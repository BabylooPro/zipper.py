zipper.py
=========


https://github.com/BabylooPro/zipper.py/assets/35376790/6286cd6f-4d00-4bf2-823f-7b69df5a7031


Description
-----------

`zipper.py` is a Python script that allows you to create and extract zip archives from a chosen directory.

It offers a console user interface to choose the directories to zip. In addition, it displays a progress bar during the creation and extraction of archives, allowing the user to follow the progress of these operations.

If an archive with the same name already exists, the script offers the user to extract it.

Usage
-----

To use `zipper.py`, simply launch the Python script from the console:

```
python zipper.py
```

Then, the script will list all the directories in the current directory and invite you to choose the directory(s) to zip. Enter the numbers corresponding to the directories separated by spaces. For example, to choose directories 1 and 3, enter:

```
2 3
```

If you want to quit the script, type 'exit'.

Once you have made your choice, the script creates a zip archive with the directory name. If an archive with the same name already exists, the script will ask you if you want to extract its contents. You can answer 'yes' or 'no'.

Functions
---------

`zipper.py` contains the following functions:

*   `clear_console()`: Clears the console. Compatible with Windows and UNIX/Linux/MacOS.
*   `count_files(directory)`: Counts the number of files in a directory recursively.
*   `create_archive(archive_name, directory)`: Creates a zip archive from a directory.
*   `extract_archive(archive_name, target_directory)`: Extracts a zip archive to a target directory.

Limitations
-----------

This script does not handle errors related to file or directory access. For example, if you do not have read rights to a file, the script will fail.

Moreover, it does not handle archives compressed with algorithms other than `ZIP_DEFLATED`.
