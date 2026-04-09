import argparse

# Initialize an ArgumentParser
parser = argparse.ArgumentParser(description='Basic web content scanner')

# Add a required positional argument for the 'target' URL
parser.add_argument('target', help='The target URL')

# Add an optional flag '-w' / '--wordlist' with a default value of 'common.txt'
parser.add_argument('-w', '--wordlist', default='common.txt', help='Path to wordlist')

# Add an boolean option '-v' / '--verbose' using action='store_true'
parser.add_argument('-v', '--verbose', action='store_true', help='Show all attempts')

# Parse the arguments
args = parser.parse_args()

print(f'\nStarting attack against: {args.target}')
print(f'Loading wordlist: {args.wordlist}')

if args.verbose:
    print('Verbose logging ENABLED. Showing all failed attempts.')
else:
    print('Verbose logging DISABLED. Only showing successful hits.')
