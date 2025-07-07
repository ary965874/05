"""
Channel handler for managing user channel subscriptions
Handles both common channel and language-specific channel joining
"""
import logging
from hydrogram import Client, filters, enums
from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from hydrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid
from database.users_chats_db import db
from language_config import COMMON_CHANNEL, get_language_channels, get_language_channel, get_all_languages, get_language_display_name, LANGUAGE_CHANNELS
from utils import is_subscribed, temp
from info import ADMINS

logger = logging.getLogger(__name__)

async def check_user_subscriptions(client: Client, user_id: int, selected_language: str = None) -> tuple:
    """
    Check if user is subscribed to required channels
    Returns (is_subscribed, missing_channels, language_needed)
    """
    missing_channels = []
    
    # Check common channel subscription
    common_subscribed = await is_subscribed(client, user_id, int(COMMON_CHANNEL))
    logger.info(f"User {user_id} common channel subscription: {common_subscribed}")
    if not common_subscribed:
        missing_channels.append(int(COMMON_CHANNEL))
    
    # If user has selected a language, check language-specific channel
    if selected_language:
        lang_channel = get_language_channel(selected_language)
        lang_subscribed = await is_subscribed(client, user_id, int(lang_channel))
        logger.info(f"User {user_id} {selected_language} channel ({lang_channel}) subscription: {lang_subscribed}")
        
        if not lang_subscribed:
            missing_channels.append(int(lang_channel))
    
    logger.info(f"User {user_id} missing channels: {missing_channels}")
    return len(missing_channels) == 0, missing_channels, selected_language is None

async def create_subscription_buttons(client: Client, user_id: int, selected_language: str = None, callback_data: str = None) -> InlineKeyboardMarkup:
    """Create buttons for channel subscription"""
    buttons = []
    
    # Check which channels user needs to join
    missing_channels = []
    
    # Check common channel
    if not await is_subscribed(client, user_id, int(COMMON_CHANNEL)):
        missing_channels.append(('common', int(COMMON_CHANNEL)))
    
    # Check language-specific channel
    if selected_language:
        lang_channel = get_language_channel(selected_language)
        if not await is_subscribed(client, user_id, int(lang_channel)):
            missing_channels.append(('language', int(lang_channel)))
    
    logger.info(f"Creating buttons for missing channels: {missing_channels}")
    
    # Create buttons only for channels user is NOT subscribed to
    for channel_type, channel_id in missing_channels:
        try:
            chat = await client.get_chat(channel_id)
            invite = await client.create_chat_invite_link(channel_id, creates_join_request=True)
            
            if channel_type == 'common':
                button_text = f"✇ Join Common Channel ({chat.title}) ✇"
            else:
                button_text = f"✇ Join {get_language_display_name(selected_language)} Channel ({chat.title}) ✇"
            
            buttons.append([
                InlineKeyboardButton(button_text, url=invite.invite_link)
            ])
        except Exception as e:
            logger.error(f"Error creating {channel_type} channel button: {e}")
    
    # Add try again button
    if callback_data:
        buttons.append([
            InlineKeyboardButton("🔄 Try Again", callback_data=callback_data)
        ])
    elif selected_language:
        buttons.append([
            InlineKeyboardButton("🔄 Try Again", callback_data=f"check_subscription_{selected_language}")
        ])
    
    return InlineKeyboardMarkup(buttons)

async def show_language_selection(client: Client, user_id: int, callback_data: str = None) -> InlineKeyboardMarkup:
    """Show language selection buttons"""
    buttons = []
    languages = get_all_languages()
    
    # Create buttons in rows of 2
    for i in range(0, len(languages), 2):
        row = []
        for j in range(2):
            if i + j < len(languages):
                lang = languages[i + j]
                display_name = get_language_display_name(lang)
                row.append(InlineKeyboardButton(
                    display_name,
                    callback_data=f"select_language_{lang}"
                ))
        buttons.append(row)
    
    return InlineKeyboardMarkup(buttons)

@Client.on_callback_query(filters.regex(r"^select_language_"))
async def handle_language_selection(client: Client, query: CallbackQuery):
    """Handle language selection callback"""
    try:
        from database.users_chats_db import db
        
        language = query.data.split("_", 2)[2]
        user_id = query.from_user.id
        
        logger.info(f"Language selection: {language} by user {user_id}")
        
        # Save user's language preference
        await db.add_user_language(user_id, language)
        
        # Answer the callback query first
        await query.answer(f"✅ {get_language_display_name(language)} selected!")
        
        # Check if user is subscribed to required channels
        is_subscribed, missing_channels, _ = await check_user_subscriptions(client, user_id, language)
        
        if is_subscribed:
            await query.message.edit_text(
                f"✅ **Language Selected**: {get_language_display_name(language)}\n\n"
                "You are subscribed to all required channels. You can now use the bot!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🎬 Search Movies", switch_inline_query_current_chat="")
                ]])
            )
        else:
            # Show subscription buttons
            subscription_buttons = await create_subscription_buttons(
                client, user_id, language, f"check_subscription_{language}"
            )
            
            await query.message.edit_text(
                f"🎯 **Language Selected**: {get_language_display_name(language)}\n\n"
                "📋 **Required Channels:**\n"
                "1. Common Updates Channel (for all users)\n"
                f"2. {get_language_display_name(language)} Channel (for your language)\n\n"
                "Please join both channels to continue:",
                reply_markup=subscription_buttons
            )
    except Exception as e:
        logger.error(f"Error handling language selection: {e}")
        await query.answer("❌ An error occurred. Please try again.")

