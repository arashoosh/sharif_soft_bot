# Sharif Soft Bot

A Telegram bot designed to maintain group rules by automatically deleting messages containing links, usernames, or Telegram group/channel invitations. 

## Features
- Automatically deletes any message containing a URL, Telegram username, or group/channel invite link.
- Sends a private warning message to users who violate the rule.
- Bans users after three violations.
- Allows a whitelist of users and admins who can send links without restrictions.

## Deployment
This bot is built using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library and can be deployed easily on platforms like Railway, Render, or VPS servers.

## Environment Variables
- `TOKEN`: Your Telegram bot token.

## How It Works
1. Monitor every incoming text message.
2. If the message contains a prohibited link or username:
   - If the sender is not whitelisted or admin, delete the message.
   - Send a private warning to the user.
3. If a user sends three violating messages, the bot bans the user from the group.

## License
This project is licensed under the MIT License.

---

Made with ❤️ by [SharifSoft](https://sharifsoft.com)
