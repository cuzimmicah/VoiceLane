# Discord Voice Channel Manager Bot

This bot enables server administrators to manage voice channel assignments interactively within Discord. Users can be moved individually or in groups between channels using a Discord Slash Command interface.

## Features

- **Interactive User Selection**: Users can be selected individually or collectively to be moved to another voice channel.
- **Channel Selection**: Target voice channels can be chosen interactively.
- **Slash Commands**: Utilizes Discord's Slash Commands for easy and accessible commands within the server.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://https://github.com/cuzimmicah/VoiceLane.git
   ```
2. Install dependencies:
   ```
   pip install discord.py python-dotenv
   ```
3. Set environment variables:
   - Create a `.env` file in the root directory.
   - Add `DISCORD_TOKEN`, `DISCORD_GUILD_ID`, and `VOICE_CHANNELS` (comma-separated channel IDs).

4. Run the bot:
   ```
   python main.py
   ```

## Code Overview

### Bot Setup and Event Handling

- `main.py` contains the initialization of the Discord bot with necessary intents for handling guilds, messages, and members.

#### `on_ready` Event

Notifies the console when the bot is operational and syncs commands to the specified guild.

### Command Registration

#### `moveusers_command`

Registers a Slash Command that allows users to interactively choose which members to move and the target voice channel. The command sets up a message with interactive components.

### Interactive Components

#### `UserSelect`

A dropdown menu to select users. Supports selecting all users in voice channels or individual users based on the current state of the voice channels.

**Callback**:
- Silently acknowledges the interaction to prevent UI disruption.

#### `ChannelSelect`

A dropdown for selecting the target voice channel for the move operation.

**Callback**:
- Silently acknowledges the interaction.

#### `ConfirmButton`

A button that when clicked, performs the move operation based on the selections.

**Callback**:
- Executes the move operation.
- Notifies the user of success or failure without leaving the interaction hanging.

#### `CancelButton`

A button that cancels the operation and notifies the user.

**Callback**:
- Sends a message confirming the cancellation of the operation.

### Utilities

#### `getVCUsers`

Fetches users from specified voice channels, useful for populating the `UserSelect` component.

### Logging

Logs important events and errors to help in troubleshooting issues during operations.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with your enhancements.

## License

Copyright (c) 2024 Micah Alpuerto. All rights reserved.

Distributed under the MIT License. See `LICENSE` for more information.
