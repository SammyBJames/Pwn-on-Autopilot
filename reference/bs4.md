# BeautifulSoup (bs4)

When writing web exploitation scripts, we need to interact with and extract data from HTML strings. `BeautifulSoup` turns HTML into cleanly searchable Python objects.

The two most common use cases are extracting CSRF tokens for brute-forcing scripts and scraping targets for links or hidden data.

## The Setup
You usually chain `bs4` directly with the `requests` library.

```python
import requests
from bs4 import BeautifulSoup

r = requests.get('http://target.local')

# Parse the raw HTML into a "soup" object
soup = BeautifulSoup(r.text, 'html.parser')
```

## Finding a Single Element (`find`)
We can use `.find()` to extract specific elements and values. It returns the first matching HTML tag. You can then treat the tag like a dictionary to pull out attributes like `value`, `href`, or `src`.

```python
# Look for a tag like: <input name="csrf_token" value="abc123xyz">
# We specify the HTML tag 'input' and a dictionary of attributes to match
token_input = soup.find('input', {'name': 'csrf_token'})

if token_input:
    # Extract the 'value' attribute using .get()
    token = token_input.get('value')
    print(f'CSRF Token: {token}')
```

## Finding Multiple Elements (`find_all`)
If you are building a custom crawler or scraping a page for data (like grabbing all the links to map an application), use `.find_all()`. This returns a list of all matching items.

```python
# Find all <a> tags
all_links = soup.find_all('a')

for link in all_links:
    # Extract the 'href' attributes using .get()
    destination = link.get('href')
    print(destination)
```

## Advanced Searching (CSS Selectors)
If you're comfortable with CSS, you can use `.select()` (returns a list) and `.select_one()` (returns the first match) to find elements with CSS selectors.

```python
# Find the first button with the class 'btn-primary' inside a form with ID 'login'
login_btn = soup.select_one('form#login .btn-primary')

# Find all <a> tags inside any <div> with the class 'sidebar'
sidebar_links = soup.select('div.sidebar a')
```

## Navigating the DOM Tree
Often, elements like `<input>` fields don't have unique IDs or classes. To find them, you first find a nearby element you *can* identify (like a `<label>`), and then navigate relative to it.

`bs4` `Tag` objects have several useful built-in navigation methods:

*   **`.find_parent()`** / **`.find_parents()`**: Searches up the tree from the current element.
*   **`.find_next_sibling()`** / **`.find_previous_sibling()`**: Searches elements on the exact same level of the tree.
*   **`.find_next()`** / **`.find_previous()`**: Searches whatever parses immediately before or after this tag, regardless of nesting.
*   **`.contents`** / **`.children`**: `.contents` returns a list of the tag's direct children, while `.children` returns an iterator (more memory efficient).
*   **`.descendants`**: Returns a generator traversing down through all sub-elements inside the tag (children, grandchildren, etc.).

```python
# Find the label that contains the text 'Password:'
pass_label = soup.find('label', string='Password:')

# Jump to the next <input> tag right after this label
pass_input = pass_label.find_next('input')

# Jump up out of the current element to its parent <div>
parent_container = pass_input.find_parent('div')

# Iterate over the direct children of the container
for child in parent_container.children:
    if child.name is not None:  # Skips non-tag elements
        print(f'Child tag: {child.name}')
```

## Extracting Data from a Tag
When you successfully find an element, you need to pull data out of it. 

*   **Attributes:** `Tag`s work like a Python dictionary. Use `.get('attribute_name')` to avoid `KeyError`s if the attribute doesn't exist.
*   **Text:** Use `.text` or `.get_text()` to extract only the human-readable text inside the tag, stripped of all HTML formatting.

```python
tag = soup.find('div', {'id': 'user-profile'})

# Extracting an attribute
user_role = tag.get('data-role', 'Unknown') 

# Extracting all human-readable text
# strip=True removes whitespace
profile_text = tag.get_text(separator=' ', strip=True) 
```
