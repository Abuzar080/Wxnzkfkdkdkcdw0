import telebot
import base64
import os
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
API_TOKEN = '7796865492:AAHqbHmX4U-4NkFgv6dQrbSim2ya22k9gas'
bot = telebot.TeleBot(API_TOKEN)

# Replace 'YOUR_CHANNEL_USERNAME' with your actual channel username
CHANNEL_USERNAME = '@AzR_projects'

def encrypt_file_to_base64(file_path):
    """Encrypt the file to Base64."""
    with open(file_path, 'rb') as file:
        # Read the file content
        file_content = file.read()
        # Encode the content to Base64
        encrypted_content = base64.b64encode(file_content).decode('utf-8')
        return encrypted_content

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Check if the user is a member of the channel
    chat_member = bot.get_chat_member(CHANNEL_USERNAME, message.from_user.id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        # Create a button to redirect to the channel
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("devloper", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        markup.add(button)

        # Send welcome message with photo and button
        welcome_message = (
            "𝑊ᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴘʏᴛʜᴏɴ ғɪʟᴇ ᴛᴏ ᴇɴᴄʀʏᴘᴛ ʙᴏᴛ 😎\n\n"
            "𝑆ᴇɴᴅ ᴍᴇ ᴘʏᴛʜᴏɴ ғɪʟᴇ ᴛᴏ ᴇɴᴄʀʏᴘᴛ ғɪʟᴇ 🌸\n\n"
            "𝑆ᴇᴄᴜʀᴇ ʏᴏᴜʀ ᴘʏᴛʜᴏɴ ғɪʟᴇ 🫧"
        )
        photo_url = "https://t.me/botposters/26"
        bot.send_photo(message.chat.id, photo=photo_url, caption=welcome_message, reply_markup=markup)
    else:
        bot.reply_to(message, f"Please join our channel {CHANNEL_USERNAME} to use this bot.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Check if the user is a member of the channel
    chat_member = bot.get_chat_member(CHANNEL_USERNAME, message.from_user.id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        if message.document.mime_type == 'text/x-python':
            try:
                # Send a processing message
                processing_message = bot.send_message(message.chat.id, "Processing your file, please wait...")

                # Get the file ID
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                # Save the file temporarily
                temp_file_path = 'temp_file.py'
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(downloaded_file)

                # Encrypt the file to Base64
                encrypted_content = encrypt_file_to_base64(temp_file_path)

                # Create a new Python file that can decode the Base64 content
                encrypted_file_path = 'encrypted_file.py'
                with open(encrypted_file_path, 'w') as encrypted_file:
                    encrypted_file.write(f"""
import base64

# This is the encrypted content
encrypted_data = '''{encrypted_content}'''

# Function to decode and execute the original code
def execute_encrypted_code():
    decoded_code = base64.b64decode(encrypted_data).decode('utf-8')
    exec(decoded_code)

if __name__ == "__main__":
    execute_encrypted_code()
""")

                # Send the encrypted Python file back to the user
                with open(encrypted_file_path, 'rb') as encrypted_file:
                    bot.send_document(message.chat.id, encrypted_file, caption="Here is your encrypted Python file.")

                # Clean up the temporary files
                os.remove(temp_file_path)
                os.remove(encrypted_file_path)

                # Edit the processing message to indicate completion
                bot.edit_message_text("Processing complete! Here is your encrypted file:", chat_id=message.chat.id, message_id=processing_message.message_id)

            except Exception as e:
                bot.reply_to(message, f"An error occurred: {str(e)}")
                bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
        else:
            bot.reply_to(message, "Please send a valid Python (.py) file.")
    else:
        bot.reply_to(message, f"Please join our channel {CHANNEL_USERNAME} to use this bot.")

@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    bot.reply_to(message, "Please send a file, don't send any messages.")

if __name__ == '__main__':
    print("Bot is polling...")
    bot.polling()
