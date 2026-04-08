# Error Handling

In many languages you are taught to "Look Before You Leap", checking conditions before performing an action.

With cyber, we are often dealing with unpredictable data and environments. Using error handling can make our scripts much simpler and more robust. Just try to perform the action, and if it fails, catch the error.

## The Basics: `try` / `except`
Instead of having your script crash 10-hours into your attack, wrap your code in a `try` block.

```python
for i in range(1000):
    try:
        # Code that might fail
        print(10 / i)
    except:
        # What to do if it fails so the script survives
        print('Something broke, but we keep running!')
```

## Catching Specific Errors
Avoid using a bare `except` clause when possible by reasoning about what exceptions your code could throw. A bare `except` will catch *everything*, including `Ctrl+C` (`KeyboardInterrupt`), making your script difficult to stop.

```python
for i in range(1000):
    try:
        # Code that might fail
        empty_dict = {}
        print(10 / i)
        print(empty_dict['nonexistent_key'])
    except ZeroDivisionError:
        # Handle ZeroDivisionError specifically
        print('Zero division occurred!')
    except ValueError:
        # Handle ValueError specifically
        print('Value error occurred!')
```

## Skip Failures (`pass`)
Often it is best to log the your errors for debugging, though sometimes you just want to ignore errors. Use `pass`.

```python
try:
    flag = mysterious_bytes.decode('utf-8')
    print(f'Found it: {flag}')
except UnicodeDecodeError:
    # Ignore the error and move on
    pass
```

## On Success (`else`)
The `else` block is executed only if the `try` block ran successfully without any errors. This helps keep your `try` blocks as small as possible so you can put only the code that might actually fail inside it. Subsequent logic can go inside the `else` block.

```python
try:
    # Put only the dangerous operation here
    response = requests.get('http://target.local/admin', timeout=2)
except requests.exceptions.Timeout:
    print('Target timed out! Moving on...')
else:
    # This runs only if the request succeeded
    print('Request successful! Searching for passwords...')
    if 'password' in response.text:
        print('Huzzah! Password!')
```

## Cleaning Up (`finally`)
The `finally` block runs no matter what, whether there was no error, a handled error, or an unhandled error. This is used to clean up resources, like closing network sockets or files.

```python
try:
    connect_to_target()
except Exception as e:
    print(f"Attack failed: {e}")
finally:
    print("Closing the socket before we exit...")
```
