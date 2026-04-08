# argparse

When you want to test payloads fast, or build reusable tools, you need to stop hardcoding IPs, payloads, and other parameters. `argparse` is Python's built-in module for building proper CLIs. It automatically generates help menus (`-h`) and validates user input for you.

## The Setup
To build a CLI tool, you create an `ArgumentParser`, add your expected arguments, and then parse whatever the user typed in the terminal.

```python
from argparse import ArgumentParser

# Initialize the parser
parser = ArgumentParser(description='My CLI tool for hacking')

# Add arguments
parser.add_argument('target', help='The target URL')

# Parse the arguments from the command line
args = parser.parse_args()

print(f'Target: {args.target}')
```

## Types of Arguments

### Positional Arguments (Required)
These are mandatory and depend on the order the user types them. They do not start with dashes.

```python
# The user MUST provide this, e.g. `python script.py http://target.local`
parser.add_argument('target', help='The target IP or URL')
```

### Optional Arguments (Flags)
These start with one or two dashes (e.g., `-w` or `--wordlist`). They are usually optional, so you should provide a `default` value, or explicitly mark them as `required=True`.

```python
# The user can provide -w words.txt or --wordlist words.txt
parser.add_argument('-w', '--wordlist', default='common.txt', help='Path to the wordlist')

# Enforce a specific data type (argparse handles the conversion and validation)
parser.add_argument('-p', '--port', type=int, default=80, help='Target port number')

# Forcing a flag to be mandatory
parser.add_argument('-u', '--username', required=True, help='Username to brute-force')
```

### Boolean Flags
Often, you just want to turn a feature on or off (like verbose logging). You don't want the user to type `--verbose True`, you just want them to pass `-v`. You achieve this using the `action='store_true'` parameter.

```python
# If the user passes -v or --verbose, args.verbose becomes True. Otherwise, False.
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
```

### Taking Multiple Values (`nargs`)
Sometimes you want users to pass a list of items rather than a single string. `nargs` allows an argument to consume multiple inputs from the command line and group them into a Python list.

- `nargs='+'`: Gathers 1 or more arguments into a list. Fails if 0 are provided.
- `nargs='*'`: Gathers 0 or more arguments.

```python
# User types: python script.py --ports 80 443 8080
parser.add_argument('--ports', nargs='+', type=int, help='List of ports to scan')

# args.ports will be: [80, 443, 8080]
```


### Handling Files (`argparse.FileType`)
If your tool requires an input file or an output file, you don't need to manually check if the file exists and open it yourself. `argparse` can do it for you inline:

```python
# This automatically opens the file for reading ('r'). 
# If the file doesn't exist, argparse prints an error to the user.
parser.add_argument('-w', '--wordlist', type=argparse.FileType('r'), required=True)

args = parser.parse_args()

# args.wordlist is already an open file object
for word in args.wordlist:
    print(f'Trying: {word.strip()}')
```

### Restricting Choices (`choices=[]`)
If your script only supports a specific list of attack vectors (like 'ssh', 'ftp', or 'http'), you can force the user to pick one of those directly in the argument setup.

```python
# If the user types anything but 'ssh', 'ftp', or 'http', argparse errors and shows the valid options.
parser.add_argument('-m', '--module', choices=['ssh', 'ftp', 'http'], required=True)
```

### How Argument Names are Determined (`dest=`)
By default, `argparse` creates the attribute name on the `args` object based on the flags you define:
1. It looks for the first "long" flag (e.g., `--user-name`).
2. It strips the dashes and converts inline dashes to underscores: `args.user_name`.
3. If only a short flag exists (`-u`), it uses the letter: `args.u`.

You can override this using the `dest=` parameter.

```python
# Even though the flag is --target-ip, the variable will just be args.ip
parser.add_argument('-t', '--target-ip', dest='ip', help='Target IP Address')
```

### Mutually Exclusive Groups
If your tool has options that conflict with each other (e.g., you can either scan a single IP *or* read a list of IPs from a file, but not both), you can enforce that logically.

```python
# If a user types `script.py --ip 1.1.1.1 --file targets.txt`, argparse will throw an error.
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--ip', help='A single target IP')
group.add_argument('--file', type=argparse.FileType('r'), help='File containing IPs')
```

### Custom Type Validators
Instead of just using `type=int`, you can pass your own custom functions to validate input before the script even runs. Throw an `argparse.ArgumentTypeError` to have `argparse` display the error and show the help menu automatically.

```python
import argparse
import re

def valid_ip(ip_str):
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip_str):
        raise argparse.ArgumentTypeError(f"'{ip_str}' is not a valid IP!")
    return ip_str

# If user types --ip 999.abc, argparse will handle the error
parser.add_argument('--ip', type=valid_ip, required=True)
```
