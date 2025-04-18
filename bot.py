import asyncio
from twitchio.ext import commands
import os
import re

# خريطة التحويل من الأحرف اللاتينية إلى العربية (حسب تخطيط الكيبورد)
char_map = {
    'h': 'ا', 'g': 'ل', ']': 'د', '[': 'ج', 'p': 'ح', 'o': 'خ', 'i': 'ه', 'u': 'ع', 'y': 'غ',
    't': 'ف', 'r': 'ق', 'e': 'ث', 'w': 'ص', 'q': 'ض', '`': 'ذ', "'": 'ط', ';': 'ك', '؛': 'ك',
    'l': 'م', 'k': 'ن', 'j': 'ت', 'f': 'ب', 'd': 'ي', 's': 'س', 'a': 'ش', '/': 'ظ', '.': 'ز',
    ',': 'و', 'm': 'ة', 'n': 'ى', 'b': 'لا', 'v': 'ر', 'c': 'ؤ', 'x': 'ء', 'z': 'ئ', ' ': ' '
}

def replace_chars(text):
    """تحويل الأحرف حسب تخطيط الكيبورد، مع تسجيل الاستبدالات"""
    result = []
    replacements = []

    for ch in text:
        replaced = char_map.get(ch.lower(), ch)
        result.append(replaced)
        if ch.lower() in char_map and ch.lower() != replaced:
            replacements.append(f"{ch} → {replaced}")
        elif ch.lower() not in char_map:
            print(f"[DEBUG] لم يتم تحويل الحرف: '{ch}' - الكود: {ord(ch)}")

    return ''.join(result), replacements

def clean_text(text):
    """تنظيف النص من الرموز غير الضرورية"""
    text = re.sub(r'\\s|\\', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class Bot(commands.Bot):
    def __init__(self):
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        if not token:
            raise ValueError("TWITCH_OAUTH_TOKEN environment variable is not set.")
        
        channels = os.getenv('TWITCH_CHANNELS')
        if not channels:
            raise ValueError("TWITCH_CHANNELS environment variable is not set.")
        
        self.channels_list = [channel.strip() for channel in channels.split(',')]
        print(f"Attempting to join channels: {self.channels_list}")
        
        super().__init__(token=token, prefix='!', initial_channels=self.channels_list)

    async def event_ready(self):
        print(f'[Bot] Logged in as | {self.nick}')
        print(f'[Bot] Successfully joined channels: {self.channels_list}')

    async def event_message(self, message):
        if not message.author:
            return
        
        if message.content.startswith('!'):
            print(f"Ignoring command: {message.content}")
            return
        
        print(f'#[{message.channel.name}] <{message.author.name}>: {message.content}')
        
        if message.author.name.lower() == "eiadu" and 'reply-parent-msg-id' in message.tags and 'غير' in message.content.lower():
            if 'reply-parent-display-name' in message.tags and 'reply-parent-msg-body' in message.tags:
                original_sender = message.tags['reply-parent-display-name']
                original_message = message.tags['reply-parent-msg-body']

                cleaned_message = clean_text(original_message)
                replaced_message, replacements = replace_chars(cleaned_message)

                await asyncio.sleep(1)

                reply = f"**( {replaced_message} )**"
                if replacements:
                    reply += " | تم الاستبدال: " + ", ".join(replacements)

                await message.channel.send(reply)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
