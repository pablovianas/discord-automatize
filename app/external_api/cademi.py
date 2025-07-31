
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CADEMI_API_BASE_URL = os.getenv("CADEMI_API_BASE_URL", "")

CADEMI_API_TOKEN = os.getenv("CADEMI_API_TOKEN", "")

def get_user_data(user_email: str):
    """
    Função para obter os dados do usuário a partir do e-mail.
    """
    url = f"{CADEMI_API_BASE_URL}/{user_email}"
    
    headers = {
        "Authorization": f"{CADEMI_API_TOKEN}",
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter dados do usuário: {response.status_code} - {response.text}")
            return None 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")
        return None