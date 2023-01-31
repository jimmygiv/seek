# Installation
For installation I want to copy seek.py to one of the writeable paths in $PATH. This will enable commandline usage of just 'seek' instead of having to navigate to downloaded git directory.
 * [Inital Description](#inital-description)
 * [Refine add_to_path](#refine-add_to_path)
 * [Add Executable Permissions](#add-executable-permissions)

# Inital Description
## Question
```
I want to make a setup script for this file. I want it to detect the os type (Linux, or Windows). And then add the script file "seek.py" to one of the filepaths writeable in $PATH
```

## Response
You can use the platform module in python to detect the operating system type, and then use the os module to add the script file to one of the file paths in the $PATH environment variable. Here's an example of a setup script that does this:

```python
import platform
import os

def add_to_path(file_path):
    if platform.system() == "Windows":
        os.environ['Path'] += f';{file_path}'
    elif platform.system() == "Linux":
        os.environ['PATH'] += f':{file_path}'

def setup():
    # Replace the path with the path to your script file
    script_file = '/path/to/seek.py'
    add_to_path(os.path.dirname(os.path.abspath(script_file)))

if __name__ == '__main__':
    setup()
```

This setup script uses the platform.system() function to detect the operating system type and sets the $PATH environment variable accordingly. The add_to_path function takes the file path as an argument and adds it to the $PATH environment variable. The setup function is then called to add the path to the script file to the $PATH environment variable.

Please note that this is just a sample and you may need to adjust it to suit your specific needs and requirements.

# Refine add_to_path
## Question
```The script above adds a filepath to $PATH. I want to check for writeable directories, and copy the script into that directory```

## Response
You can modify the add_to_path function to check for writeable directories in the $PATH environment variable and copy the script file to the first writeable directory it finds. Here's an example:

```python
import platform
import os
import shutil

def add_to_path(file_path):
    path_dirs = os.environ['PATH'].split(os.pathsep)
    for dir in path_dirs:
        try:
            with open(os.path.join(dir, 'test.txt'), 'w') as f:
                f.write('')
            os.remove(os.path.join(dir, 'test.txt'))
            shutil.copy(file_path, dir)
            print(f"Copied {file_path} to {dir}")
            return
        except (OSError, PermissionError):
            pass
    print(f"No writeable directories found in $PATH")

def setup():
    # Replace the path with the path to your script file
    script_file = '/path/to/seek.py'
    add_to_path(script_file)

if __name__ == '__main__':
    setup()

```

In this modified version of the script, the add_to_path function first splits the $PATH environment variable into a list of directories using os.pathsep. It then iterates over each directory and tries to write a test file to the directory using open and os.remove. If it is successful, it copies the script file to the directory using shutil.copy and returns. If no writeable directories are found, it prints an error message.

# Add Executable Permissions
## Question
```In the script above, how would I make the copied file have executable permissions?```

## Response
You can modify the add_to_path function to add executable permissions to the copied file by using the os.chmod function. Here's an example:

```python
import platform
import os
import shutil

def add_to_path(file_path):
    path_dirs = os.environ['PATH'].split(os.pathsep)
    for dir in path_dirs:
        try:
            with open(os.path.join(dir, 'test.txt'), 'w') as f:
                f.write('')
            os.remove(os.path.join(dir, 'test.txt'))
            shutil.copy(file_path, dir)
            os.chmod(os.path.join(dir, os.path.basename(file_path)), 0o755)
            print(f"Copied {file_path} to {dir} with execute permission")
            return
        except (OSError, PermissionError):
            pass
    print(f"No writeable directories found in $PATH")

def setup():
    # Replace the path with the path to your script file
    script_file = '/path/to/seek.py'
    add_to_path(script_file)

if __name__ == '__main__':
    setup()

```
In this modified version of the script, after copying the file using shutil.copy, the os.chmod function is called with the 0o755 argument to set the execute permission for the owner and group, and read permission for all others. The os.path.basename function is used to extract the name of the script file from the file path.
