from aiogram import Bot

def find_track(user_message, tracks_db):
    query = user_message.lower().strip()
    # подготваливаем наше сообщение - приводим всё в нижний регист и убираем пробелы
    result = [] # создаём список,куда будут добавляться всё треки,названия которых совпали с тем что в списке
    # в переменную track перебираем все совпадения из нашего списка песен
    for track in tracks_db:
        # в переменной title получаем доступ ко всем названиям песени из спискаи и по умолчаню тут пробел в значении
        title = track.get('title', '')
        # проверяем,является ли title списком
        if isinstance(title, list):
            # перебираем всё названия песе из списка,форматируем в строку и ставим в значение на место пробела
            title = ' '.join(str(t) for t in title)
            # все элементы из списка превращаем в строку и методом join разделяем пробелом
        if query in title.lower():
            # тогда добавляем в result все характеристики совпавших песен
            result.append({
                'title': title,
                'file_id': track.get('file_id'),
                'filename': track.get('filename'),
                'duration': track.get('duration')
            })
    return result 

CHAT_ID = '@test_chanel38'

async def check_subscription(bot: Bot, user_id: int) -> bool:
    quer = await bot.get_chat_member(
        chat_id=CHAT_ID,
        user_id=user_id
    )
    return quer.status in(
        'creator',
        'administrator',
        'member'
    )
