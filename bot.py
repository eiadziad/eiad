from twitchio.ext import commands
import os

# خريطة التحويل من الأحرف اللاتينية إلى العربية
char_map = {
    'h': 'ا', 'g': 'ل', ']': 'د', '[': 'ج', 'p': 'ح', 'o': 'خ', 'i': 'ه', 'u': 'ع', 'y': 'غ',
    't': 'ف', 'r': 'ق', 'e': 'ث', 'w': 'ص', 'q': 'ض', '`': 'ذ', "'": 'ط', ';': 'ك', 'l': 'م',
    'k': 'ن', 'j': 'ت', 'f': 'ب', 'd': 'ي', 's': 'س', 'a': 'ش', '/': 'ظ', '.': 'ز', ',': 'و',
    'm': 'ة', 'n': 'ى', 'b': 'لا', 'v': 'ر', 'c': 'ؤ', 'x': 'ء', 'z': 'ئ'
}

def replace_chars(text):
    """تحويل الأحرف في النص بناءً على char_map، يدعم الأحرف الكبيرة والصغيرة"""
    # لكل حرف، يتم تحويله لحرف صغير أولاً ثم البحث في الخريطة
    return ''.join(char_map.get(ch.lower(), ch) for ch in text)

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
        
        # التحقق من أن الرسالة عبارة عن رد (reply) وتحتوي على كلمة "بدل"
        if 'reply-parent-msg-id' in message.tags and 'بدل' in message.content.lower():
            if 'reply-parent-display-name' in message.tags and 'reply-parent-msg-body' in message.tags:
                original_sender = message.tags['reply-parent-display-name']
                original_message = message.tags['reply-parent-msg-body']
                
                # استبدال الأحرف في الرسالة الأصلية باستخدام replace_chars
                replaced_message = replace_chars(original_message)
                # استبدال الرمز "\" بمسافة
                replaced_message = replaced_message.replace("\\", " ")
                
                # إرسال الرد إلى القناة
                await message.channel.send(f"انهو يقول ( {replaced_message} )")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
