from pyrogram import filters, Client
from AnonX import app
import asyncio
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from AnonX.core.call import Anon
from AnonX.utils.database import *
from pytgcalls.exceptions import (NoActiveGroupCall,TelegramServerError)

import random

audio_files = ["tom.mp3", "ahmed.mp3", "mas.mp3", "tomr.mp3"]

@app.on_message(filters.regex("بدأ الألعاب"))
async def strcall(client, message):
    assistant = await group_assistant(Anon, message.chat.id)
    try:
        if "بدأ الألعاب" in message.text:
            await message.reply("جاري تشغيل الألعاب في الكول...")

        audio_file = audio_files[0]
        if "tom" in message.text:
            audio_file = audio_files[0]
        elif "ahmed" in message.text:
            audio_file = audio_files[1]
        elif "mas" in message.text:
            audio_file = audio_files[2]
        elif "tomr" in message.text:
            audio_file = audio_files[3]

        await assistant.join_group_call(message.chat.id, AudioPiped(f"./assets/{audio_file}"), stream_type=StreamType().pulse_stream)
        await message.reply("تم التشغيل بنجاح!")

        while True:
            if "استوب" in (await app.get_history(message.chat.id, limit=1))[0].text:
                await assistant.leave_group_call(message.chat.id)
                await message.reply("تم الإيقاف بنجاح!")
                break
            elif not audio_files:
                await assistant.leave_group_call(message.chat.id)
                await message.reply("تم تشغيل جميع المقاطع بنجاح!")
                break

            await asyncio.sleep(٥)

        audio_files.append(audio_files.pop(0))

    except NoActiveGroupCall:
        await message.reply("لا يوجد كول مفتوح يا معلم")
    except TelegramServerError:
        await message.reply("في مشكلة في الييرفر، ابعت الأمر تاني")
