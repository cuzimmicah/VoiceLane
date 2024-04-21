import discord
from discord.ext import commands
from discord.ui import Select, View, Button
import os
from dotenv import load_dotenv
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

# Configure client with intents
intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.members = True
client = commands.Bot(command_prefix='/', intents=intents)

# Setup logging
logging.basicConfig(level=logging.INFO)

def getVCUsers():

    """Retrieve users from voice channels based on environment configuration."""
    voice_channel_ids = os.getenv('VOICE_CHANNELS').split(',')
    users = {}
    for channelID in voice_channel_ids:
        voice_channel = client.get_channel(int(channelID))
        if voice_channel:
            users[voice_channel.id] = [member for member in voice_channel.members]
        else:
            logging.warning(f"Channel ID {channelID} is not accessible or does not exist.")
    return users

class UserSelect(Select):

    """A select menu to choose users for operations."""
    def __init__(self, users, placeholder='Choose users'):
        options = [discord.SelectOption(label='Everybody', description='Select all users', value='all')] + [
            discord.SelectOption(label=user.display_name, value=str(user.id))
            for user_list in users.values() for user in user_list
        ]
        super().__init__(placeholder=placeholder, min_values=1, max_values=len(options), options=options)


    async def callback(self, interaction: discord.Interaction):
        
        """Silently acknowledge the interaction."""
        await interaction.response.defer(ephemeral=True)

class ChannelSelect(Select):

    """A select menu to choose a target voice channel."""
    def __init__(self, channels, placeholder='Choose target voice channel'):
        options = [discord.SelectOption(label=channel.name, value=str(channel.id)) for channel in channels]
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):

        """Silently acknowledge the interaction."""
        await interaction.response.defer(ephemeral=True)

class ConfirmButton(Button):

    """Button to confirm the selected operation."""
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):

        """Handle the operation based on user and channel selection."""
        users_select = [component for component in self.view.children if isinstance(component, UserSelect)][0]
        channel_select = [component for component in self.view.children if isinstance(component, ChannelSelect)][0]
        target_channel = interaction.guild.get_channel(int(channel_select.values[0]))

        if 'all' in users_select.values:
            users = [member for member in interaction.guild.members if member.voice]
        else:
            users = [interaction.guild.get_member(int(user_id)) for user_id in users_select.values]

        for user in users:
            if user and user.voice:
                await user.move_to(target_channel)

        await interaction.response.send_message("Move operation successful!", ephemeral=True)

class CancelButton(Button):

    """Button to cancel the operation."""
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):

        """Notify about the operation cancellation."""
        await interaction.response.send_message("Operation cancelled.", ephemeral=True)

@client.tree.command(name="moveusers", description="Move users between voice channels")
async def moveusers_command(interaction: discord.Interaction):

    """Handle the moveusers command."""
    users = getVCUsers()
    channels = [channel for channel in interaction.guild.voice_channels]
    view = View()
    view.add_item(UserSelect(users, 'Select users to move'))
    view.add_item(ChannelSelect(channels, 'Select target voice channel'))
    view.add_item(ConfirmButton("Confirm", discord.ButtonStyle.green))
    view.add_item(CancelButton("Cancel", discord.ButtonStyle.red))
    await interaction.response.send_message("Select users and target channel:", view=view, ephemeral=True)

@client.event
async def on_ready():

    """Notify when the bot is online and ready."""
    print(f'{client.user} is now running!')
    await client.tree.sync(guild=discord.Object(id=GUILD_ID))

def main():

    """Start the Discord bot."""
    client.run(TOKEN)

if __name__ == '__main__':
    main()
