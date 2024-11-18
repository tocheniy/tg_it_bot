from arq.connections import RedisSettings
from arq.cron import cron
from arq import Worker
from config import setting
from telethon import TelegramClient
from schedule.task import send_message
# from task import send_message

rd_settings = RedisSettings(
    host=setting.redis.host,
    port=setting.redis.port,
    database=setting.redis.db,
    password=setting.redis.password,
)


async def startup(ctx):
    ctx["client"] = TelegramClient(
        "session_schedule",
        # "session_name",
        setting.tg.api_id,
        setting.tg.api_hash,
    )
    ctx["text"] = "Привет Алешка!!!"

    client: TelegramClient = ctx["client"]
    await client.start()


async def shutdown(ctx):
    client: TelegramClient = ctx["client"]
    await client.disconnect()


class WorkerSettings(Worker):
    on_startup = startup
    on_shutdown = shutdown
    functions = [send_message]
    cron_jobs = [cron(send_message, second={10, 20, 30}, run_at_startup=True)]
    redis_settings = rd_settings
    log_results = True

    # def logging_config(self, verbose):
    #     conf = super().logging_config(verbose)
    #     # alter logging setup to set arq.jobs level to WARNING
    #     conf["loggers"]["arq.jobs"]["level"] = "WARNING"
    #     return conf