@Client.on_callback_query(filters.regex(r"^check_subscription_"))
async def handle_subscription_check(client: Client, query: CallbackQuery):
    """Handle subscription check callback"""
    try:
        language = query.data.split("_", 2)[2]
        user_id = query.from_user.id
        
        # Check if user is subscribed to required channels
        is_subscribed, missing_channels, _ = await check_user_subscriptions(client, user_id, language)
        
        if is_subscribed:
            await query.answer("✅ Great! You are now subscribed to all required channels!")
            await query.message.edit_text(
                f"✅ **Language**: {get_language_display_name(language)}\n\n"
                "🎉 **All set!** You are now subscribed to all required channels.\n"
                "You can now use the bot to search for movies and subtitles!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🎬 Search Movies", switch_inline_query_current_chat="")
                ]])
            )
        else:
            await query.answer("❌ Please join all required channels first!")
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        await query.answer("❌ An error occurred. Please try again.")

@Client.on_callback_query(filters.regex(r"^show_language_selection$"))
async def handle_show_language_selection(client: Client, query: CallbackQuery):
    """Handle show language selection callback"""
    try:
        language_buttons = await show_language_selection(client, query.from_user.id)
        await query.message.edit_text(
            "🌐 **Select Your Language**\n\n"
            "Choose your preferred language to get access to language-specific content:",
            reply_markup=language_buttons
        )
    except Exception as e:
        logger.error(f"Error showing language selection: {e}")
        await query.answer("❌ An error occurred. Please try again.")

@Client.on_callback_query(filters.regex(r"^check_file_access_"))
async def handle_file_access_check(client: Client, query: CallbackQuery):
    """Handle file access check after channel subscription"""
    try:
        from database.users_chats_db import db
        
        file_id = query.data.split("_", 3)[3]
        user_id = query.from_user.id
        
        # Get user's language preference
        user_language = await db.get_user_language(user_id)
        
        if not user_language:
            await query.answer("❌ Please select your language first!")
            return
        
        # Check if user is subscribed to required channels
        is_subscribed, missing_channels, _ = await check_user_subscriptions(client, user_id, user_language)
        
        if is_subscribed:
            await query.answer("✅ Great! You can now access the file!")
            
            # Create a new callback query object to process the file
            new_query = type('CallbackQuery', (), {
                'data': f"files#{file_id}",
                'from_user': query.from_user,
                'message': query.message,
                'answer': query.answer
            })()
            
            # Directly handle the file access without circular import
            await handle_file_button_after_subscription(client, new_query, file_id)
            
        else:
            await query.answer("❌ Please join all required channels first!")
    except Exception as e:
        logger.error(f"Error checking file access: {e}")
        await query.answer("❌ An error occurred. Please try again.")

async def handle_file_button_after_subscription(client: Client, query, file_id: str):
    """Handle file button click after subscription verification"""
    try:
        from database.ia_filterdb import get_file_details
        from real_subtitle_handler import real_subtitle_handler as subtitle_handler
        from language_config import get_language_display_name
        from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        # Get file details
        file_details = await get_file_details(file_id)
        if file_details:
            # Show subtitle language selection
            subtitle_languages = subtitle_handler.get_supported_languages()
            btn = []
            
            # Add subtitle language options
            for lang in subtitle_languages[:8]:  # Show first 8 languages
                display_name = get_language_display_name(lang)
                btn.append([InlineKeyboardButton(f"{display_name}", callback_data=f"subtitle#{file_id}#{lang}")])
            
            # Add "No Subtitles" option
            btn.append([InlineKeyboardButton("🚫 No Subtitles Needed", callback_data=f"no_sub#{file_id}")])
            
            await query.message.edit_text(
                f"🎬 **{file_details['file_name']}**\n\n"
                "🗣 **Select Subtitle Language:**\n"
                "Choose your preferred subtitle language or select 'No Subtitles' to proceed without subtitles.",
                reply_markup=InlineKeyboardMarkup(btn)
            )
        else:
            from utils import temp
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
    except Exception as e:
        logger.error(f"Error handling file after subscription: {e}")