from aiogram import BaseMiddleware
'''
импортируем фукнцию BaseMiddleware,чтобы созданный класс унаследовал все параметры от этой функции
вообще сама суть этой функции в том,чтобы делать единое место проверки. в созданной нами функции будет проверка 
не выполнив условие которого она не допустит выполнение объекта 
'''
from aiogram.types import Message
from typing import Any,Awaitable,Callable,Dict
from function import check_subscription
from buttons import subscribe

# создаем класс,указываем импортированую функцию. теперь наш класс будет наследовать всё от неё
class SubscriptionMiddleware(BaseMiddleware):
    '''
    тут очень важно,что мы назвали функции __call__
    это особый метод в Python,позволяющий вызвать объект класса как функцию
    именно такой логики aiogram требует от BaseMiddleware и нам это нужно,
    чтобы в главном файле head при работе с dispatcher мы написали только объект класса
    ведь функция выполнится
    '''
    async def __call__(
        self, 
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        # под handler мы подставляем абсолютно любой вызваный обработчик
        #callable означает буквально - 'Это должно быть что-то, что можно вызвать как функцию
            # первое содержимое callable [Any, Dict[str, Any]]:
                # Any - означает буквально  "мне всё равно какой здесь тип"
                # Dict - означает "словарь, где ключи — строки, а значения могут быть любыми"
            # вторая часть callable - Awaitable[any] означает:
                # саму функцию Awaitable мы импортировали,так как у нас ассинхронные функции
                # она звучит так: "результат, который можно ожидать через await, и после выполнения он может вернуть что угодно"                

        event: Message, 
        # в этом параметре находится класс,который позволяет нам узнать кто отправил,что отправил,куда и т.п
        data: Dict[str, Any]
    ) -> Any:
        # ниже у нас заключены данные для параметров в переменные
        bot = data['bot'] 
        user_id = event.from_user.id

        # здесь моя функция проверки подписки
        subscribed = await check_subscription(
            user_id=user_id,
            bot=bot
        )
        if not subscribed: # если пользователь не подписан
            if isinstance(event, Message):
                await event.answer(
                    text="Перед использованием бота бота необходимо подписаться на наш канал",
                    reply_markup=subscribe()
                    )
            return # Хендлер НЕ будет срабатывать, Middleware остановится здесь

        # подписка есть -> продолжаем выполнение хендлера
        return await handler(event, data)
