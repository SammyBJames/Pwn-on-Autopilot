import json

# Load the data from 1_data.json
# We use .load() because we are reading from a file object
with open('1_data.json') as f:
    data = json.load(f)

# Print the admin's password from the dictionary
print(f'Admin password: {data["credentials"]["admin"]}')

# Add a new user 'backdoor' with password 'pwned'
data['credentials']['backdoor'] = 'pwned'

# Save the modified data to a file called 1_modified.json
with open('1_modified.json', 'w') as f:
    json.dump(data, f, indent=4)
