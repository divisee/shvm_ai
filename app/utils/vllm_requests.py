# utils/vllm_requests.py

# import asyncio
import aiohttp
from openai import OpenAI

BASE_SYSTEM_PROMPT = """Ты выступаешь в роли Психотерапевта из вселенной Гарри Поттера.
Твоя цель – оказать психологическую помощь и поддержку собеседникам, используя дружелюбный волшебный стиль общения с отсылками к магическому миру.
Можешь упоминать реалистичные детали о Хогвартсе, колдовских атрибутах, волшебных существах и заклинаниях, существующих в книгах и фильмах.
Ты говоришь вежливо, проявляешь эмпатию и предлагаешь советы, сохраняя атмосферу мира Гарри Поттера. Отвечай в несколько предложений, кратко."""

async def send_request_to_vllm(user_question: str) -> str:
    openai_api_key = "None"
    openai_api_base = "http://model_service:8000/v1"# http://localhost:8000/v1" #

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    chat_response = client.chat.completions.create(
        model="divisee/Magic-psy-LoRA-Qwen-Finetuned",
        messages=[
            {"role": "system", "content": BASE_SYSTEM_PROMPT},
            {"role": "user", "content": user_question},
        ],
        temperature=0.7,
        top_p=0.8,
        max_tokens=512,
        extra_body={
            "repetition_penalty": 1.05,
        },
    )
    print(chat_response)
    return chat_response.choices[0].message.content

# async def send_request_to_vllm(user_question: str) -> str:
#     """Отправка запроса к VLLM API и получение ответа"""
#     api_url = "http://model_service:8000/v1/chat/completions"  # изза Compose не обязательно указывать 81.94.158.229
#     payload = {
#         "model": "divisee/Magic-psy-LoRA-Qwen-Finetuned",
#         "messages": [
#             {"role": "system", "content": BASE_SYSTEM_PROMPT},
#             {"role": "user", "content": user_question}
#         ],
#         "temperature":0.7,
#         "top_p":0.8,
#         "max_tokens":512,
#         "repetition_penalty":1.05,
#         "do_sample": True
#     }


#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.post(api_url, json=payload) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     print(data)
#                     if "response" in data:
#                         return data["response"]
#                     else:
#                         return "Ошибка: Ключ 'response' отсутствует в ответе API."
#                 else:
#                     return f"Ошибка: API вернул статус {response.status}"
#         except aiohttp.ClientConnectionError as e:
#             return f"Ошибка подключения к Мудрецу" # API: {str(e)}"
#         except aiohttp.ClientPayloadError as e:
#             return f"Ошибка в данных запроса/ответа: {str(e)}"
#         except aiohttp.ClientError as e:
#             return f"Общая ошибка клиента: {str(e)}"
        





# if __name__ == "__main__":
#     asyncio.run(send_request_to_vllm("Мне кажется, я испытываю стресс из-за учёбы."))