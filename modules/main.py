# main.py

import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import api_id, api_hash, bot_token, owner_user_id, premium_users
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram.types import CallbackQuery
from premium_verification import verify_premium_user, prompt_upgrade


bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)


@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("**ℍɪɪ** ┈━═My Freind═━┈😎\n\n I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File Om Telegram So Basically If You Want To Use Me First Send Me /mahi Command And Then Follow Few Steps..")

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

# Variable to store the QR code filename
qr_code_filename = "qr_code.jpg"

# Handler for the "set" command
@bot.on_message(filters.user(owner_user_id) & filters.command("set") & filters.reply & filters.photo)
async def set_qr_code(bot: Client, m: Message):
    # Get the photo file ID
    photo_file_id = m.reply_to_message.photo.file_id
    
    # Download the photo and save it as the QR code file
    await bot.download_media(photo_file_id, file_name=qr_code_filename)
    
    # Send a message to confirm that the QR code has been set
    await m.reply_text("QR code has been set successfully.")

@bot.on_message(filters.command(["mahi"]))
async def account_login(bot: Client, m: Message):
    # Check if the user is a premium user
    if not await verify_premium_user(m.from_user.id):
        # If not a premium user, prompt them to upgrade with the QR code image
        await prompt_upgrade(bot, m)
        return

    # If the user is a premium user, proceed with the upload process
    editable = await m.reply_text('𝕋𝕆 ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴛxᴛ ғɪʟᴇ 𝕤ᴇɴᴅ ʜᴇʀᴇ ⚡️')
    input_msg: Message = await bot.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)
    # Continue with the rest of the upload process...

# Callback to handle "send_screenshot" button press
@bot.on_callback_query()
async def callback_handler(bot: Client, query: CallbackQuery):
    if query.data == "send_screenshot":
        # Reply to the user asking to send the screenshot
        await query.message.reply_text(
            "Send the screenshot (only Photo) as a reply to this message.",
            reply_markup=ForceReply(selective=True)
        )

# Handler for when user sends the screenshot
@bot.on_message(filters.reply & filters.photo)
async def handle_screenshot(bot: Client, m: Message):
    # Check if the user is replying to the correct message (the one asking for the screenshot)
    if m.reply_to_message and m.reply_to_message.reply_markup and isinstance(m.reply_to_message.reply_markup, ForceReply):
        # Forward the screenshot to the premium channel
        forwarded_message = await m.forward(chat_id=premium_channel_id)
        
        # Get user details
        user_id = m.from_user.id
        user_mention = m.from_user.mention
        user_photo_id = m.from_user.photo.big_file_id if m.from_user.photo else None
        
        # Create a message with user details
        user_details_message = f"User ID: {user_id}\nUser Mention: {user_mention}"
        
        # If user has a photo, append it to the message
        if user_photo_id:
            user_details_message += f"\n\n[User Photo](tg://user?id={user_id})"
        
        # Send the user details to the premium channel
        await forwarded_message.reply_text(user_details_message)
        
        # Send a message to the premium channel indicating that payment details are being verified
        await bot.send_message(premium_channel_id, "Payment Details sent to the premium channel. Please wait while we are verifying...")
        
        # Send a reply to the user confirming that the payment details are being verified
        await m.reply_text("Payment Details sent to the premium channel. Please wait while we are verifying...")
    else:
        # If the user did not reply to the correct message, send a message asking for a valid payment receipt
        await m.reply_text("Out of Time🥹, Please send a valid payment receipt with UTR Number.")


# Handler for non-photo replies
@bot.on_message(filters.reply & ~filters.photo)
async def handle_invalid_payment_receipt(bot: Client, m: Message):
    # Check if the user is replying to the correct message (the one asking for the screenshot)
    if m.reply_to_message and m.reply_to_message.reply_markup and isinstance(m.reply_to_message.reply_markup, ForceReply):
        # If the user sends a non-photo reply, send a message asking for a valid payment receipt
        await m.reply_text("Please send a valid payment receipt with UTR Number.")
