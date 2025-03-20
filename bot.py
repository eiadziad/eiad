from twitchio.ext import commands
import os
from googletrans import Translator  # تأكد من تثبيت مكتبة googletrans باستخدام pip install googletrans

class Bot(commands.Bot):
    def __init__(self):
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        if not token:
            raise ValueError("TWITCH_OAUTH_TOKEN environment variable is not set.")
        
        channels = os.getenv('TWITCH_CHANNELS')
        if not channels:
            raise ValueError("TWITCH_CHANNELS environment variable is not set.")
        
        self.channels_list = [channel.strip() for channel in channels.split(',')]
        super().__init__(token=token, prefix='!', initial_channels=self.channels_list)
        self.translator = Translator()

    async def event_ready(self):
        print(f'[Bot] Logged in as | {self.nick}')
        print(f'[Bot] Successfully joined channels: {self.channels_list}')

    async def event_message(self, message):
        if not message.author or not getattr(message.author, "name", None):
            return

        # البحث عن وجود كلمة "ترجم" في محتوى الرسالة
        if "ترجم" in message.content:
            if message.author.name.lower() == "eiadu":
                parent_text = message.tags.get("reply-parent-msg-body")
                if parent_text:
                    try:
                        translated = self.translator.translate(parent_text, dest='ar')
                        await message.channel.send(f"الترجمة: {translated.text}")
                    except Exception as e:
                        await message.channel.send("error")
                else:
                    await message.channel.send("رد طيب")
            return

        if message.author.name.lower() == self.nick.lower():
            return

        if message.content.startswith('!'):
            return

        print(f'#[{message.channel.name}] <{message.author.name}>: {message.content}')

if __name__ == "__main__":
    bot = Bot()
    bot.run()
