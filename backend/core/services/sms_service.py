import requests
from backend.app.config import config


class SMSService:
    base_url = config.sms.api_url

    def __get_token(self):
        data = requests.post(
            url=f"{self.base_url}/auth/login/",
            data={
                "email": config.sms.auth_email,
                "password": config.sms.auth_secret_key,
            },
        )
        res = data.json()
        return res["data"]["token"]

    def send_message(self, phone_number, message):
        token = self.__get_token()
        payload = {"mobile_phone": phone_number, "message": message, "from": "4546"}
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.post(
            url=f"{self.base_url}/message/sms/send", headers=headers, data=payload
        )
        print(res)
