import requests
from bs4 import BeautifulSoup

# Fetch the content of a form page
response = requests.get('http://quotes.toscrape.com/login')

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the CSRF token from the page and print it
csrf_input = soup.find('input', {'name': 'csrf_token'})
csrf_token = csrf_input.get('value')
print(f'CSRF Token: {csrf_token}')
