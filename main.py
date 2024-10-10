import random
import asyncio
import logging
from telethon import TelegramClient, errors
from telethon.errors import FloodWaitError, RpcCallFailError, PasswordHashInvalidError
from config import API_ID, API_HASH, USE_PROXY, PROXY, CHAT_IDS, MIN_INTERVAL, MAX_INTERVAL, PHONE_OR_BOT_TOKEN

# Логирование для отладки и отслеживания работы программы
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция подключения к Telegram
def get_client():
    if USE_PROXY:
        # Используем прокси-сервер
        client = TelegramClient('session_name', API_ID, API_HASH, 
                                 proxy=(PROXY['proxy_type'], PROXY['addr'], PROXY['port'], 
                                        True, PROXY['username'], PROXY['password']))
    else:
        client = TelegramClient('session_name', API_ID, API_HASH)
    
    return client

# Функция для генерации случайных сообщений
def generate_random_message():
    greetings = ["Привет", "Здравствуйте", "Хай", "Приветствую"]
    subjects = ["Как дела?", "Что нового?", "Как поживаете?", "Как ваши дела?"]
    closings = ["Удачного дня!", "Береги себя!", "На связи!", "Всего доброго!"]

    message = f"{random.choice(greetings)}! {random.choice(subjects)} {random.choice(closings)}"
    return message

# Асинхронная функция для отправки случайного сообщения в случайный чат
async def send_random_message(client):
    chat_id = random.choice(CHAT_IDS)
    message = generate_random_message()  # Генерируем новое сообщение
    try:
        await client.send_message(chat_id, message)
        logger.info(f"Message '{message}' sent to chat {chat_id}")
    except FloodWaitError as e:
        logger.warning(f"FloodWaitError: Sleeping for {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
    except RpcCallFailError:
        logger.error("Failed to send message due to RpcCallFailError.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

# Асинхронная функция для работы с интервалами
async def message_scheduler(client):
    while True:
        await send_random_message(client)
        # Выбираем случайный интервал времени от MIN_INTERVAL до MAX_INTERVAL
        interval = random.randint(MIN_INTERVAL, MAX_INTERVAL)
        logger.info(f"Waiting {interval // 60} minutes before sending the next message")
        await asyncio.sleep(interval)

# Главная функция
async def main():
    client = get_client()
    try:
        # Подключаемся к клиенту
        await client.start(phone=PHONE_OR_BOT_TOKEN)  # Передаем номер телефона или токен бота
        logger.info("Client started successfully")

        # Проверяем, требуется ли ввод пароля
        if client.is_user and await client.is_authenticated:
            # Если требуется пароль, запрашиваем его
            password = input("Please enter your password: ")
            await client.sign_in(PHONE_OR_BOT_TOKEN, password)
            logger.info("Signed in successfully with password.")

        # Запуск планировщика сообщений
        await message_scheduler(client)

    except FloodWaitError as e:
        logger.warning(f"Flood wait error: {str(e)}")
    except PasswordHashInvalidError:
        logger.error("Invalid password. Please check your password.")
    except errors.AuthKeyError:
        logger.error("Authentication error. Please check your phone number or bot token.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
