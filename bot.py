from twitchio.ext import commands
import os
from googletrans import Translator
from collections import deque

class Bot(commands.Bot):
    def __init__(self):
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        if not token:
            raise ValueError("TWITCH_OAUTH_TOKEN not set!")
        
        channels = os.getenv('TWITCH_CHANNELS')
        if not channels:
            raise ValueError("TWITCH_CHANNELS not set!")
        
        self.channels_list = [ch.strip() for ch in channels.split(',')]
        self.message_history = {}
        super().__init__(token=token, prefix='!', initial_channels=self.channels_list)

    async def event_ready(self):
        print(f'[Bot] Logged in as {self.nick}')
        print(f'[Bot] Channels: {self.channels_list}')

    async def event_message(self, message):
        # تجاهل رسائل البوت نفسه تمامًا
        if message.author.name.lower() == self.nick.lower():
            return

        # تحديث تاريخ الرسائل
        channel = message.channel.name
        if channel not in self.message_history:
            self.message_history[channel] = deque(maxlen=5)
        
        # حفظ الرسالة في التاريخ إذا لم تكن من البوت
        self.message_history[channel].append(message)
        
        # طباعة الرسالة في اللوق
        print(f'[#{channel}] <{message.author.name}>: {message.content}')

        # معالجة أمر الترجمة
        if (
            message.content.strip().lower() == 'ترجم'
            and message.author.name.lower() == 'eiadu'  # المستخدم المصرح له
        ):
            try:
                # البحث عن آخر رسالة غير أمر الترجمة وغير من البوت
                for msg in reversed(self.message_history[channel]):
                    if (
                        msg.content.strip().lower() != 'ترجم'
                        and msg.author.name.lower() != self.nick.lower()
                    ):
                        translator = Translator()
                        translated = translator.translate(msg.content, dest='ar')
                        await message.channel.send(
                            f"@{message.author.name} الترجمة: {translated.text}"
                        )
                        return
                
                await message.channel.send("⚠️ لم يتم العثور على نص للترجمة")
            except Exception as e:
                print(f"ERROR: {str(e)}")
                await message.channel.send("⚠️ فشلت الترجمة")

        await self.handle_commands(message)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
