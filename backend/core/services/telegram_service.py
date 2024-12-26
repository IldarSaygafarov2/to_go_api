import json
import httpx

from backend.app.config import config

base_url = "https://api.telegram.org/bot{bot_token}/{method}"


class TelegramService:
    def __generate_confirm_keyboard(self, user_id: int):
        kb = {
            "inline_keyboard": [
                [
                    {"text": "Ответить", "callback_data": f"answer:{user_id}"},
                ]
            ],
        }
        return json.dumps(kb)

    async def send_message(self, telegram_chat_id: int, message: str, **kwargs):
        params = {
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "HTML",
            "reply_markup": self.__generate_confirm_keyboard(
                user_id=kwargs.get("user_id")
            ),
        }

        url = base_url.format(bot_token=config.telegram.token, method="sendMessage")

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=params)
            print(response.json())
