import asyncio
import os
import re
from twitchio.ext import commands

# خريطة التحويل من الأحرف اللاتينية إلى العربية
char_map = {
    'h': 'ا', 'g': 'ل', ']': 'د', '[': 'ج', 'p': 'ح', 'o': 'خ', 'i': 'ه', 'u': 'ع', 'y': 'غ',
    't': 'ف', 'r': 'ق', 'e': 'ث', 'w': 'ص', 'q': 'ض', '`': 'ذ', "'": 'ط', ';': 'ك', 'l': 'م',
    'k': 'ن', 'j': 'ت', 'f': 'ب', 'd': 'ي', 's': 'س', 'a': 'ش', '/': 'ظ', '.': 'ز', ',': 'و',
    'm': 'ة', 'n': 'ى', 'b': 'لا', 'v': 'ر', 'c': 'ؤ', 'x': 'ء', 'z': 'ئ', ' ': ' '
}

# نمط المنشن مثل @اسم
mention_pattern = re.compile(r'(@\w+)', re.UNICODE)

def replace_chars_preserve_mentions(text):
    """يستبدل الحروف حسب الخريطة، ويحافظ على المنشن كما هو"""
    segments = mention_pattern.split(text)
    result = []
    for segment in segments:
        if mention_pattern.match(segment):
            result.append(segment)  # احتفظ بالمنشن كما هو
        else:
            result.append(''.join(char_map.get(c.lower(), c) for c in segment))
    return ''.join(result)

def clean_text(text):
    """إزالة الرموز \ و \s وتنظيف الفراغات"""
    text = re.sub(r'\\s|\\', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

class Bot(commands.Bot):
    def __init__(self):
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        channels = os.getenv('TWITCH_CHANNELS')
        if not token or not channels:
            raise ValueError("TWITCH_OAUTH_TOKEN و TWITCH_CHANNELS يجب ضبطهم.")
        super().__init__(token=token, prefix='!', initial_channels=[c.strip() for c in channels.split(',')])

    async def event_ready(self):
        print(f'[Bot] Logged in as | {self.nick}')

    async def event_message(self, message):
        if not message.author:
            return

        content = message.content.strip().lower()

        # تجاهل الأوامر
        if content.startswith('!'):
            return

        # شرط الأمر: المرسل هو EIADu والرسالة هي بالضبط "بدل" ويوجد رد
        if (
            message.author.name.lower() == "eiadu" and
            content == "بدل" and
            'reply-parent-msg-body' in message.tags
        ):
            original = message.tags['reply-parent-msg-body']
            cleaned = clean_text(original)
            converted = replace_chars_preserve_mentions(cleaned)

            await asyncio.sleep(1)
            await message.channel.send(f"انهو يقول ( {converted} )")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
