import tkinter as tk, os, configparser
import tkinter.messagebox

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get("BOT", "token")
USERID = config.get("USER", "userid")

class DiscordBotUI:
    def __init__(self, start_callback, stop_callback, token_callback, userid_callback):
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.token_callback = token_callback
        self.userid_callback = userid_callback

        self.mainwindow = tk.Tk()
        self.mainwindow.title("Dolphsol Bot")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, 'dolphinico.ico')
        self.mainwindow.iconbitmap(icon_path)

        self.mainwindow.geometry("325x150")
        self.mainwindow.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        token_frame = tk.Frame(self.mainwindow, pady=10)
        token_frame.pack()

        # Label and entry for Discord Bot Token
        tk.Label(token_frame, text="Discord Bot Token: ").grid(row=0, column=0, sticky="w")
        self.token_entry = tk.Entry(token_frame, width=30, show="●")
        self.token_entry.grid(row=0, column=1, padx=5)
        self.token_entry.insert(0, str(TOKEN))
        self.token_entry.bind('<KeyRelease>', self.token_bot_handler)

        # Label and entry for Discord User ID
        tk.Label(token_frame, text="Your Discord User ID: ").grid(row=1, column=0, sticky="w")
        self.userid_entry = tk.Entry(token_frame, width=30)
        self.userid_entry.grid(row=1, column=1, padx=5)
        self.userid_entry.insert(0, str(USERID))
        self.userid_entry.bind('<KeyRelease>', self.userid_handler)

        button_frame = tk.Frame(self.mainwindow, pady=20)
        button_frame.pack()

        # Button to start the bot
        tk.Button(button_frame, text="Start Bot", bd=5, command=self.start_bot_wrapper, width=10).pack(side="left", padx=10)

        # Button to stop the bot
        tk.Button(button_frame, text="Stop Bot", bd=5, command=self.stop_bot_handler, width=10).pack(side="left", padx=10)



    def start_bot_handler(self):
        token = self.token_entry.get().strip()
        if token:
            try:
                self.start_callback()
            except Exception as e:
                print(e)
                tk.messagebox.showerror("Error", f"Failed to start bot: {e}")
        else:
            tk.messagebox.showerror("Error", "Please enter a valid Discord bot token.")

    def start_bot_wrapper(self):
        self.start_bot_handler()

    def token_bot_handler(self, event):
        token = self.token_entry.get().strip()
        if token:
            self.token_callback(token)

    def userid_handler(self, event):
        userid = self.userid_entry.get().strip()
        if userid:
            self.userid_callback(userid)


    def stop_bot_handler(self):
        print("Stopping bot...")
        self.stop_callback()

    def run(self):
        self.mainwindow.mainloop()