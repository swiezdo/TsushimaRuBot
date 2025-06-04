# keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import GROUP_LINK

def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Начать регистрацию", callback_data="start_registration")]
        ]
    )

def platform_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💻 ПК", callback_data="platform_pc")],
            [InlineKeyboardButton(text="🎮 PlayStation", callback_data="platform_playstation")],
        ]
    )

def modes_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Сюжет", callback_data="mode_story")],
            [InlineKeyboardButton(text="🗡️ Выживание", callback_data="mode_survival")],
            [InlineKeyboardButton(text="🎯 Испытания Иё", callback_data="mode_trials")],
            [InlineKeyboardButton(text="🏔️ Главы", callback_data="mode_chapters")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="mode_done")]
        ]
    )

def goals_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏆 Получение трофеев", callback_data="goal_trophies")],
            [InlineKeyboardButton(text="🔍 Узнать что-то новое", callback_data="goal_learn")],
            [InlineKeyboardButton(text="👥 Поиск тиммейтов", callback_data="goal_teammates")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="goal_done")]
        ]
    )

def level_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🥉 Бронза", callback_data="level_bronze")],
            [InlineKeyboardButton(text="🥈 Серебро", callback_data="level_silver")],
            [InlineKeyboardButton(text="🥇 Золото", callback_data="level_gold")],
            [InlineKeyboardButton(text="🏅 Платина", callback_data="level_platinum")],
            [InlineKeyboardButton(text="👻 Кошмар", callback_data="level_nightmare")],
            [InlineKeyboardButton(text="🔥 HellMode", callback_data="level_hell")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="level_done")]
        ]
    )

def after_register_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏯 Tsushima.ru", url=GROUP_LINK)],
            [InlineKeyboardButton(text="📜 Профиль", callback_data="view_profile")],
            [InlineKeyboardButton(text="🏁 Начало", callback_data="start_over")]
        ]
    )

def back_to_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")]
        ]
    )
