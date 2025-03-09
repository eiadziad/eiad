from twitchio.ext import commands
import os

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
        
        # تجاهل الرسائل التي تبدأ بعلامة "!"
        if message.content.startswith('!'):
            print(f"Ignoring command: {message.content}")
            return
        
        # طباعة اسم القناة واسم المستخدم والرسالة في السجلات
        print(f'#[{message.channel.name}] <{message.author.name}>: {message.content}')

if __name__ == "__main__":
    bot = Bot()
    bot.run()
