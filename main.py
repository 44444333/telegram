# main.py

import random
import asyncio
import logging
from telethon import TelegramClient, errors
from telethon.errors import (
    FloodWaitError, 
    RpcCallFailError
)
from config import API_ID, API_HASH, USE_PROXY, PROXY, CHAT_IDS, MESSAGES, MIN_INTERVAL, MAX_INTERVAL

# Логирование для отладки и отслеживания работы программы
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция подключения к Telegram
def get_client():
    if USE_PROXY:
        # Используем прокси-сервер
        client = TelegramClient('session_name', API_ID, API_HASH, proxy=(PROXY['proxy_type'], PROXY['addr'], PROXY['port'], True, PROXY['username'], PROXY['password']))
    else:
        client = TelegramClient('session_name', API_ID, API_HASH)
    
    return client

# Асинхронная функция для отправки случайного сообщения в случайный чат
async def send_random_message(client):
    chat_id = random.choice(CHAT_IDS)
    message = random.choice(MESSAGES)
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
        # Выбираем случайный интервал времени от 15 до 40 минут
        interval = random.randint(MIN_INTERVAL, MAX_INTERVAL)
        logger.info(f"Waiting {interval // 60} minutes before sending the next message")
        await asyncio.sleep(interval)

# Главная функция
async def main():
    client = get_client()
    try:
        # Подключаемся к клиенту
        await client.start()
        logger.info("Client started successfully")

        # Запуск планировщика сообщений
        await message_scheduler(client)

    except errors.ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        await client.disconnect()
    except asyncio.TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
        await client.disconnect()
    except KeyboardInterrupt:
        logger.info("Program stopped manually")
        await client.disconnect()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
