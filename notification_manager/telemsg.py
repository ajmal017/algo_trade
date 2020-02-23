import telepot


def send_msg_tele(token, chat_id, msg):
    send_manager = telepot.Bot(token=token)
    send_manager.sendMessage(chat_id=chat_id, text=msg)


def send_photo_tele(token, chat_id, photo):
    send_manager = telepot.Bot(token=token)
    send_manager.sendPhoto(chat_id=chat_id, photo=photo)
