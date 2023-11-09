import discord
from discord.ext import commands
import json
from datetime import datetime, timedelta

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load the settings from the file
with open('settings.json', 'r') as f:
    settings = json.load(f)

#啟動機器人
@bot.event
async def on_ready():
    print(f'{bot.user.name} 連接到Discord!')
    update_activity()
    await botActivity()

async def botActivity():
    activity = discord.Activity(type=discord.ActivityType.listening, name="監聽你")
    await bot.change_presence(activity=activity)

#把所有使用者加入倒Activity.json
@bot.command(name='update_db')
async def update_db_command(ctx):
    update_db()
    await ctx.send('已更新活動數據庫！')

@bot.command(name='check')
async def check_inactive_command(ctx):
    inactive_users = check_inactive()
    if len(inactive_users) > 0:
        message = '以下使用者已經閒置：\n'
        for user in inactive_users:
            message += f'- {user}\n'
    else:
        message = '目前沒有使用者閒置。'
    await ctx.send(message)

def check_inactive():
    # Load the activity data from the file
    with open('activity.json', 'r') as f:
        activity_data = json.load(f)

    # Load the settings from the file
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    # Calculate the inactive time threshold
    inactive_threshold = datetime.now() - timedelta(days=settings['inactive'])

    # Check the activity data for inactive users
    inactive_users = []
    for data in activity_data:
        last_active_time = datetime.fromisoformat(data['activity'])
        if last_active_time < inactive_threshold:
            inactive_users.append(data['name'])

    # Return the inactive users
    return inactive_users



#玩家加入伺服器
@bot.event
async def on_member_join(member):
    update_activity(member.id)

#玩家離開伺服器
@bot.event
async def on_member_remove(member):
    remove_user_activity(member.name, member.id)

def remove_user_activity(name, userid):
    # Load the activity data from the file
    with open('activity.json', 'r') as f:
        activity_data = json.load(f)

    # Find the user's activity data and remove it
    for i, data in enumerate(activity_data):
        if data['name'] == name and data['userid'] == userid:
            activity_data.pop(i)
            break

    # Save the updated activity data to the file
    with open('activity.json', 'w') as f:
        json.dump(activity_data, f, indent=4)

# 偵測文字頻道訊息
@bot.event
async def on_message(message):
    if message.author.bot:
        # Ignore messages from bots
        return

    if message.guild is None:
        # Private message
        print(f'{message.author.name} sent a private message: {message.content}')
    else:
        # Message in a guild
        if message.content.startswith('!'):
            await bot.process_commands(message)
            return
        
        # Detect messages in text channels
        if isinstance(message.channel, discord.TextChannel):
            # Do something with the message
            print(f'{message.author.name} sent a message in {message.channel.name} text channel: {message.content}')
            
    update_activity(message.author.id)

#偵測加入語音頻道
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        # User joined a voice channel
        print(f'{member.name} joined {after.channel.name} voice channel')
        update_activity(member.id)
    elif before.channel is not None and after.channel is None:
        # User left a voice channel
        print(f'{member.name} left {before.channel.name} voice channel')
        update_activity(member.id)

#更新使用者活動
def update_activity(member_id=None):
    # Load the activity data from the file
    with open('activity.json', 'r') as f:
        activity_data = json.load(f)

    # Find the user's activity data and update it
    found_user = False
    for data in activity_data:
        if data['userid'] == member_id:
            data['activity'] = str(datetime.now())
            found_user = True
            break

    # If the user is not found and member_id is not None, add the user to the activity data
    if not found_user and member_id is not None:
        member_name = "Unknown"
        # Get the member's name from the server
        member = bot.get_user(member_id)
        if member is not None:
            member_name = member.name
        activity_data.append({'name': member_name, 'userid': member_id, 'activity': str(datetime.now())})

    # Write the activity data to the file
    with open('activity.json', 'w') as f:
        json.dump(activity_data, f, indent=4)

#更新資料庫
def update_db():
    # Get all members in the server
    members = bot.guilds[0].members

    # Load the activity data from the file
    with open('activity.json', 'r') as f:
        activity_data = json.load(f)

    # Add all members to the activity data, except for the bot itself
    for member in members:
        if member.bot:
            continue
        # Check if the member is already in the activity data
        found_member = False
        for data in activity_data:
            if data['userid'] == member.id:
                found_member = True
                break

        # If the member is not found, add them to the activity data
        if not found_member:
            activity_data.append({'name': member.name, 'userid': member.id, 'activity': str(datetime.now())})

    # Write the updated activity data to the file
    with open('activity.json', 'w') as f:
        json.dump(activity_data, f, indent=4)

# 目前無法偵測文字編輯

bot.run(settings['token'])