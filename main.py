import asyncio, discord, threading, configparser, pyautogui, os, sys, pygetwindow as gw, autoit, time
from discord import app_commands
from discord.ext import commands
import tkinter.messagebox
from ui import DiscordBotUI

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get("BOT", "token")
USERID = config.get("USER", "userid")

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
    TOKEN = str(token)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def setUserid(userid):
    config.set('USER', 'userid', str(userid))
    USERID = str(userid)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

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
    # tkinter.messagebox.showinfo("Dolphsol Bot", "Your bot has successfully connected")
    pyautogui.alert(text='Your bot has successfully connected', title='Dolphsol Bot', button='OK')

@bot.tree.command(name="restart", description="Restarts your macro")
async def restart(interaction: discord.Interaction):
    if str(interaction.user.id) == str(USERID):
        pyautogui.press('f3')
        await asyncio.sleep(2)
        pyautogui.press('f1')
        await interaction.response.send_message("Successfully restarted macro", ephemeral=True)
    else:
        await interaction.response.send_message("This isn't your macro!", ephemeral=True)
@bot.tree.command(name="screenshot", description="Takes a screenshot")
async def screenshot(interaction: discord.Interaction):
    if str(interaction.user.id) == str(USERID):
        pyautogui.screenshot("screenshot.png")
        await interaction.response.send_message(file=discord.File("screenshot.png"), ephemeral=True)
    else:
        await interaction.response.send_message("This isn't your macro!", ephemeral=True)

@bot.tree.command(name="inventory",description="Views your inventory")
@app_commands.choices(options = [
    app_commands.Choice(name="Gear",value="gear"),
    app_commands.Choice(name="Items",value="items")
])
async def inventory(interaction: discord.Interaction, options: app_commands.Choice[str]):
    if str(interaction.user.id) == str(USERID):
        await interaction.response.send_message("Viewing your inventory..")
        pyautogui.press('f3')
        await asyncio.sleep(1)
        hwnd = gw.getWindowsWithTitle('Roblox')
        if hwnd != []:
            try:
                hwnd[0].activate()
            except:
                hwnd[0].minimize()
                hwnd[0].maximize()
        if pyautogui.pixelMatchesColor(425, 127, (255, 255, 255)):
            autoit.mouse_click("left", 290, 100)
        if pyautogui.pixelMatchesColor(30, 27, (255, 255, 255)):
            autoit.mouse_click("left", 30, 27)
        if pyautogui.pixelMatchesColor(508, 793, (255, 255, 255)):
            autoit.mouse_click("left", 40, 443)
        autoit.mouse_click("left", 291, 98, speed=2)
        autoit.mouse_click("left", 40, 443)
        if (options.value == 'items'):
            autoit.mouse_click("left", 1265, 294, speed=2)
            pyautogui.screenshot("screenshot.png")
        elif (options.value == 'gear'):
            autoit.mouse_click("left", 955,295, speed=2)
            pyautogui.screenshot("screenshot.png")
        embed = discord.Embed(title="Inventory Screenshot")
        embed.set_image(url="attachment://screenshot.png")
        file = discord.File("screenshot.png", filename="screenshot.png")
        await interaction.edit_original_response(embed=embed, attachments=[file])
        autoit.mouse_click("left", 40, 443, speed=2)
        pyautogui.press('f1')
    else:
        await interaction.response.send_message("This isn't your macro!", ephemeral=True)
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
    if pyautogui.size() == (1920, 1080):
        ui = DiscordBotUI(start_callback=start_bot_thread, stop_callback=stopBot, token_callback=setToken, userid_callback=setUserid)
    else:
        alert = pyautogui.alert(text='You must have 1920x1080 as your screen resolution!', title='Dolphsol Bot')
        if alert == "OK":
            exit()

    # Run the UI main loop
    ui.run()

# Manual event loop management
if __name__ == "__main__":
    main()
