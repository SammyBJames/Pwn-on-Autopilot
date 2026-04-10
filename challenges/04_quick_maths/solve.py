from pwn import *
from operator import add, sub, mul


def solve():
    # Connect to the remote server
    p = remote('math.inmt.win', 8001)

    # Skip the introduction text
    p.recvuntil(b'Go!\n\n')

    # Loop 100 times to answer all questions
    for _ in range(100):
        # Read the question line and decode to a string
        question_line = p.recvline().decode()
        
        # Parse the math equation from the line
        q_part = question_line.strip().split('What is ')[1].replace('?', '')
        q_split = q_part.split()
        operators = {'+': add, '-': sub, '*': mul}
        ans = operators[q_split[1]](int(q_split[0]), int(q_split[2]))

        # Send the answer after the prompt
        p.sendlineafter(b'Answer: ', str(ans).encode())

    # Print the rest of the output (the flag)
    print(p.recvall().decode())


if __name__ == '__main__':
    solve()
