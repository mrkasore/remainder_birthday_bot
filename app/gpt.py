import requests, os

async def get_text_from_gpt(about_user, is_male):
    gender = 'женский'
    if is_male:
        gender = 'мужской'

    prompt = {
        "modelUri": f"gpt://{os.getenv("CATALOG_ID")}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "500"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты помогаешь написать текст поздравления с днем рождения основываясь на данных, которые ввел user о том человеке. "
                        f"Писать нужно от первого лица. Не надо оставлять место для имени. Пол именника - {gender}"
            },
            {
                "role": "user",
                "text": about_user
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {os.getenv('GPT_TOKEN')}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()

    return result["result"]["alternatives"][0]["message"]["text"]
