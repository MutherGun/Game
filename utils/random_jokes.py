import requests

def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        if response.status_code == 200:
            data = response.json()
            return f"{data['setup']} ... {data['punchline']}"
        else:
            return "Dnes už žádný vtip, jsem unavený."
    except Exception:
        return "Nemůžu se připojit k internetu. Někdo změnil heslo na wifi."
