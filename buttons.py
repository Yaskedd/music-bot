from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def reply_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text='💽К разделу треков')
    builder.button(text='🔎Поиск трека')
    builder.button(text='🔧Тех. поддержка')
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def all_albums():
    builder = InlineKeyboardBuilder()
    builder.button(text='Drake - ICEMAN', callback_data='iceman')
    builder.button(text='Kanye West - Graduation', callback_data='Graduation')
    builder.adjust(1, 1)
    return builder.as_markup()
def iceman():

    builder = InlineKeyboardBuilder()
    builder.button(text='Make Them Cry', callback_data='mtc')
    builder.button(text='Dust', callback_data='dust')
    builder.button(text='Whisper My Name', callback_data='wmn')
    builder.button(text='Janice STFU', callback_data='stfu')
    builder.button(text='Ran To Atlanta', callback_data='rta')
    builder.button(text='Shabang', callback_data='shbng')
    builder.button(text='Make Them Pay', callback_data='mtp')
    builder.button(text='Burning Bridges', callback_data='bb')
    builder.button(text='National Treasures', callback_data='nt')
    builder.button(text='B\'s On The Table', callback_data='bot')
    builder.button(text='What Did I Miss', callback_data='wdim')
    builder.button(text='Plot Twist', callback_data='pt')
    builder.button(text='2 Hard 4 The Radio', callback_data='24')
    builder.button(text='Make Them Remember', callback_data='mtr')
    builder.button(text='Little Birdie', callback_data='lb')
    builder.button(text='Don\'t Worry', callback_data='DW')
    builder.button(text='Firm Friends', callback_data='ff')
    builder.button(text='Make Them Know', callback_data='mtk')
    builder.button(text='♻Сохранить весь альбом', callback_data='download_ice')
    builder.button(text='Вернуться в меню⬅',callback_data='back')
    builder.adjust(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    return builder.as_markup()

def Graduation():
    builder = InlineKeyboardBuilder()

    builder.button(text='Good Morning', callback_data='GM')
    builder.button(text='Champion', callback_data='champ')
    builder.button(text='Stronger', callback_data='strong')
    builder.button(text='I Wonder', callback_data='i won')
    builder.button(text='Good Life', callback_data='life')
    builder.button(text='Can\'t Tell Me Nothing', callback_data='CTMN')
    builder.button(text='Barry Bonds', callback_data='bonds')
    builder.button(text='Drunk and Hot Girls', callback_data='dahg')
    builder.button(text='Flashing Lights', callback_data='fl')
    builder.button(text='Everything I Am', callback_data='eia')
    builder.button(text='The Glory', callback_data='tglory')
    builder.button(text='Homecoming', callback_data='home')
    builder.button(text='Big Brother', callback_data='brat')
    builder.button(text='Good Night', callback_data='nigth')
    builder.button(text='♻Сохранить весь альбом', callback_data='download_grad')
    builder.button(text='Вернуться в меню⬅',callback_data='back')
    builder.adjust(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    return builder.as_markup()

def yes_not(track_id: str, index: int, total: int):
    builder = InlineKeyboardBuilder()
    # track_id - нужен,чтобы при нажатии на кнопки бот точно знал о каком треке идёт речь
    # index - порядковый номер текущего трека в просматриваемом списке,начиная с 0 или 1
    # total - общее колличество треков в текущем списке
    # confirm - префикс, который говорит обработчику,что это запрос на подтверждения выбора а подставленные параметры - индификатор выбора
    builder.button(text='✅Да,это он',callback_data=f'confirm:yes:{index}')
    builder.button(text='❌Нет,это не он', callback_data=f'confirm:no:{index}')
    builder.adjust(1, 1)
    return builder.as_markup()

def subscribe():
    builder  = InlineKeyboardBuilder()
    builder.button(text='Подписаться', url='https://t.me/test_chanel38')
    builder.button(text='Проверить подписку', callback_data='issub')
    builder.adjust(1,1)
    return builder.as_markup()