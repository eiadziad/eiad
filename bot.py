from twitchio.ext import commands
import os

class Bot(commands.Bot):
    def __init__(self):
        # قراءة الـ OAuth Token من متغيرات البيئة
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        
        # قراءة أسماء القنوات من متغيرات البيئة وتحويلها إلى قائمة
        channels = os.getenv('TWITCH_CHANNELS').split(',')
        
        # تهيئة البوت
        super().__init__(token=token, prefix='!', initial_channels=channels)

    async def event_ready(self):
        print(f'[Bot] Logged in as | {self.nick}')

    async def event_message(self, message):
        # تجاهل الرسائل المرسلة من البوت نفسه
        if message.author.name.lower() == self.nick.lower():
            return
        
        # طباعة اسم القناة واسم المستخدم والرسالة في السجلات
        print(f'[ {channel.name}] [ {author.name}] Message: {message.content}')
        
        # معالجة الأوامر
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def hello(self, ctx):
        # إرسال رد إلى المستخدم
        await ctx.send(f'Hello {ctx.author.name}!')

if __name__ == "__main__":
    bot = Bot()
    bot.run()
