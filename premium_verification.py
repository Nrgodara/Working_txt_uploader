# premium_verification.py

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
