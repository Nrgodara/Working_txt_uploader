from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import CallbackQuery

async def handle_non_premium(bot, m, premium_users):
    reply_text = (
        "𝑺𝒐𝒓𝒓𝒚 𝑩𝒐𝒔𝒔 𝑶𝒏𝒍𝒚 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑼𝒔𝒆𝒓𝒔 𝑪𝒂𝒏 𝑼𝒔𝒆 𝑴𝒆 🙂 \n\n"
        "**Uᴘɢʀᴀᴅᴇ Pʀᴇᴍɪᴜᴍ ᴛᴏ Use Me😎**"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝑼𝒑𝒈𝒓𝒂𝒅𝒆 𝑷𝒓𝒆𝒎𝒊𝒖𝒎✅", callback_data="upgrade_premium"),
         InlineKeyboardButton("𝑭𝒓𝒆𝒆 𝑻𝒓𝒊𝒂𝒍 🥲", callback_data="free_trial")]
    ])
    await bot.send_message(m.chat.id, reply_text, reply_markup=keyboard)

async def handle_free_trial(bot, m, premium_users):
    await bot.send_message(m.chat.id, "ℂ𝕠𝕟𝕘𝕣𝕒𝕥𝕦𝕝𝕒𝕥𝕚𝕠𝕟𝕤 𝕐𝕠𝕦 𝔸𝕣𝕖 𝕋𝕙𝕖 𝕃𝕦𝕔𝕜𝕪 𝕆𝕟𝕖 ✨ \n Yᴏᴜ Cᴀɴ Nᴏᴡ Usᴇ Mᴇ ғᴏʀ 𝟷 Hᴏᴜʀ As A Fʀᴇᴇ Tʀɪᴀʟ 🥳")
    # Add user to premium_users for 1 hour
    premium_users.add(m.from_user.id)
    # Set a timer to remove the user after 1 hour
    await asyncio.sleep(3600)  # 3600 seconds = 1 hour
    premium_users.remove(m.from_user.id)
    # Inform the user that the trial period has ended
    inform_text = (
        "𝕆𝕙𝕙 🥺 𝕐𝕠𝕦𝕣 𝔽𝕣𝕖𝕖 𝕋𝕣𝕚𝕒𝕝 ℍ𝕒𝕤 𝔼𝕩𝕡𝕚𝕣𝕖𝕕 \n\nTᴏ Cᴏɴᴛɪɴᴜᴇ Usɪɴɢ Mᴇ 🔼Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ Nᴏᴡ🪄"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝑼𝒑𝒈𝒓𝒂𝒅𝒆 𝑷𝒓𝒆𝒎𝒊𝒖𝒎✅", callback_data="upgrade_premium")],
    ])
    await bot.send_message(m.chat.id, inform_text, reply_markup=keyboard)

async def handle_upgrade_premium(bot, m):
    reply_text = (
        "𝑯𝒊,𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝒕𝒐 {𝕄𝔸ℍ𝕀_𝕋𝕖𝕔𝕙}(https://t.me/+YbnyONK0ZuhlMjk1) \n\n𝑪𝒖𝒓𝒓𝒆𝒏𝒕𝒍𝒚 𝑾𝒆 𝑶𝒏𝒍𝒚 𝒉𝒂𝒗𝒆 3 𝒑𝒍𝒂𝒏𝒔 𝒇𝒐𝒓 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑴𝒆𝒎𝒃𝒆𝒓𝒔𝒉𝒊𝒑 \n **𝑺𝒆𝒍𝒆𝒄𝒕 𝒚𝒐𝒖𝒓 𝒑𝒍𝒂𝒏**👇"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("1. For 15 days 199/-", callback_data="premium_plan_15_days"),
         InlineKeyboardButton("2. For 30 Days 350/-", callback_data="premium_plan_30_days")],
        [InlineKeyboardButton("3. For 2 Months 599/-", callback_data="premium_plan_2_months")]
    ])
    await bot.send_message(m.chat.id, reply_text, reply_markup=keyboard)
