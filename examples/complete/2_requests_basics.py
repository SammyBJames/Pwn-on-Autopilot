import requests

# Send a GET request to https://httpbin.org/json
response = requests.get('https://httpbin.org/json')

# Print the status code and the response text
print('Status Code:', response.status_code)
print('Response Text:', response.text)

# Print the response content as bytes
print('Response Content (bytes):', response.content)

# Print the response body as JSON
print('Response JSON:', response.json())

# Send a POST or PUT request to https://httpbin.org/post and print the status code
post_response = requests.post('https://httpbin.org/post')

# Print the status code of the POST request
print('POST Status Code:', post_response.status_code)
