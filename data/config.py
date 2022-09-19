import os



BOT_TOKEN = str("5715470295:AAGLbx4bRzDrNvXXSpuW3u9IHEg3BJf8qxA")
admins = [
    936590877
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
