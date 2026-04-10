# Quick Maths Write Up

## Why Scripting?
The challenge requires us to answer 100 math equations in under 5 seconds. You can't do that. You can with Python!

## Intended Solution

### 1. Connecting to the Process
When we first connect to the server, it prints out an introduction text and then starts asking us 100 math questions. After 5 seconds pass or we get a question wrong, the server closes the connection. We'll have to use a script to be faster.

### 2. Getting Started
Let's connect to the process with `pwntools` and start receiving some of the output so we can isolate the questions.

```python
from pwn import *

# Connect to the remote server
p = remote('math.inmt.win', 8001)

# Skip the introduction text
p.recvuntil(b'Go!\n\n')
```

### 3. Setting Up a Loop
We know there are 100 questions, so we can set up a `for` loop to repeat 100 times and answer each question. We can then parse out the math questions and send our answers.

```python
for _ in range(100):
    # Read the question line and decode to a string
    question_line = p.recvline().decode()
```

### 4. Parsing and Calculating
Now we need to extract the actual equation from a string like `"Question 1: What is 19 * 11?\n"`. Let's use Python's `strip`, `split`, and `replace` methods to isolate just the equation.

We can then split the equation into its two operands and the operator. We can use a simple dictionary to map the operator symbol to the corresponding Python function from the `operator` module.

```python
from pwn import *
from operator import add, sub, mul

for _ in range(100):
    # Read the question line and decode to a string
    question_line = p.recvline().decode()

    # Parse the math equation from the line
    q_part = question_line.strip().split('What is ')[1].replace('?', '')
    q_split = q_part.split()
    operators = {'+': add, '-': sub, '*': mul}
    ans = operators[q_split[1]](int(q_split[0]), int(q_split[2]))
```

### 5. Sending the Answer
Now that we have the answer calculated, we can send it back to the process. The server sends an "Answer: " prompt after each question, so we can use `sendlineafter` to wait for that before sending our response.

```python
    # Send the answer after the prompt
    p.sendlineafter(b'Answer: ', str(ans).encode())
```

Once the loop completes 100 times, we simply read the rest of the output (which contains the flag)!

```python
# Print the rest of the output (the flag)
print(p.recvall().decode())
```

## Solution Script

```python
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
```
