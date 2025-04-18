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

mention_pattern = re.compile(r'(@\w+)')

def replace_segment(text: str) -> str:
    """يستبدل أحرف segment غير المنشن وفق char_map"""
    return ''.join(char_map.get(ch.lower(), ch) for ch in text)

def process_message(text: str) -> str:
    """
    يقسم النص إلى منشن وغير منشن ويعالج كل جزء:
    - المنشن يُترك كما هو
    - بقية النص يُستبدل بأحرفه العربية
    ثم يُعاد جمعهم
    """
    parts = mention_pattern.split(text)
    return ''.join(
        seg if mention_pattern.fullmatch(seg) else replace_segment(seg)
        for seg in parts
    )

def clean_text(text: str) -> str:
    """يزيل \\s و \\ ويضغط الفراغات المتكررة"""
    text = re.sub(r'\\s|\\', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

class Bot(commands.Bot):
    def __init__(self):
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        channels = os.getenv('TWITCH_CHANNELS')
        if not token or not channels:
            raise ValueError("تأكد من ضبط TWITCH_OAUTH_TOKEN و TWITCH_CHANNELS")
        super().__init__(token=token, prefix='!', initial_channels=[c.strip() for c in channels.split(',')])

    async def event_ready(self):
        print(f'[Bot] Logged in as | {self.nick}')

    async def event_message(self, message):
        # تجاهل الرسائل بدون author أو التي تبدأ بـ "!"
        if not message.author or message.content.startswith('!'):
            return

        # سجل الرسالة
        print(f'#[{message.channel.name}] <{message.author.name}>: {message.content}')

        # الأمر يجب أن يكون بالضبط "بدل" ومن المرسل EIADu (المستخدم/البوت)
        if (
            message.author.name.lower() == "eiadu"
            and message.content.strip() == "بدل"
            and 'reply-parent-msg-id' in message.tags
            and 'reply-parent-msg-body' in message.tags
        ):
            original = message.tags['reply-parent-msg-body']
            cleaned = clean_text(original)
            replaced = process_message(cleaned)

            # تأخير ثانية واحدة لتفادي حد الرسائل
            await asyncio.sleep(1)
            await message.channel.send(f"انهو يقول ( {replaced} )")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
