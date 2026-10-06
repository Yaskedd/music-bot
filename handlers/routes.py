from aiogram import Router, types, F, html
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from buttons import reply_menu, all_albums,iceman, Graduation, yes_not, subscribe
from track_db import list, TRACKS_GRAD, TRACKS_ICE
from FSM import TrackSearch
from bot_instance import bot
from function import check_subscription, find_track

router = Router()  

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Привет!Я Мэнди,твой ассистент по поиску музыки.\nВ моем каталоге доступно более 30 треков и все они бесплатные!\n'
    'У меня ты можешь найти много уникальных треков и альбомов\n\n' 
    '<b>Зачем это нужно?</b>\n\n' 
    '• 👤Ставь в профиль!\nДругие будут видеть что ты слушаешь\n' \
    '• 📶Скачивай и слушай без интернета!\nАбсолютно все треки,которые ты скачал сохраняются здесь и работают без интернета\n' 
    '• 🔇Недоступные треки в вашем регионе\nТут такого нет,ты можешь найти желанный альбом без ограничений!\n\n' 
    '<b>В чём моё преимущество?</b>\n\n' 
    '•💦Треки без водяного знака!\nВ твоем профиле будет отображаться только автор и название,ничего лишнего!\n' 
    '• 🆓Всё абсолютно <b>бесплатно</b>\nБольше не нужно платить сервисам за подписку\n\nЧтобы начать,выбери нужную кнопку ниже⬇',
    parse_mode='HTML',reply_markup=reply_menu())


@router.message(Command('catalog'))
async def cmd_catalog(message: Message):
    photo_menu = FSInputFile('traks_menu.png')
    await message.answer_photo(photo_menu, caption='🎵Вы находитесь в главном разделе всех треков\n\nВыберите доступные альбомы кнопками⬇️',
    reply_markup=all_albums())

@router.message(Command('search'))
async def cmd_search(message: Message):
    Photo = FSInputFile('search_menu.jpg')
    await message.answer_photo(Photo, caption='🎵Вы находитесь в главном меню поиска\n\n'
    'Я помогу найти желанный трек или альбом\n\nДля этого просто отправь мне ключевое слово,трека,который вы ищите\n'
    'Я тщательно поищу его у себя в библиотеке😉')
# ловит дату,из ключей словаря TRACKS_ICE
# TRACKS_ICE.keys() - получает все ключи словаря
@router.callback_query(F.data.in_(TRACKS_ICE.keys()))
async def send_ice_track(callback: types.CallbackQuery):
    # тут TRACKS_ICE[callback.data] означает,что когда пользователь нажал кнопку с датой 'ice' то 
    # TRACKS_ICE[callback.data] фактически становится равно TRACKS_ICE['ice']
    track = TRACKS_ICE[callback.data]
    audio = FSInputFile(track['file']) # в этой переменной хранится доступ к файлу,который содержит выбраная callback_data
    await callback.message.answer_audio(
        audio=audio,
        title=track['title'],
        performer=track['performer']
)
    await callback.answer()

@router.callback_query(F.data.in_(TRACKS_GRAD.keys()))
async def send_grad_track(callback: types.CallbackQuery):
    track = TRACKS_GRAD[callback.data]
    audio = FSInputFile(track['file'])
    await callback.message.answer_audio(
        audio=audio,
        title=track['title'],
        performer=track['performer']
)
    await callback.answer()
# этот обработчик сработает,если словит следующие даты:
@router.callback_query(
    F.data.in_({
        'iceman',
        'back',
        'Graduation',
        'download_ice',
        'download_grad',
        'issub'
    })
)
async def process_menu_buttons(callback: types.CallbackQuery):
    data = callback.data

    if data == 'issub':
        chesk = await check_subscription(
            bot=callback.bot,
            user_id=callback.from_user.id
        )
        if chesk:
            await callback.message.edit_text(
                '✅Успешно')
            await cmd_start(message=callback.message)
            return
        else:
            await callback.message.edit_text(
                '❌Вы всё ещё не подписаны',
                reply_markup=subscribe()
            )
        await callback.answer()
    if data == 'iceman':
        photo = FSInputFile('iceman.jpg')
        caption = 'Drake - ICEMAN\n\n2026\n\nСписок треков⬇'

        new_media = InputMediaPhoto(
            media=photo,
            caption=caption
        )

        await callback.message.edit_media(
            media=new_media,
            reply_markup=iceman()
        )

    elif data == 'back':
        photo_menu = FSInputFile('traks_menu.png')
        caption_menu = (
            'Вы находитесь в главном разделе всех треков\n\n'
            'Выберите доступные альбомы кнопками⬇️'
        )

        media_menu = InputMediaPhoto(
            media=photo_menu,
            caption=caption_menu
        )

        await callback.message.edit_media(
            media=media_menu,
            reply_markup=all_albums()
        )

    elif data == 'Graduation':
        photo_grad = FSInputFile('Graduation.jpg')
        caption_grad = 'Kanye West - Graduation\n\n2007\n\nСписок треков⬇'

        new_media_grad = InputMediaPhoto(
            media=photo_grad,
            caption=caption_grad
        )

        await callback.message.edit_media(
            media=new_media_grad,
            reply_markup=Graduation()
        )

    elif data == 'download_ice':
        for track in TRACKS_ICE.values():
            audio = FSInputFile(track['file'])

            await callback.message.answer_audio(
                audio=audio,
                title=track['title'],
                performer=track['performer']
            )

    elif data == 'download_grad':
        for track in TRACKS_GRAD.values():
            audio = FSInputFile(track['file'])

            await callback.message.answer_audio(
                audio=audio,
                title=track['title'],
                performer=track['performer']
            )

    await callback.answer()

