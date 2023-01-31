# Commandline Arguments
I'm basically just going to take the output given, and re-organize it into a class for the validation functions. And add a __name__ == 'main' clause to be run as a standalone script.

I'm also going to replace full imports with just the required module classes to trim on memory usage.

  * [Opening question of arguments](#opening-question)
  * [Add file validation for cli args](#add-file-validation-for-cli-args)


# Opening question

## Question:
```
I'm making a python3 script. I want to use command-line arguments with the module "ArgParser" to take user input, and then validate that the are the requested data types. I want to use the following arguments: "-h","--hex" for a hexadecimal pattern, "-r","--regex" for a regex pattern, "-f","--file" for an input file, "-s","--string" for strings
```

## Response:

Sure, you can add a function to validate the file called "validate_file" to check if the file exists and is accessible for reading. Here is an example of how you can do that:

```python
import os

def validate_file(value):
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError("Invalid file")
    if not os.access(value, os.R_OK):
        raise argparse.ArgumentTypeError("File is not readable")
    return value

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True, type=validate_file,
                    help="input file")
parser.add_argument("-s", "--string", required=True, type=str,
                    help="search string")
parser.add_argument("-h", "--hex", required=False, type=validate_hex,
                    help="search for a hex pattern")
parser.add_argument("-r", "--regex", required=False, type=validate_regex,
                    help="search for a regular expression pattern")

args = parser.parse_args()
```
This script uses the os.path.isfile() function to check if the file exists and the os.access() function to check if the file is readable. If either of these checks fail, the argparse.ArgumentTypeError is raised with an appropriate error message. If the file is valid, the function returns the file path.

You can run this script with the following command:

```python
python script.py -f input.txt -s "search string" -h "hex pattern" -r "regex pattern"
```

The script will parse the command line arguments and validate the data types of the arguments based on the validate functions.
It will also validate the file and check if it's valid by using validate_file function.
You can then access the values of the arguments by their names, for example, args.file or args.string.
You can also add some logic to the script to check if the user specified the hex or the regex pattern, and if so, use the appropriate search function to search the file.

# Add file validation for cli args
## Question
```
Could you also add a function to validate the file called "validate_file?"
```

## Response
Sure, you can add a function to validate the file called "validate_file" to check if the file exists and is accessible for reading. Here is an example of how you can do that:

```python
import os

def validate_file(value):
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError("Invalid file")
    if not os.access(value, os.R_OK):
        raise argparse.ArgumentTypeError("File is not readable")
    return value

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True, type=validate_file,
                    help="input file")
parser.add_argument("-s", "--string", required=True, type=str,
                    help="search string")
parser.add_argument("-h", "--hex", required=False, type=validate_hex,
                    help="search for a hex pattern")
parser.add_argument("-r", "--regex", required=False, type=validate_regex,
                    help="search for a regular expression pattern")

args = parser.parse_args()
```

This script uses the os.path.isfile() function to check if the file exists and the os.access() function to check if the file is readable. If either of these checks fail, the argparse.ArgumentTypeError is raised with an appropriate error message. If the file is valid, the function returns the file path.

You can run this script with the following command:

```python
python script.py -f input.txt -s "search string" -h "hex pattern" -r "regex pattern"
```

The script will parse the command line arguments and validate the data types of the arguments based on the validate functions.
It will also validate the file and check if it's valid by using validate_file function.
You can then access the values of the arguments by their names, for example, args.file or args.string.
You can also add some logic to the script to check if the user specified the hex or the regex pattern, and if so, use the appropriate search function to search the file.


