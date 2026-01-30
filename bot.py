import asyncio
import random
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# 1. Create the inline keyboard with 4 buttons
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💰 Deposit", callback_data="deposit")],
    [InlineKeyboardButton(text="🚀 Trade", callback_data="trade")],
    [InlineKeyboardButton(text="⏯️ Stop/Start", callback_data="toggle_trade")],
    [InlineKeyboardButton(text="🏧 Withdraw", callback_data="withdraw")]
])

# 2. Handle the /start command
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    welcome_text = (
        "Welcome to the Demo Trading Bot! 📈\n\n"
        "Use the buttons below to simulate trading actions:"
    )
    await message.answer(welcome_text, reply_markup=keyboard)

# 3. Handle button presses
@router.callback_query()
async def handle_button_click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    response_text = ""

    if callback.data == "deposit":
        # Generate a fake deposit address
        fake_address = ''.join(random.choices('0123456789abcdef', k=40))
        response_text = f"Deposit ETH here: `{fake_address}`\n*(This is a demo address)*"

    elif callback.data == "trade":
        response_text = "Hurry, I'm going into the ETH market now and will make a profit for you! 📊"

    elif callback.data == "toggle_trade":
        # Simple state toggle simulation
        response_text = "Trading **stopped** ⏸️" if random.choice([True, False]) else "Trading **started** ▶️"

    elif callback.data == "withdraw":
        response_text = (
            "Please send your ETH withdrawal address.\n"
            "*(Simulation: Sending '0x123...' will trigger the response below)*"
        )
        # For demo: simulate a user sending an address
        if "0x123" in callback.message.text:  # This is a simplified check
            response_text = "Congratulations! 10 ETH profit is coming your way! 🎉"

    await callback.message.answer(response_text, parse_mode="Markdown")
    await callback.answer()  # Close the loading state on the button

# 4. Main function to start the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
