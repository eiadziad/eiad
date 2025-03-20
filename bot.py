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
        super().__init__(token=token, prefix='!', initial_channels=self.channels_list)

    async def event_ready(self):
        print(f'[Bot] Logged in as {self.nick}')
        print(f'[Bot] Channels: {self.channels_list}')

    async def event_message(self, message):
        # طباعة جميع الرسائل في اللوق دائماً
        print(f'[#{message.channel.name}] <{message.author.name}>: {message.content}')

        if message.echo:  # تجاهل رسائل البوت نفسه
            return

        # التحقق من شروط الترجمة
        if (
            message.content.strip().lower() == 'ترجم' 
            and message.reference 
            and message.author.name.lower() == 'EIADu'
        ):
            try:
                replied_msg = await message.channel.fetch_message(message.reference.id)
                translator = Translator()
                translated = translator.translate(replied_msg.content, dest='ar')
                await message.channel.send(
                    f"@{message.author.name} الترجمة: {translated.text}"
                )
            except Exception as e:
                print(f"Error: {str(e)}")
                await message.channel.send("⚠️ فشلت الترجمة")

        # معالجة الأوامر العادية
        await self.handle_commands(message)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