@router.callback_query(F.data.startswith('confirm'), TrackSearch.waiting_confirmation) 
# F.data.startswith('confirm') - проверяет,начинается ли строка,которую мы пришили к кнопе с подстроки confirm
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data
    try:
        '''
            _ - общепринятое в Python имя переменной,для ненужного значения,сюда попадает префикс confirm
            action - сюда прилетает второй элемент, 'yes' или 'no'
            track_id - третий элемент идентификатор трека,нужен,чтобы точно знать какой трек отклонили или приняли
            current_index - четвёртый элемент,индекс трека (например 2)
            '''
        if data.startswith('confirm:'):
            _, action, current_index = data.split(':')
        
            current_index = int(current_index) # cообщаем что этот параметр - целое число
            data1 = await state.get_data() # эта команда запрашивает у хранилища состояний все данные,которые были сохранены для текущего диалога
                # get_data() - возвращает словарь со всеми сохранёнными парами
            tracks = data1.get('tracks', []) #нам доступен список,со всеми совпавшими треками # текущий список
        
            if not (0 <= current_index < len(tracks)):# если этот список пуст,выводим сообщение в отдельном окне для этого у нас show_alert
                await callback.answer('❌Данные устарели,начните поиск заного', show_alert=True)
                await state.clear()
                return
            current_tracks = tracks[current_index] # выбранный трек
            if action == 'yes':
                await callback.message.edit_text(f'✅Отправляю: <b>{current_tracks["title"]}</b>', parse_mode='HTML')
        
                await bot.send_audio(
                chat_id=callback.message.chat.id,
                audio=current_tracks['file_id'],
                title=current_tracks['title']
                )
                await state.clear() # после отправки трека,удаляем его из памяти
            elif action == 'no':
                next_index = current_index + 1 #прибавляем 1 к id с каждым no
                if next_index >= len(tracks): # когда мы перебрали последний трек
                    await callback.message.answer('Это были все найденые треки\n' \
                    'Попробуйте уточнить название и найти снова')
                    await state.clear() # после неудачного поиска очищаем всё что было в памяти
                    return
                next_track = tracks[next_index] # в этой переменной хранится индекс трека
                await state.update_data(current_index=next_index)
                await callback.message.edit_text(
                     f'🎧 Вариант <b>{next_index + 1} из {len(tracks)}</b>:\n'
                    f'<b>{next_track["title"]}</b>\n\n'
                    f'Это то, что вы искали?',
                    reply_markup=yes_not(
                        track_id=current_tracks.get("file_id", "unknown"),
                        index=next_index,
                        total=len(tracks)
                    ),
                    parse_mode='HTML'
                    )
                await callback.answer()
        
    except Exception:
        await callback.message.answer('Произошла ошибка,её исправление уже ведётся.')        

@router.message(F.text == '💽К разделу треков')
async def traks_menu(message: Message):
    photo_menu = FSInputFile('traks_menu.png')
    await message.answer_photo(photo_menu, caption='Вы находитесь в главном разделе всех треков\n\nВыберите доступные альбомы кнопками⬇️',
    reply_markup=all_albums())

@router.message(F.text == '🔎Поиск трека')
async def search_track(message: Message):
    Photo = FSInputFile('search_menu.jpg')
    await message.answer_photo(Photo, caption='🎵Вы находитесь в главном меню поиска\n\n'
        'Я помогу найти желанный трек или альбом\n\nДля этого просто отправь мне ключевое слово,трека,который вы ищите\n'
        'Я тщательно поищу его у себя в библиотеке😉')

@router.message(F.text == '🔧Тех. поддержка')
async def support(message: Message):
    await message.answer('Если у вас возникла проблема,вы можете обратиться в поддержку,задав свой вопрос разработчику.\n\n@Yasked\n\n'
    '❕Убедительная просьба писать только по делу\nОжидайте ответ в течении суток☺')


@router.message(F.text)
async def search_handler(message: Message, state: FSMContext): # в параметрах подключаем fsm состояния
    query = message.text
    tracks_list = list
    tracks = find_track(user_message=query, tracks_db=tracks_list)
    if not tracks:
        await message.answer('Ничего не нашлось...')
        return
    await state.set_state(TrackSearch.waiting_confirmation) # переходим на заполнения параметра
    await state.update_data(tracks=tracks, current_index=0) # указываем название и индекс
    
    
    if len(tracks) == 1:
        # если найден только один трек,сразу спрашиваем вывод
        current_tracks = tracks[0] # выбираем 1 элемент из списка,не знаю зачем,если он тут один
        await message.answer(
            f'🎧Найден трек: \n <b>{current_tracks['title']}</b>\nЭто то,что вы искали?',
            reply_markup=yes_not(current_tracks['file_id'], 0, 1),
            parse_mode='HTML'
        )
    else:
        # если найдено несколько начинаем с первого
        current_tracks = tracks[0]

        await message.answer(
            f'🎧Найдено {len(tracks)} трека\n\n'
            f'Вариант <b>1 из {len(tracks)}</b>:\n'
            f'<b>{current_tracks["title"]}</b>\n\n'
            f'Это то,что вы искали?',
            reply_markup=yes_not(current_tracks['file_id'], 0, len(tracks)),
            parse_mode='HTML'
        )

@router.message()
async def words(message: Message):
    await message.answer('Я вас не понял. Открыл меню ниже — выберите нужный раздел кнопками⬇',reply_markup=reply_menu())

