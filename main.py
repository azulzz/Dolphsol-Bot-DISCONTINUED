import asyncio, discord, threading, configparser, pyautogui, os, sys
from discord.ext import commands
import tkinter.messagebox
from ui import DiscordBotUI

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get("BOT", "token")

# Initialize Discord bot
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=".",
    case_insensitive=True,
    intents=intents
)

# Asynchronous callback functions
def stopBot():
    exit()

def setToken(token):
    config.set('BOT', 'token', str(token))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(f"Token set to: {token}")

def start_bot(token):
    try:
        bot.run(token, reconnect=True)
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror("Error", f"Failed to start bot: {e}")
        os.execl(sys.executable, sys.executable, *sys.argv)
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Connected")
    tkinter.messagebox.showinfo("Dolphsol Bot", "Your bot has successfully connected") 

@bot.tree.command(name="restart", description="Restart the macro")
async def restart(interaction: discord.Interaction):
    pyautogui.press('f3')
    await asyncio.sleep(2)
    pyautogui.press('f1')
    await interaction.response.send_message("Successfully restarted macro", ephemeral=True)

@bot.tree.command(name="screenshot", description="Takes a screenshot")
async def screenshot(interaction: discord.Interaction):
    pyautogui.screenshot("screenshot.png")
    await interaction.response.send_message(file=discord.File("screenshot.png"), ephemeral=True)

# Main function to run the DiscordBotUI
def main():
    # Define the start_bot_thread function
    def start_bot_thread():
        token = ui.token_entry.get().strip()  # Retrieve the token from the UI
        if token:
            threading.Thread(target=start_bot, args=(token,), daemon=True).start()
        else:
            tkinter.messagebox.showerror("Error", "Please enter a discord bot token")

    # Instantiate the DiscordBotUI instance
    ui = DiscordBotUI(start_callback=start_bot_thread, stop_callback=stopBot, token_callback=setToken)

    # Run the UI main loop
    ui.run()

# Manual event loop management
if __name__ == "__main__":
    main()
