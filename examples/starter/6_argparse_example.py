import argparse

# TODO: Initialize an ArgumentParser

# TODO: Add a required positional argument for the 'target' URL

# TODO: Add an optional flag '-w' / '--wordlist' with a default value of 'common.txt'

# TODO: Add an boolean option '-v' / '--verbose' using action='store_true'

# TODO: Parse the arguments

print(f'\n[*] Starting attack against: {args.target}')
print(f'[*] Loading wordlist: {args.wordlist}')

if args.verbose:
    print('[!] Verbose logging ENABLED. Showing all failed attempts.')
else:
    print('[*] Verbose logging DISABLED. Only showing successful hits.')
