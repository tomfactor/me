from pyrogram import filters, Client
from AnonX import app
import asyncio
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from AnonX.core.call import Anon
from AnonX.utils.database import *
from pytgcalls.exceptions import (NoActiveGroupCall, TelegramServerError)



async def play_audio_files(assistant, chat_id):
    while True:
        if not audio_files:
            await assistant.leave_group_call(chat_id)
            await message.reply("تم تشغيل جميع المقاطع بنجاح!")
            break

        audio_file = audio_files[0]
        await assistant.join_group_call(chat_id, AudioPiped(f"./assets/{audio_file}"), stream_type=StreamType().pulse_stream)
        await message.reply(f"تم تشغيل الملف الصوتي {audio_file} بنجاح!")

        await asyncio.sleep(5)
        audio_files.append(audio_files.pop(0))

@app.on_message(filters.regex("بدا الالعاب"))
async def start_playing(client, message):
    assistant = await group_assistant(Anon, message.chat.id)
    try:
        if "بدأ الألعاب" in message.text:
            await message.reply("جاري تشغيل الألعاب في الكول...")

        global audio_files
        audio_files = ["tom.mp3", "ahmed.mp3", "mas.mp3", "tomr.mp3"]
        await play_audio_files(assistant, message.chat.id)

    except NoActiveGroupCall:
        await message.reply("لا يوجد كول مفتوح يا معلم")
    except TelegramServerError:
        await message.reply("في مشكلة في السيرفر، ابعت الأمر تاني")

@app.on_message(filters.regex("استوب"))
async def stop_playing(client, message):
    assistant = await group_assistant(Anon, message.chat.id)
    try:
        await assistant.leave_group_call(message.chat.id)
        await message.reply("تم الإيقاف بنجاح!")
    except NoActiveGroupCall:
        await message.reply("لا يوجد كول مفتوح يمعلم")
