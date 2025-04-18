import asyncio  # استيراد مكتبة asyncio لإضافة التأخير
from twitchio.ext import commands
import os
import re

# خريطة التحويل من الأحرف اللاتينية إلى العربية
char_map = {
    'h': 'ا', 'g': 'ل', ']': 'د', '[': 'ج', 'p': 'ح', 'o': 'خ', 'i': 'ه', 'u': 'ع', 'y': 'غ',
    't': 'ف', 'r': 'ق', 'e': 'ث', 'w': 'ص', 'q': 'ض', '`': 'ذ', "'": 'ط', ';': 'ك', 'l': 'م',
    'k': 'ن', 'j': 'ت', 'f': 'ب', 'd': 'ي', 's': 'س', 'a': 'ش', '/': 'ظ', '.': 'ز', ',': 'و',
    'm': 'ة', 'n': 'ى', 'b': 'لا', 'v': 'ر', 'c': 'ؤ', 'x': 'ء', 'z': 'ئ'
}

def replace_chars(text):
    """تحويل الأحرف اللاتينية إلى العربية مع معالجة الرموز الخاصة مثل ; و :"""
    # استبدال : و ; برموز مميزة لتجنب المشاكل مع Twitch
    text = text.replace(':', 'COLON_PLACEHOLDER').replace(';', 'SEMICOLON_PLACEHOLDER')

    # نمر على كل حرف في النص ونتأكد من تحويله
    result = []
    for char in text:
        if char in char_map:
            result.append(char_map[char])  # تحويل الحروف الموجودة في char_map
        else:
            result.append(char)  # ترك الحروف الأخرى كما هي

    # استبدال الرموز المميزة بالرموز الأصلية بعد التحويل
    result_text = ''.join(result).replace('COLON_PLACEHOLDER', ':').replace('SEMICOLON_PLACEHOLDER', 'ك')

    return result_text

def clean_text(text):
    """تنظيف النص وإزالة أي حروف خاصة مثل @ أو الرموز في بداية أو نهاية الكلمات"""
    result = []
    for word in text.split():
        if word.startswith('@'):
            result.append(word)  # لا نحتاج لتغيير الكلمات التي تبدأ بـ @ (أسماء المستخدمين)
        else:
            converted_word = replace_chars(word)  # تحويل الكلمات
            result.append(converted_word)  # إضافة الكلمة المحولة للقائمة
    return ' '.join(result)




class Bot(commands.Bot):
    def __init__(self):
        # قراءة الـ OAuth Token من متغيرات البيئة
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        if not token:
            raise ValueError("TWITCH_OAUTH_TOKEN environment variable is not set.")
        
        # قراءة أسماء القنوات من متغيرات البيئة وتحويلها إلى قائمة
        channels = os.getenv('TWITCH_CHANNELS')
        if not channels:
            raise ValueError("TWITCH_CHANNELS environment variable is not set.")
        
        self.channels_list = [channel.strip() for channel in channels.split(',')]
        print(f"Attempting to join channels: {self.channels_list}")
        
        # تهيئة البوت
        super().__init__(token=token, prefix='!', initial_channels=self.channels_list)

    async def event_ready(self):
        print(f'[Bot] Logged in as | {self.nick}')
        print(f'[Bot] Successfully joined channels: {self.channels_list}')

    async def event_message(self, message):
        # **تجاهل أي رسالة ليس لها مرسل (author) لمنع الخطأ**
        if not message.author:
            return

        # تجاهل الرسائل التي تبدأ بعلامة "!"
        if message.content.startswith('!'):
            print(f"Ignoring command: {message.content}")
            return

        # طباعة اسم القناة واسم المستخدم والرسالة في السجلات
        print(f'#[{message.channel.name}] <{message.author.name}>: {message.content}')

        # السماح فقط للمستخدم EIADu بتنفيذ أمر "بدل" إذا كتب "غير" فقط بعد تجاهل @الرد
        if (
            message.author.name.lower() == "eiadu"
            and 'reply-parent-msg-id' in message.tags
        ):
            # إزالة المنشن إن وُجد (@اسم)
            msg = message.content.strip()
            if msg.startswith('@'):
                parts = msg.split(' ', 1)
                if len(parts) > 1:
                    msg = parts[1].strip()
                else:
                    msg = ''

            if msg.lower() == "غير":
                if 'reply-parent-display-name' in message.tags and 'reply-parent-msg-body' in message.tags:
                    original_sender = message.tags['reply-parent-display-name']
                    original_message = message.tags['reply-parent-msg-body']

                    # تنظيف الرسالة من أي محارف غريبة قبل المعالجة
                    cleaned_message = clean_text(original_message)

                    # استبدال الأحرف في الرسالة الأصلية
                    replaced_message = replace_chars(cleaned_message)

                    # ⏳ **إضافة تأخير لمدة ثانية واحدة قبل إرسال الرد**
                    await asyncio.sleep(1)

                    # إرسال الرد إلى القناة
                    await message.channel.send(f"**( {replaced_message} )**")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
