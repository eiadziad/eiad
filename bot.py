from twitchio.ext import commands
import os
from googletrans import Translator

class Bot(commands.Bot):
    def __init__(self):
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        if not token:
            raise ValueError("TWITCH_OAUTH_TOKEN not set!")
        
        channels = os.getenv('TWITCH_CHANNELS')
        if not channels:
            raise ValueError("TWITCH_CHANNELS not set!")
        
        self.channels_list = [ch.strip() for ch in channels.split(',')]
        self.last_messages = {}  # لتخزين آخر رسالة في كل قناة
        super().__init__(token=token, prefix='!', initial_channels=self.channels_list)

    async def event_ready(self):
        print(f'[Bot] Logged in as {self.nick}')
        print(f'[Bot] Channels: {self.channels_list}')

    async def event_message(self, message):
        # تحديث آخر رسالة في القناة
        self.last_messages[message.channel.name] = message
        
        # طباعة الرسالة في اللوق
        print(f'[#{message.channel.name}] <{message.author.name}>: {message.content}')

        if message.echo:  # تجاهل رسائل البوت نفسه
            return

        # التحقق من شروط الترجمة (بدون اعتماد على الرد)
        if (
            message.content.strip().lower() == 'ترجم'
            and message.author.name.lower() == 'eiadu'
        ):
            try:
                # الحصول على آخر رسالة قبل الأمر
                last_msg = self.last_messages.get(message.channel.name)
                
                if not last_msg or last_msg.content == message.content:
                    await message.channel.send("⚠️ لا يوجد نص للترجمة")
                    return
                
                # الترجمة
                translator = Translator()
                translated = translator.translate(last_msg.content, dest='ar')
                
                # إرسال النتيجة
                await message.channel.send(
                    f"@{message.author.name} الترجمة: {translated.text}"
                )
            except Exception as e:
                print(f"ERROR: {str(e)}")
                await message.channel.send("⚠️ فشلت الترجمة")

        await self.handle_commands(message)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
