import requests

from app.dependencies import get_settings
from models.news import NewsInput
from models.users import UserRead


settings = get_settings()
api_url = settings.telegram_api_url
bot_token = settings.telegram_bot_token
channel_link = settings.telegram_channel_link


def post_news(n: NewsInput, u: UserRead = None):
    content = f'<b>{n.title}</b>\n{n.content}'
    if u:
        content += f'\n<em>{u.email}</em>'

    request = f'{api_url}/bot{bot_token}/sendMessage?chat_id={channel_link}&text={content}&parse_mode=html'
    return requests.get(request).json()['result']['message_id']
