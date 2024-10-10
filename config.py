# config.py

# API-ключи Telegram
API_ID = 26584958  # замените на ваш API ID
API_HASH = 'ba30d1f3e9c4977317b7db564ccfa6b9'  # замените на ваш API Hash

# Данные для прокси (если необходимо)
USE_PROXY = False  # Установите False, если прокси не используется
PROXY = {
    'proxy_type': 'socks5',  # Тип прокси ('socks5', 'http', и т.д.)
    'addr': 'proxy.server.address',  # Адрес прокси
    'port': 1080,  # Порт прокси
    'username': 'proxy_user',  # Логин (если требуется)
    'password': 'proxy_password'  # Пароль (если требуется)
}

# Список ID чатов для мониторинга
CHAT_IDS = [
    -1002222037494,  # замените на реальные chat ID
    -1001542092460,
    -1001954394751,
    -1002092127630,
    -1002078031708  
]

# Фразы для отправки
MESSAGES = [
    "Hello, how's it going?",
    "lfg guuuys!",
    "gm friends!"
]

# Интервалы отправки сообщений (в секундах)
MIN_INTERVAL = 10 * 60  # 15 минут
MAX_INTERVAL = 40 * 60  # 40 минут
