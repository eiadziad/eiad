from twitchio.ext import commands
import os
from googletrans import Translator

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
        # تجاهل الرسائل المرسلة من البوت نفسه
        if message.author.name.lower() == self.nick.lower():
            return
        
        # طباعة اسم القناة واسم المستخدم والرسالة في السجلات
        print(f'#[{message.channel.name}] <{message.author.name}>: {message.content}')
        
        # التحقق من أن الرسالة هي "ترجم" كرد على رسالة أخرى ومن المستخدم EIADu
        if message.content.strip() == 'ترجم' and message.referenced_message is not None and message.author.name.lower() == 'eiadu':
            try:
                # استخراج النص الأصلي من الرسالة التي تم الرد عليها
                original_text = message.referenced_message.content
                # إنشاء كائن للترجمة
                translator = Translator()
                # ترجمة النص إلى العربية
                translated = translator.translate(original_text, dest='ar')
                # إرسال الترجمة إلى الدردشة
                await message.channel.send(f"الترجمة: {translated.text}")
            except Exception as e:
                print(f"حدث خطأ أثناء الترجمة: {e}")
                await message.channel.send("فيه مشكلة ما اقدر اترجم لك يا غالي")
        
        # معالجة الأوامر (ضروري لتنفيذ الأوامر الأخرى)
        await self.handle_commands(message)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
