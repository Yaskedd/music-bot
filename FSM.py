from aiogram.fsm.state import StatesGroup, State 
class TrackSearch(StatesGroup):
    waiting_confirmation = State()