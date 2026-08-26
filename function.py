def find_track(user_message, tracks_db):
    query = user_message.lower().strip()
    # подготваливаем наше сообщение - приводим всё в нижний регист и убираем пробелы
    result = [] # создаём список,куда будут добавляться всё треки,названия которых совпали с тем что в списке
    # в переменную track перебираем все совпадения из нашего списка песен
    for track in tracks_db:
        # в переменной title получаем доступ ко всем названиям песени из спискаи и по умолчаню тут пробел в значении
        title = track.get('title', '')
        # указываем,что title может быть списком
        if isinstance(title, list):
            # перебираем всё названия песе из списка,форматируем в строку и ставим в значение на место пробела
            title = ' '.join(str(t) for t in title)
            # проверяем,что если у нас сообщение пользователя совпало с тем,что в нашем списке
        if query in title.lower():
            # тогда добавляем в result все характеристики совпавших песен
            result.append({
                'title': title,
                'file_id': track.get('file_id'),
                'filename': track.get('filename'),
                'duration': track.get('duration')
            })
    return result 
