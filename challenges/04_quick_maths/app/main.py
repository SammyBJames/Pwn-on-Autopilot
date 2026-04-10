import random
import sys
import time


def generate_question():
    ops = ['+', '-', '*']
    op = random.choice(ops)
    
    if op == '*':
        a = random.randint(1, 20)
        b = random.randint(1, 20)
    else:
        a = random.randint(1, 500)
        b = random.randint(1, 500)
        
    ans = eval(f'{a}{op}{b}')
    return f'{a} {op} {b}', ans


def main():
    print('Welcome to Quick Maths!')
    print('I will ask you 100 questions. You have 5 seconds total.')
    print('Go!\n')
    sys.stdout.flush()
    
    start_time = time.time()
    
    for i in range(100):
        q, ans = generate_question()
        print(f'Question {i + 1}: What is {q}?')
        sys.stdout.write('Answer: ')
        sys.stdout.flush()
        
        try:
            user_input = sys.stdin.readline().strip()
        except EOFError:
            print('\nConnection closed.')
            return
            
        time_taken = time.time() - start_time
        if time_taken > 5.0:
            print(f'\nToo slow! You took {round(time_taken, 2)} seconds. The max is 5.')
            return
            
        try:
            if int(user_input) != ans:
                print(f'\nWrong! {q} is {ans}, not {user_input}.')
                return
        except ValueError:
            print('\nPlease enter valid numbers.')
            return
            
    print('\nCongratulations! You are a human calculator.')
    print(f'Time taken: {round(time.time() - start_time, 2)} seconds')
    print('Flag: bsides{qu1ck3st_m4th5_w35t_0f_th3_m1ss1551pp1}')


if __name__ == '__main__':
    main()
