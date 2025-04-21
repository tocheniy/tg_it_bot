import logging
from arq.connections import RedisSettings
from arq.cron import cron
from arq import Worker
from config import setting
from telethon import TelegramClient

# from schedule.task import send_message
from database.crud.chat import get_chats
from schedule.event_tasks import send_statistics
# from task import send_message

rd_settings = RedisSettings(
    host=setting.redis.host,
    port=setting.redis.port,
    database=setting.redis.db,
    password=setting.redis.password,
)
# Инициализация логгера


async def startup(ctx):
    logger = logging.getLogger("arq_worker")
    logger.setLevel(logging.DEBUG)
    # Настройка консольного вывода
    console_handler = logging.StreamHandler()
    # Форматтер для логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    ctx["logger"] = logger

    ctx["client"] = TelegramClient(
        "session_schedule",
        setting.tg.api_id,
        setting.tg.api_hash,
    )
    logger.info("🚀 Инициализация воркера...")
    try:
        client: TelegramClient = ctx["client"]
        await client.start()
        chats = await get_chats()
        if not chats:
            return
        for chat in chats:
            tg_chat_id = chat.tg_chat_id
            mesg = "Планировщик заданий запущен ✔️"
            await client.send_message(tg_chat_id, mesg)
    except Exception as ex:
        print(ex)


async def shutdown(ctx):
    logger = ctx["logger"]
    logger.info("🛑 Завершение работы воркера...")
    try:
        client: TelegramClient = ctx["client"]
        chats = await get_chats()
        if not chats:
            return

        for chat in chats:
            tg_chat_id = chat.tg_chat_id
            mesg = "Планировщик заданий остановлен ❌"
            await client.send_message(tg_chat_id, mesg)

    except Exception as ex:
        print(ex)
    finally:
        await client.disconnect()
        logger.info("Telegram клиент отключен")


class WorkerSettings(Worker):
    on_startup = startup
    on_shutdown = shutdown
    # functions = [send_message]
    cron_jobs = [cron(send_statistics, hour={9}, minute={30})]
    # * Тест
    # cron_jobs = [cron(send_statistics, second={30})]
    redis_settings = rd_settings
    log_results = True

    # def logging_config(self, verbose):
    #     conf = super().logging_config(verbose)
    #     # alter logging setup to set arq.jobs level to WARNING
    #     conf["loggers"]["arq.jobs"]["level"] = "WARNING"
    #     return conf
