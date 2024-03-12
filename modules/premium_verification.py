# premium_verification.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from vars import premium_users

# Define qr_code_filename or import it from another module if necessary
qr_code_filename = "qr_code.jpg"

async def verify_premium_user(user_id):
    return user_id in premium_users

async def prompt_upgrade(bot, message):
    text = (
        "Upgrade to premium to access this feature.\n\n"
        "Scan the QR code below and pay. After successful payment, share the screenshot for upgrading to Premium user."
    )
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Send Screenshot", callback_data="send_screenshot")]]
    )
    await message.reply_photo(photo=qr_code_filename, caption=text, reply_markup=keyboard)
