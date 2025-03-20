from twitchio.ext import commands
import os
from googletrans import Translator  # تأكد من تثبيت مكتبة googletrans

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
        # تهيئة المترجم
        self.translator = Translator()

    async def event_ready(self):
        print(f'[Bot] Logged in as | {self.nick}')
        print(f'[Bot] Successfully joined channels: {self.channels_list}')

    async def event_message(self, message):
        # تجاهل الرسائل المرسلة من البوت نفسه
        if message.author.name.lower() == self.nick.lower():
            return
        
        # تجاهل الرسائل التي تبدأ بعلامة "!"
        if message.content.startswith('!'):
            print(f"Ignoring command: {message.content}")
            return
        
        # التحقق من أمر "ترجم" في حال كان الرد على رسالة
        if message.content.startswith("ترجم"):
            # التأكد من أن المستخدم هو EIADu
            if message.author.name.lower() == "eiadu":
                # محاولة الحصول على نص الرسالة المُرد عليها
                # يعتمد هذا على وجود التاج "reply-parent-msg-body" في الرسالة
                parent_text = message.tags.get("reply-parent-msg-body")
                if parent_text:
                    translated = self.translator.translate(parent_text, dest='ar')
                    await message.channel.send(f"الترجمة: {translated.text}")
                else:
                    await message.channel.send("لا يوجد رسالة مُرد عليها للترجمة.")
            # لا نستجيب لأوامر "ترجم" من مستخدمين آخرين
            return
        
        # طباعة اسم القناة واسم المستخدم والرسالة في السجلات
        print(f'#[{message.channel.name}] <{message.author.name}>: {message.content}')

if __name__ == "__main__":
    bot = Bot()
    bot.run()
