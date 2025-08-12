# 🤖 AI-Powered Discord Meme Recommendation Bot

A smart Discord bot that automatically analyzes conversation context and recommends the perfect memes and reaction GIFs using AI models.

link: https://discord.com/oauth2/authorize?client_id=1404307063005384816&permissions=2048&integration_type=0&scope=bot (invite this bot to your server)


## ✨ Features

- **🎭 Smart Context Analysis**: Uses AI to understand conversation mood and intent
- **🤖 Multi-AI Support**: Works with Google Gemini API
- **🎬 GIF Recommendations**: Integrates with Tenor API for high-quality GIFs
- **💬 Conversation Memory**: Maintains context across multiple messages
- **🚀 Auto-Recommendations**: Automatically suggests memes based on conversation flow
- **⚡ Manual Commands**: Get meme recommendations on demand

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Copy `config.example` to `.env` and fill in your API keys:

```bash
# Required
DISCORD_TOKEN=your_discord_bot_token

# Optional but recommended
GEMINI_API_KEY=your_gemini_key  
TENOR_API_KEY=your_tenor_key
```

### 3. Run the Bot
```bash
python main.py
```

## 🔑 Getting API Keys

### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and copy the token

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account and generate an API key

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key for Gemini

### Tenor API Key
1. Visit [Tenor Developer Portal](https://tenor.com/developer/keyregistration)
2. Register and get your API key

## 📋 Commands

| Command | Description |
|---------|-------------|
| `!meme [context]` | Get a meme recommendation (with optional context) |
| `!context` | Show recent conversation context |
| `!clear_context` | Clear conversation context |
| `!help_meme` | Show help for meme bot features |

## 🧠 How It Works

### 1. **Context Capture**
The bot listens to all messages in Discord channels and maintains a conversation history.

### 2. **AI Analysis**
When triggered (automatically or manually), the bot sends recent conversation context to an AI model (OpenAI GPT or Gemini) to analyze:
- Overall mood/vibe (roast, celebration, chaos, etc.)
- Appropriate search terms for finding relevant GIFs

### 3. **GIF Recommendation**
The bot searches Tenor API using the AI-generated search terms and presents the perfect reaction GIF with context.

## 🎯 Supported Moods

The bot can detect and respond to various conversation moods:
- **🔥 Roast/Savage** - Perfect for friendly banter
- **🏆 Celebration/Victory** - Great for achievements
- **😏 Sarcasm/Sass** - Ideal for witty comebacks
- **🤯 Chaos/Confusion** - Perfect for "what just happened" moments
- **🎉 Hype/Excitement** - Great for building energy
- **😅 Awkward/Funny** - Perfect for relatable moments

## ⚙️ Configuration Options

### Auto-Recommendation Frequency
The bot automatically suggests memes with a 15% probability per message to avoid spam. You can adjust this in the code.

### Context Memory
By default, the bot remembers the last 10 messages per channel. This can be modified in the `MAX_CONTEXT_MESSAGES` variable.

### AI Model Priority
The bot tries OpenAI first, then falls back to Gemini if OpenAI is unavailable.

## 🔧 Customization

### Adding New Moods
You can extend the fallback analysis in the `_fallback_analysis` method to recognize new conversation patterns.

### Custom GIF Sources
Modify the `get_recommended_gif` method to integrate with other GIF APIs like Giphy or Imgur.

### Prompt Engineering
Customize the AI prompts in `_analyze_with_openai` and `_analyze_with_gemini` for better mood detection.

## 💡 Use Cases

- **Gaming Communities**: Perfect for celebrating wins, reacting to epic fails
- **Friend Groups**: Great for friendly roasting and inside jokes
- **Work Teams**: Lighten the mood with appropriate reaction GIFs
- **Streaming Communities**: React to chat messages in real-time

## 🚨 Troubleshooting

### Bot Not Responding
- Check if `DISCORD_TOKEN` is set correctly
- Ensure the bot has proper permissions in your Discord server
- Verify the bot is online in your server

### AI Analysis Failing
- Check your API keys are valid
- Ensure you have sufficient API credits
- Check the logs for specific error messages

### No GIFs Found
- Verify your `TENOR_API_KEY` is correct
- Check if you've exceeded API rate limits
- The bot will fall back to placeholder GIFs if needed

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the bot!

---

**Happy meme-ing! 🎭✨**
