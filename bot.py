from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token='oauth:ylrsztrpajobjqbaaxlmc5xfj3so0h', prefix='!', initial_channels=['11kaboy', 'bardan9'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

bot = Bot()
bot.run()