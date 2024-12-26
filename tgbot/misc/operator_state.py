from aiogram.fsm.state import State, StatesGroup


class OperatorState(StatesGroup):
    message = State()
