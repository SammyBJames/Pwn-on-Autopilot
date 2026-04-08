# JSON Processing

JSON is the standard for data exchange on the web. You will interact with JSON constantly:

- REST API requests and responses
- Cloud configurations (AWS IAM policies)
- Tool outputs (BloodHound, Nmap, nuclei)
- Exfiltrated application data

Python's built-in `json` module translates seamlessly between JSON text and Python dictionaries/lists.

## The Rule of "S"
The `json` module has four main functions. The easiest way to remember which one to use is the **"S" stands for String**.
- `json.load()` / `json.dump()`: For reading/writing directly to **Files**.
- `json.loads()` / `json.dumps()`: For reading/writing from Python **Strings**.

## Strings: `loads` and `dumps`

When serializing or deserializing JSON data in string form, use `loads` and `dumps`.

```python
import json

json_string = '{"user": "admin", "id": 1, "is_admin": true}'

# Convert string to Python dictionary
data = json.loads(json_string)

print(data['user'])     # 'admin'
print(data['is_admin']) # True

# Convert Python dictionary back to a JSON string
# indent=4 makes the output pretty and readable
new_json_string = json.dumps(data, indent=4)
```

## Files: `load` and `dump`

When reading or writing files, use `load` and `dump` inside your `with open()` context manager.

```python
import json

# Reading from a file
with open('some_data.json') as f:
    data = json.load(f)

# Modifying the data (dictionary)
data['domain'] = 'malicious.net'

# Writing back to a file
with open('some_data.json', 'w') as f:
    json.dump(data, f, indent=4)
```

## Handling Errors
If you try to `.loads()` a string that isn't valid JSON (e.g., the web server returned a 404 HTML page instead of the expected JSON API response), Python will throw a `json.decoder.JSONDecodeError`. 

Always handle your errors!

```python
import json

bad_response = '<html><body>Not Found</body></html>'

try:
    data = json.loads(bad_response)
except json.JSONDecodeError:
    print('Target did not return valid JSON!')
```

## Resources
- [Official `json` Documentation](https://docs.python.org/3/library/json.html)
- [Working with JSON Data in Python (Real Python)](https://realpython.com/python-json/)
