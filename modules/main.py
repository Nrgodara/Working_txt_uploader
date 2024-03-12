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

bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)


qr_code_filename = "qr_code.jpg"

# Handler for the "set" command
@bot.on_message(filters.user(owner_user_id) & filters.command("set") & filters.reply)
async def set_qr_code(bot: Client, m: Message):
    # Check if the replied message is a photo or a document containing photo media
    if m.reply_to_message.photo or (m.reply_to_message.document and "image" in m.reply_to_message.document.mime_type):
        # Get the media file ID
        media_file_id = None
        if m.reply_to_message.photo:
            media_file_id = m.reply_to_message.photo.file_id
        elif m.reply_to_message.document:
            media_file_id = m.reply_to_message.document.file_id
        
        # Download the media and save it as the QR code file
        await bot.download_media(media_file_id, file_name=qr_code_filename)
        
        # Send a message to confirm that the QR code has been set
        await m.reply_text("QR code has been set successfully.")
    else:
        # If the replied message is neither a photo nor a document containing photo media, send an error message
        await m.reply_text("Please reply to a photo or a document containing photo media.")





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






@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("**ℍɪɪ** ┈━═My Freind═━┈😎\n\n I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File Om Telegram So Basically If You Want To Use Me First Send Me /mahi Command And Then Follow Few Steps..")

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)





@bot.on_message(filters.command(["mahi"]))
async def account_login(bot: Client, m: Message):
    # Check if the user is a premium user
    if m.from_user.id not in premium_users:
        # If not a premium user, prompt them to upgrade with the QR code image
        text = (
            "Upgrade to premium to access this feature.\n\n"
            "Scan the QR code below and pay. After successful payment, share the screenshot for upgrading to Premium user."
        )
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Send Screenshot", callback_data="send_screenshot")]]
        )
        # Send the QR code image as a photo along with the text and buttons
        await m.reply_photo(photo=qr_code_filename, caption=text, reply_markup=keyboard)
        return

    # If the user is a premium user, proceed with the upload process
    editable = await m.reply_text('𝕋𝕆 ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴛxᴛ ғɪʟᴇ 𝕤ᴇɴᴅ ʜᴇʀᴇ ⚡️')
    input_msg: Message = await bot.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)
     #Continue with the rest of the upload process...
    
    path = f"./downloads/{m.chat.id}"

    try:
       with open(x, "r") as f:
           content = f.read()
       content = content.split("\n")
       links = []
       for i in content:
           links.append(i.split("://", 1))
       os.remove(x)
            # print(len(links)
    except:
           await m.reply_text("**Invalid file input.**")
           os.remove(x)
           return
    
   
    await editable.edit(f"**𝕋ᴏᴛᴀʟ ʟɪɴᴋ𝕤 ғᴏᴜɴᴅ ᴀʀᴇ🔗🔗** **{len(links)}**\n\n**𝕊ᴇɴᴅ 𝔽ʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛɪᴀʟ ɪ𝕤** **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Now Please Send Me Your Batch Name**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    

    await editable.edit("**𝔼ɴᴛᴇʀ ʀᴇ𝕤ᴏʟᴜᴛɪᴏɴ📸**\n144,240,360,480,720,1080 please choose quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("Now Enter A Caption to add caption on your uploaded file or send **no** to skip")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'no':
        MR = highlighter 
    else:
        MR = raw_text3
   
    await editable.edit("Now send the Thumb url/nEg » https://telegra.ph/file/xyz.jpg \n Or if don't want thumbnail send = **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']

            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}. {𝗻𝗮𝗺𝗲𝟭}{MR}.mkv\n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**\n**🤖 𝑫𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒅 𝑩𝒚** » @Professor_the_beast'
                cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}. {𝗻𝗮𝗺𝗲𝟭}{MR}.pdf \n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**\n**🤖 𝑫𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒅 𝑩𝒚** » @Professor_the_beast'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"**⥥ 🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️... »**\n\n**📝Name »** `{name}\n❄Quality » {raw_text2}`\n\n**🔗URL »** `{url}`\n\n**𝔹ᴏᴛ 𝑫𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒅 𝑩𝒚 » 𝑴𝑨𝑯𝑰®🇮🇳**"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**downloading Interupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("**𝔻ᴏɴᴇ 𝔹ᴏ𝕤𝕤😎**")
    


    



bot.run()
