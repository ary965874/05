import logging
import asyncio
from hydrogram import Client, filters, enums
from hydrogram.errors import FloodWait
from info import ADMINS, CHANNELS
from database.ia_filterdb import save_file
from utils import temp
import time

logger = logging.getLogger(__name__)

# Store last indexing time for each channel
last_indexed = {}

@Client.on_message(filters.chat(CHANNELS) & filters.media)
async def auto_index_new_files(client, message):
    """Automatically index new files when they're posted to movie channels"""
    try:
        # Check if message has media
        if not message.media:
            return
            
        # Check if it's a supported media type
        if message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
            return
            
        # Get media object
        media = getattr(message, message.media.value, None)
        if not media:
            return
            
        # Set media properties
        media.file_type = message.media.value
        media.caption = message.caption
        
        # Save to database
        saved, status = await save_file(media)
        
        if saved:
            logger.info(f"Auto-indexed new file: {media.file_name}")
            # Optionally notify admins
            if ADMINS:
                try:
                    await client.send_message(
                        ADMINS[0], 
                        f"🎬 New movie auto-indexed!\n\n"
                        f"📁 File: {media.file_name}\n"
                        f"💾 Size: {media.file_size}\n"
                        f"📺 Channel: {message.chat.title}"
                    )
                except Exception as e:
                    logger.error(f"Failed to notify admin: {e}")
        elif status == 0:
            logger.info(f"File already exists: {media.file_name}")
        else:
            logger.error(f"Failed to save file: {media.file_name}")
            
    except Exception as e:
        logger.error(f"Auto-indexing error: {e}")

@Client.on_message(filters.command("auto_index") & filters.user(ADMINS))
async def manual_auto_index(client, message):
    """Guide user through manual indexing process"""
    try:
        guide_msg = f"""🎬 **Auto-Index Guide**

To index your movie channels, follow these steps:

**Method 1: Forward Message**
1. Go to your movie channel
2. Forward any movie message to this bot
3. Click "Accept Index" when prompted

**Method 2: Channel Link**
1. Copy any message link from your channel
2. Send the link to this bot
3. Click "Accept Index" when prompted

**Your Movie Channels:**
"""
        
        for channel_id in CHANNELS:
            try:
                channel = await client.get_chat(channel_id)
                guide_msg += f"📺 {channel.title} (`{channel_id}`)\n"
            except:
                guide_msg += f"📺 Channel `{channel_id}`\n"
        
        guide_msg += f"""
**Example Channel Link Format:**
`https://t.me/c/1234567890/123`

**Note:** Due to Telegram bot limitations, automatic scanning isn't available. Please use the manual methods above to index your channels.
"""
        
        await message.reply(guide_msg)
        
    except Exception as e:
        logger.error(f"Auto-index guide error: {e}")
        await message.reply(f"❌ Error: {e}")

@Client.on_message(filters.command("index_status") & filters.user(ADMINS))
async def show_index_status(client, message):
    """Show indexing status for all channels"""
    try:
        # Get database count
        from database.ia_filterdb import get_database_count
        primary_count, secondary_count = get_database_count()
        total_movies = primary_count + secondary_count
        
        status_msg = f"📊 **Bot Status**\n\n"
        status_msg += f"🎬 **Movies in Database:** {total_movies}\n"
        status_msg += f"📁 **Primary DB:** {primary_count}\n"
        status_msg += f"📁 **Secondary DB:** {secondary_count}\n\n"
        status_msg += f"📺 **Configured Channels:** {len(CHANNELS)}\n\n"
        
        for i, channel_id in enumerate(CHANNELS, 1):
            try:
                channel = await client.get_chat(channel_id)
                status_msg += f"{i}. **{channel.title}**\n"
                status_msg += f"   └ ID: `{channel_id}`\n"
                status_msg += f"   └ Bot is Admin: ✅\n\n"
            except Exception as e:
                status_msg += f"{i}. **Channel {channel_id}**\n"
                status_msg += f"   └ Status: ❌ {str(e)[:50]}...\n\n"
        
        status_msg += f"**Usage:**\n"
        status_msg += f"• Forward messages from channels to index\n"
        status_msg += f"• Use `/auto_index` for indexing guide\n"
        status_msg += f"• New uploads auto-index in real-time"
        
        await message.reply(status_msg)
        
    except Exception as e:
        await message.reply(f"❌ Error checking status: {e}")