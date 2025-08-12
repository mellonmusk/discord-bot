import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import json
import aiohttp
from openai import AsyncOpenAI
import google.generativeai as genai
from typing import List, Dict, Optional
import random

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
TENOR_API_KEY = os.getenv('TENOR_API_KEY')

# Configure logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO)

# Configure AI clients
openai_client: Optional[AsyncOpenAI] = None
if OPENAI_API_KEY:
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Conversation context storage (channel_id -> recent_messages)
conversation_contexts: Dict[int, List[Dict]] = {}
MAX_CONTEXT_MESSAGES = 10

class MemeRecommender:
    def __init__(self):
        self.tenor_base_url = "https://tenor.googleapis.com/v2/search"
        self.fallback_gifs = [
            "https://media.tenor.com/example1.gif",
            "https://media.tenor.com/example2.gif",
            "https://media.tenor.com/example3.gif"
        ]
    
    async def analyze_conversation_mood(self, messages: List[str]) -> Dict[str, str]:
        """Analyze conversation context and determine mood/intent"""
        try:
            if GEMINI_API_KEY:
                return await self._analyze_with_gemini(messages)
            else:
                return self._fallback_analysis(messages)
        except Exception as e:
            logging.error(f"Error analyzing conversation: {e}")
            return self._fallback_analysis(messages)
    
    async def _analyze_with_openai(self, messages: List[str]) -> Dict[str, str]:
        """Use OpenAI to analyze conversation mood"""
        if openai_client is None:
            raise RuntimeError("OpenAI client not initialized")
        try:
            conversation_text = "\n".join(messages[-5:])  # Last 5 messages for context
            
            prompt = f"""
            Analyze the following conversation and determine:
            1. The overall mood/vibe (roast, celebration, chaos, hype, confusion, etc.)
            2. A search query for finding an appropriate reaction GIF/meme
            
            Conversation:
            {conversation_text}
            
            Respond in JSON format:
            {{
                "mood": "mood_description",
                "search_query": "gif_search_terms",
                "confidence": "high/medium/low"
            }}
            """
            
            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logging.error(f"OpenAI analysis failed: {e}")
            raise
    
    async def _analyze_with_gemini(self, messages: List[str]) -> Dict[str, str]:
        """Use Gemini to analyze conversation mood"""
        try:
            conversation_text = "\n".join(messages[-5:])
            
            prompt = f"""
            Analyze this conversation and determine the mood and appropriate GIF search terms.
            Conversation: {conversation_text}
            
            Return JSON: {{"mood": "mood", "search_query": "search terms", "confidence": "level"}}
            """
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = await model.generate_content_async(prompt)
            
            # Extract JSON from response
            result_text = response.text
            if "{" in result_text and "}" in result_text:
                start = result_text.find("{")
                end = result_text.rfind("}") + 1
                json_str = result_text[start:end]
                result = json.loads(json_str)
                return result
            else:
                raise ValueError("Invalid response format")
                
        except Exception as e:
            logging.error(f"Gemini analysis failed: {e}")
            raise
    
    def _fallback_analysis(self, messages: List[str]) -> Dict[str, str]:
        """Fallback analysis when AI APIs fail"""
        # Simple keyword-based analysis
        text = " ".join(messages).lower()
        
        if any(word in text for word in ["roast", "burn", "savage", "rekt"]):
            return {"mood": "roast", "search_query": "savage burn gif", "confidence": "low"}
        elif any(word in text for word in ["celebration", "victory", "win", "congrats"]):
            return {"mood": "celebration", "search_query": "celebration victory gif", "confidence": "low"}
        elif any(word in text for word in ["chaos", "madness", "wtf", "confused"]):
            return {"mood": "chaos", "search_query": "confused chaos gif", "confidence": "low"}
        else:
            return {"mood": "neutral", "search_query": "reaction gif", "confidence": "low"}
    
    async def get_recommended_gif(self, search_query: str) -> Optional[str]:
        """Get a GIF recommendation from Tenor API"""
        try:
            if not TENOR_API_KEY:
                return random.choice(self.fallback_gifs)
            
            params = {
                'q': search_query,
                'key': TENOR_API_KEY,
                'limit': 10,
                'media_filter': 'gif'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.tenor_base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('results') and len(data['results']) > 0:
                            # Pick a random GIF from results
                            gif = random.choice(data['results'])
                            return gif.get('media_formats', {}).get('gif', {}).get('url')
            
            return random.choice(self.fallback_gifs)
            
        except Exception as e:
            logging.error(f"Error fetching GIF: {e}")
            return random.choice(self.fallback_gifs)

# Initialize meme recommender
meme_recommender = MemeRecommender()

def update_conversation_context(channel_id: int, author: str, content: str):
    """Update conversation context for a channel"""
    if channel_id not in conversation_contexts:
        conversation_contexts[channel_id] = []
    
    # Add new message
    conversation_contexts[channel_id].append({
        'author': author,
        'content': content,
        'timestamp': asyncio.get_event_loop().time()
    })
    
    # Keep only recent messages
    if len(conversation_contexts[channel_id]) > MAX_CONTEXT_MESSAGES:
        conversation_contexts[channel_id] = conversation_contexts[channel_id][-MAX_CONTEXT_MESSAGES:]

@bot.event
async def on_ready():
    print(f"🤖 {bot.user.name} is ready! Meme recommendations activated!")
    print(f"🔗 Connected to {len(bot.guilds)} guild(s)")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Update conversation context
    update_conversation_context(
        message.channel.id,
        message.author.display_name,
        message.content
    )
    
    # Process commands first
    await bot.process_commands(message)
    
    # Auto-recommend memes based on conversation (with some randomness to avoid spam)
    if random.random() < 0.15:  # 15% chance to recommend
        await auto_recommend_meme(message)

async def auto_recommend_meme(message):
    """Automatically recommend a meme based on conversation context"""
    try:
        channel_id = message.channel.id
        if channel_id not in conversation_contexts:
            return
        
        # Get recent messages for context
        recent_messages = [msg['content'] for msg in conversation_contexts[channel_id][-5:]]
        
        # Analyze conversation mood
        analysis = await meme_recommender.analyze_conversation_mood(recent_messages)
        
        # Get recommended GIF
        gif_url = await meme_recommender.get_recommended_gif(analysis['search_query'])
        
        if gif_url:
            # Create embed for the recommendation
            embed = discord.Embed(
                title="🎭 Meme Recommendation",
                description=f"**Mood detected:** {analysis['mood'].title()}\n**Context:** {analysis['search_query']}",
                color=0x00ff88
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text=f"Confidence: {analysis['confidence']} | Auto-detected")
            
            await message.channel.send(embed=embed)
            
    except Exception as e:
        logging.error(f"Auto-recommendation failed: {e}")

@bot.command(name='meme')
async def recommend_meme(ctx, *, context: str = None):
    """Manually request a meme recommendation"""
    try:
        if context:
            # Use provided context
            analysis = await meme_recommender.analyze_conversation_mood([context])
        else:
            # Use recent conversation context
            channel_id = ctx.channel.id
            if channel_id in conversation_contexts:
                recent_messages = [msg['content'] for msg in conversation_contexts[channel_id][-5:]]
                analysis = await meme_recommender.analyze_conversation_mood(recent_messages)
            else:
                analysis = {"mood": "random", "search_query": "funny reaction gif", "confidence": "manual"}
        
        # Get recommended GIF
        gif_url = await meme_recommender.get_recommended_gif(analysis['search_query'])
        
        if gif_url:
            embed = discord.Embed(
                title="🎭 Meme Recommendation",
                description=f"**Mood:** {analysis['mood'].title()}\n**Search:** {analysis['search_query']}",
                color=0xff6b6b
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text=f"Confidence: {analysis['confidence']} | Requested by {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Sorry, couldn't find a suitable meme right now!")
            
    except Exception as e:
        logging.error(f"Meme recommendation failed: {e}")
        await ctx.send("❌ Something went wrong with the meme recommendation!")

@bot.command(name='context')
async def show_context(ctx):
    """Show current conversation context"""
    channel_id = ctx.channel.id
    if channel_id in conversation_contexts and conversation_contexts[channel_id]:
        recent_messages = conversation_contexts[channel_id][-5:]
        context_text = "\n".join([f"**{msg['author']}:** {msg['content']}" for msg in recent_messages])
        
        embed = discord.Embed(
            title="💬 Recent Conversation Context",
            description=context_text,
            color=0x3498db
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("📝 No recent conversation context available.")

@bot.command(name='clear_context')
async def clear_context(ctx):
    """Clear conversation context for current channel"""
    channel_id = ctx.channel.id
    if channel_id in conversation_contexts:
        del conversation_contexts[channel_id]
        await ctx.send("🧹 Conversation context cleared!")
    else:
        await ctx.send("📝 No context to clear.")

@bot.command(name='help_meme')
async def help_meme(ctx):
    """Show help for meme bot features"""
    help_text = """
🎭 **Meme Recommendation Bot Commands:**

`!meme [context]` - Get a meme recommendation (with optional context)
`!context` - Show recent conversation context
`!clear_context` - Clear conversation context
`!help_meme` - Show this help message

**Auto-features:**
- Bot automatically analyzes conversations
- Provides meme recommendations based on mood
- Learns from conversation context

**Supported moods:**
- Roast/Savage
- Celebration/Victory  
- Chaos/Confusion
- Hype/Excitement
- And more!
    """
    
    embed = discord.Embed(
        title="🤖 Meme Bot Help",
        description=help_text,
        color=0x9b59b6
    )
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    else:
        logging.error(f"Command error: {error}")
        await ctx.send("❌ Something went wrong with that command!")

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ Error: DISCORD_TOKEN not found in environment variables!")
        exit(1)
    
    print("🚀 Starting AI-powered Meme Recommendation Bot...")
    print("📋 Required API keys:")
    print(f"   Discord: {'✅' if DISCORD_TOKEN else '❌'}")
    print(f"   OpenAI: {'✅' if OPENAI_API_KEY else '❌ (optional)'}")
    print(f"   Gemini: {'✅' if GEMINI_API_KEY else '❌ (optional)'}")
    print(f"   Tenor: {'✅' if TENOR_API_KEY else '❌ (optional)'}")
    
    bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.INFO)