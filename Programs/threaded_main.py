from os import makedirs
from os.path import join, dirname, join, exists

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox, Messagebox
from tkinter.filedialog import askdirectory

from collections import namedtuple
from shutil import move
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener
from decimal import Decimal
import csv
import datetime

from Scripts.get_imgs_data import multi_get_img_data
from Scripts.ImageDisplay import ImageDisplay
from Scripts.ImageButtons import ImageButtons
from Scripts.EntryWigits import EntryWigits
from Scripts.SessionTable import SessionTable
from Scripts.SessionFrame import SessionFrame
from Slots.PlayFactory import PlayFactory

register_heif_opener(decode_threads=8, thumbnails=False)

Dropdown_data = namedtuple("Dropdown_data", ["filename", "defaults"])
externals = {
    "play_type": Dropdown_data(
        "playtype_entry_values.csv",
        ["AP", "Gamble", "Misplay", "Non-play", "Science", "Tip"],
    ),
    "casino": Dropdown_data("casino_entry_values.csv", ["ilani", "Spirit Mountain"]),
    "denom": Dropdown_data(
        "denom_entry_values.csv",
        ["1cent", "2cent", "5cent", "10cent", "25cent", "$1", "$2"],
    ),
    "machine": Dropdown_data(
        "machine_entry_values.csv",
        ["Frankenstein", "Lucky Wealth Cat", "Pinwheel Prizes", "Power Push"],
    ),
}


class App(ttk.Window):
    def __init__(self):
        super().__init__()

        self.title("Slot Data Entry")
        self.minsize(450, 705)
        self.geometry("1300x800")
        self.iconphoto(
            False, ttk.PhotoImage(file=r"Programs\Icon\slot_machine_icon.png")
        )

        self._current_index = None
        self.imgs = []
        self.play_imgs = []
        self.hand_pay = []
        self.plays = {}
        self._current_play = None
        self.start_datetime = datetime.MINYEAR

        self.get_dropdown_data()

        self.pointer = 0
        self.scale = 7
        self.rotation = 0

        self.default_session_date = "Load first play"
        self.default_dt = "Auto / YYYY-MM-DD"
        self.session_date = ttk.StringVar(value=self.default_session_date)
        self.start_img = ttk.StringVar()
        self.end_img = ttk.StringVar()
        self.ttk_state = ttk.StringVar()

        self.columnconfigure(0, uniform="a", weight=1)
        self.columnconfigure(1, uniform="a", weight=2)
        self.columnconfigure(2, uniform="a", weight=2)

        self.session_table = SessionTable(self)
        self.session_table.grid(row=0, column=0, sticky="nsew")

        self.info_frame = ttk.Frame(self)
        self.session_frame = SessionFrame(self.info_frame, self)
        self.session_frame.pack(anchor="center")
        self.entry_wigits = EntryWigits(self.info_frame, self)
        self.entry_wigits.pack(anchor="center")
        self.info_frame.grid(row=0, column=1, sticky="nsew")

        image_frame = ttk.Frame(self)
        self.image_buttons = ImageButtons(image_frame, self)
        self.image_buttons.pack(side="top", padx=5, pady=5, anchor="n")
        self.image_display = ImageDisplay(image_frame)
        self.image_display.pack(side="top", padx=5, pady=5)
        # image_frame.pack(side='right', fill='both', anchor='ne')
        image_frame.grid(row=0, column=2, sticky="nsew")

        self.make_menu()

        self.setup_keybinds()

        self.image_buttons.save_button.configure(state="disabled")
        self.image_buttons.save_session_button.configure(state="disabled")
        self.image_buttons.set_image_adders("disabled")
        self.image_buttons.remove_button.configure(state="disabled")
        self.image_buttons.delete_button.configure(state="disabled")
        self.image_buttons.set_image_navigation("disabled")

    def get_dropdown_data(self):
        self.play_types = App.get_entry_values(externals["play_type"])
        self.casino_values = App.get_entry_values(externals["casino"])
        self.machine_values = App.get_entry_values(externals["machine"])
        self.denom_values = App.get_entry_values(externals["denom"])

    @staticmethod
    def get_entry_values(dd_data: Dropdown_data):
        if exists(dd_data.filename):
            with open(dd_data.filename, "r") as csvfile:
                values = list(csv.reader(csvfile))
                values = [
                    val.strip()
                    for sublist in values
                    for val in sublist
                    if (val.strip() != "")
                ]
                return values

        msg = f"{dd_data.filename} not found."
        if dd_data.defaults:
            print(msg, " Using defaults.")
            return dd_data.defaults

        return []

    def make_menu(self):
        menu = ttk.Menu(master=self)
        self.configure(menu=menu)

        file_menu = ttk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Add Casino", command=self.add_casino)
        file_menu.add_command(label="Add Machine", command=self.add_machine)
        file_menu.add_command(label="Add Denom", command=self.add_denom)
        file_menu.add_command(label="Add PlayType", command=self.add_playtype)
        file_menu.add_separator()
        file_menu.add_command(label="Set Image Scale Divisor", command=self.set_scale)
        file_menu.add_command(label="Rotate Image", command=self.rotate_image)
        file_menu.add_separator()
        file_menu.add_command(label="Preload Test Play", command=self.load_test_play)
        file_menu.add_command(label="Open Test Folder", command=self.open_test_folder)

        menu.add_cascade(label="File", menu=file_menu)

    def open_test_folder(self):
        folder = join(dirname(dirname(__file__)), "Data", "test_pics")
        self.open_folder(folder)

    def open_folder(self, directory=""):
        if directory == "":
            directory = askdirectory(mustexist=True)

        if directory == "":
            return

        print("Loading ", datetime.datetime.now())
        # ( image path, image type, image date )
        self.imgs = [d for d in multi_get_img_data(directory) if d is not None]
        print("Loaded ", datetime.datetime.now())

        if len(self.imgs) == 0:
            return

        self.imgs = sorted(self.imgs, key=lambda item: item[2])
        self.display_image()
        self.image_buttons.set_image_adders("normal")
        self.image_buttons.delete_button.configure(state="warning")
        self.image_buttons.set_image_navigation("normal")

    def add_casino(self):
        new_casino = Querybox.get_string(prompt="Enter a casino", title="Casino Entry")
        if (new_casino is not None) and (new_casino not in self.casino_values):
            self.casino_values.append(new_casino)

    def add_machine(self):
        new_machine = Querybox.get_string(
            prompt="Enter a machine", title="Machine Entry"
        )
        if (new_machine is not None) and (new_machine not in self.machine_values):
            self.machine_values.append(new_machine)

    def add_playtype(self):
        new = Querybox.get_string(prompt="Enter a play type", title="PlayType Entry")
        if (new is not None) and (new not in self.play_types):
            self.play_types.append(new)

    def add_denom(self):
        new = Querybox.get_string(prompt="Enter a denomination", title="Denom Entry")
        if (new is not None) and (new not in self.denom_values):
            self.denom_values.append(new)

    def set_scale(self):
        scale = Querybox.get_integer(
            "Enter a integer scale. Larger makes the image smaller",
            "Set scale",
            self.scale,
            1,
        )
        if scale is None:
            pass
        else:
            self.scale = scale
        self.display_image()
    
    def rotate_image(self):
        self.rotation = self.rotation + 90 if self.rotation + 90 <= 360 else 0
        self.display_image()
    

    def display_image(self):
        if len(self.imgs) == 0:
            return

        self.image_display.canvas.delete("all")
        # opens the image at the current pointer
        with Image.open(self.imgs[self.pointer][0]) as image:
            image = image.reduce(self.scale)
            image = image.rotate(self.rotation, expand=1)

            global imagetk
            # turns the image into a image that tkinter can display
            imagetk = ImageTk.PhotoImage(image)

            # gets the image dimensions and divides them by 2
            x, y = image.size
            x, y = x / 2, y / 2

            # adds the image to the canvas
            self.image_display.canvas.create_image(x, y, image=imagetk)

    def update_session_date(self):
        if self._current_play is None:
            return
        if (
            self.session_date.get() != ""
            and self.session_date.get() != self.default_session_date
        ):
            fmt = "%Y%m%d"
            self._current_play.session_date = datetime.datetime.strptime(
                self.session_date.get(), fmt
            )

    def update_casino(self, casino=None):
        if self._current_play is None:
            return
        if self.session_frame.casino.var.get():
            self._current_play.casino = self.session_frame.casino.var.get()

    def update_start_datetime(self):
        if (
            self.entry_wigits.dt.var.get() != self.default_dt
            and self.entry_wigits.dt.var.get() != ""
        ):
            fmt = "%Y-%m-%d %H:%M:%S"
            if len(self.entry_wigits.dt.var.get()) == 10:
                fmt = "%Y-%m-%d"
            self._current_play.start_time = datetime.datetime.strptime(
                self.entry_wigits.dt.var.get(), fmt
            )

    def update_end_datetime(self):
        if self._current_play is None:
            return
        if (
            self.entry_wigits.end_dt.var.get() != ""
            and self.entry_wigits.end_dt.var.get() != "1"
        ):
            fmt = "%Y%m%d%H%M%S"
            self._current_play.end_time = datetime.datetime.strptime(
                self.entry_wigits.end_dt.var.get(), fmt
            )

    def update_bet(self, bet=None):
        if self._current_play is None:
            return
        if self.entry_wigits.bet.var.get():
            self._current_play.bet = Decimal(self.entry_wigits.bet.var.get())

    def update_play_type(self, play_type=None):
        if self._current_play is None:
            return
        if self.entry_wigits.play_type.var.get():
            self._current_play.play_type = self.entry_wigits.play_type.var.get()

    def update_denom(self, denom=None):
        if self._current_play is None:
            return
        if self.entry_wigits.denom_cb.var.get():
            self._current_play.denom = self.entry_wigits.denom_cb.var.get()

    def update_pnl(self):
        if self._current_play is None:
            return
        self.entry_wigits.profit_loss.var.set(self._current_play.pnl)

    def update_cashin(self, cashin=None):
        if self._current_play is None:
            return
        if self.entry_wigits.cashin.var.get():
            self._current_play.cash_in = Decimal(self.entry_wigits.cashin.var.get())
            self.update_pnl()

    def update_cashout(self, cashout=None):
        if self._current_play is None:
            return
        if self.entry_wigits.cashout.var.get():
            self._current_play.cash_out = Decimal(self.entry_wigits.cashout.var.get())
            self.update_pnl()

    def update_init_state(self):
        if self._current_play is None:
            return
        lines = self.entry_wigits.initial_state.get_text().split(r"\n")
        line = " ".join(lines)
        line = line.strip()
        self._current_play.state = line

    def update_play_note(self):
        if self._current_play is None:
            return
        lines = self.entry_wigits.note.get_text().split(r"\n")
        line = " ".join(lines)
        line = line.strip()
        self._current_play.note = line

    def update_start_image(self):
        if self._current_play is None:
            return
        self._current_play.start_image = self.entry_wigits.start_entry.var.get()

    def update_end_image(self):
        if self._current_play is None:
            return
        self._current_play.end_image = self.entry_wigits.end_entry.var.get()

    def update_addl_images(self):
        if self._current_play is None:
            return
        # filter duplicates
        to_add = list(dict.fromkeys(self.play_imgs))
        self._current_play.add_images(to_add)

    def update_handpays(self):
        self._current_play.hand_pays.clear()
        for hp in self.hand_pay:
            self._current_play.add_hand_pay(hp)
        self.update_pnl()

    def load_play(self, playid):
        self._loaded_play_id = playid
        self._current_index = list(self.plays.keys()).index(playid)
        self._current_play = self.plays[playid]
        self.entry_wigits.machine_cb.var.set(self._current_play.machine.get_name())
        self.session_date.set(self._current_play.session_date.strftime("%Y-%m-%d"))
        self.session_frame.casino.var.set(self._current_play.casino)
        self.entry_wigits.dt.var.set(self._current_play.start_time)
        self.entry_wigits.end_dt.var.set(self._current_play.end_time)
        self.entry_wigits.bet.var.set(self._current_play.bet)
        self.entry_wigits.denom_cb.var.set(self._current_play.denom)
        self.entry_wigits.play_type.var.set(self._current_play.play_type)
        self.entry_wigits.cashin.var.set(self._current_play.cash_in)
        self.entry_wigits.cashout.var.set(self._current_play.cash_out)
        self.update_pnl()
        self.entry_wigits.initial_state.set_text(self._current_play.state)
        self.entry_wigits.note.set_text(self._current_play.note)

        self.entry_wigits.start_entry.var.set(self._current_play.start_image)
        self.entry_wigits.end_entry.var.set(self._current_play.end_image)
        self.play_imgs = self._current_play.addl_images
        self.entry_wigits.update_table(self)

        self.hand_pay = self._current_play.hand_pays
        self.entry_wigits.update_hand_pay_table(self)

        self.image_buttons.save_button.configure(state="normal", bootstyle="normal")

    def create_play(self, machine_name=None):
        if machine_name is None:
            machine_name = self.entry_wigits.machine_cb.var.get()
        self._current_play = PlayFactory.get_play(machine_name)
        self.update_all_play_values()

    def update_all_play_values(self):
        self.update_session_date()
        self.update_casino()
        self.update_start_datetime()
        self.update_end_datetime()
        self.update_bet()
        self.update_denom()
        self.update_play_type()
        self.update_cashin()
        self.update_cashout()
        self.update_init_state()
        self.update_play_note()
        self.update_start_image()
        self.update_end_image()
        self.update_addl_images()
        self.update_handpays()

    def editing_play(self):
        return self._current_index is not None

    def save(self):
        if self.image_buttons.save_button.state() == "disabled":
            return

        if self._current_play is None:
            self.create_play()

        if self.editing_play():
            li = list(self.plays.items())
            li[self._current_index] = (
                self._current_play.identifier,
                self._current_play,
            )
            self.plays = dict(li)
            self.update_all_play_values()
        else:
            self.update_all_play_values()
            if self._current_play.identifier in self.plays:
                button = Messagebox.okcancel(
                    f"You are not editing an exiting play and this will overwrite a play. Proceed?",
                    f"Overwrite Warning",
                )
                if button != "OK":
                    return
            self.plays[self._current_play.identifier] = self._current_play

        self.session_table.update_table()

        # clears all entry values
        self._current_index = None
        self.entry_wigits.dt.var.set("")
        self.entry_wigits.end_dt.var.set("")
        self.entry_wigits.bet.var.set(0)
        self.entry_wigits.cashin.var.set(self._current_play.cash_out)
        self.entry_wigits.cashout.var.set(0)
        self.entry_wigits.initial_state.clear()
        self.ttk_state.set("")
        self.entry_wigits.note.clear()
        self.entry_wigits.start_entry.var.set("")
        self.entry_wigits.end_entry.var.set("")

        self.play_imgs.clear()
        self.entry_wigits.update_table(self)

        self.hand_pay.clear()
        self.entry_wigits.update_hand_pay_table(self)

        # resets the save button to disabled
        self.image_buttons.save_button.configure(state="disabled")
        self.image_buttons.save_session_button.configure(state="enabled")
        self.create_play()

    def save_session(self):
        # gets the path to the data save
        save_path = join(dirname(dirname(__file__)), "Data")
        file_path = join(save_path, "slots_data.csv")

        makedirs(save_path, exist_ok=True)

        while True:
            try:
                f = open(file_path, "a+")
            except Exception:
                Messagebox.show_error(
                    f'Cannot open "{file_path}".\nPlease close and try again',
                    "File Open Error",
                )
            else:
                f.close()
                break

        new_path = ""
        if list(self.plays.values())[0].start_image:
            new_path = join(
                dirname(dirname(list(self.plays.values())[0].start_image)),
                f"Sorted/{self.session_date.get()}",
            )

            try:
                makedirs(new_path, exist_ok=False)
            except Exception:
                pass

        pics_to_remove = []
        # move all images and update play values with new location
        try:
            playId = ""
            with open(file_path, "a+", newline="") as csvfile:
                writer = csv.writer(csvfile)
                for p in list(self.plays.values()):
                    playId = p.identifier
                    if p.start_image and new_path:
                        pics_to_remove.append(p.start_image)
                        p.start_image = move(p.start_image, new_path)
    
                    pics_to_remove.extend(p.addl_images)
                    for i, a in enumerate(p.addl_images):
                        p.addl_images[i] = move(a, new_path)
    
                    if p.end_image and new_path:
                        pics_to_remove.append(p.end_image)
                        p.end_image = move(p.end_image, new_path)
    
                for row in p.get_csv_rows():
                    writer.writerow(row)
        except Exception as e:
            Messagebox.show_error(f'Error saving session at {playId}. Aborting. You will need to manually fix up a few things to continue.\n{e}', 'Error Saving')
            return

        self.imgs = [ d for d in self.imgs if (d[0] not in pics_to_remove) ]
        self.imgs = sorted(self.imgs, key=lambda item: item[2])
        self.display_first_image()

        self.plays.clear()
        self.session_table.update_table()

        self.image_buttons.set_image_adders("normal")

        self.image_buttons.save_button.configure(state="disabled")
        self.image_buttons.save_session_button.configure(state="disabled")
        self.session_date.set(self.default_session_date)

    def image_is_in_current_play(self, img):
        return (
            (img in self.play_imgs)
            or (img == self.entry_wigits.start_entry.var.get())
            or (img == self.entry_wigits.end_entry.var.get())
        )

    def display_first_image(self):
        if len(self.imgs) == 0:
            return

        self.pointer = 0
        self.display_image()

        current_image_path = self.imgs[self.pointer][0]
        if self.image_is_in_current_play(current_image_path):
            self.image_buttons.set_image_adders("disabled")
        else:
            self.image_buttons.set_image_adders("normal")

    def remove_play(self, key):
        del self.plays[key]
        if len(self.plays) == 0:
            self.image_buttons.save_session_button.configure(state="disabled")

    def check_save_valid(self):
        casino = self.session_frame.casino.var.get()
        dt = self.entry_wigits.dt.var.get()
        machine = self.entry_wigits.machine_cb.var.get()
        play_type = self.entry_wigits.play_type.var.get()

        bet = self.entry_wigits.bet.var.get()
        cashin = self.entry_wigits.cashin.var.get()
        cashout = self.entry_wigits.cashout.var.get()

        if (
            casino == ""
            or dt == self.default_dt
            or dt == ""
            or machine == "Select Machine"
            or play_type == ""
        ):
            self.image_buttons.save_button.configure(state="disabled")
        elif bet == "0" or cashin == "0" or cashout == "0":
            self.image_buttons.save_button.configure(
                state="normal", bootstyle="warning"
            )
        else:
            self.image_buttons.save_button.configure(state="normal", bootstyle="normal")

    def save_externals(self):
        externals = {
            "casino_entry_values.csv": self.casino_values,
            "machine_entry_values.csv": self.machine_values,
            "denom_entry_values.csv": self.denom_values,
            "playtype_entry_values.csv": self.play_types,
        }
        for f, var in externals.items():
            file_path = join(dirname(dirname(__file__)), f)
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                for item in var:
                    writer.writerow([item])

    def reset_play(self):
        self._current_index = None
        self.session_table.clear_selection()
        if self._current_play is None:
            return
        self.create_play()

    def setup_keybinds(self):
        self.bind("<FocusIn>", lambda _: self.check_save_valid())
        self.bind("<FocusOut>", lambda _: self.check_save_valid())

        self.bind("<Control-s>", lambda _: self.save())
        self.bind("<Prior>", lambda _: self.image_buttons.prev_button_command(self))
        self.bind("<Next>", lambda _: self.image_buttons.next_button_command(self))
        self.bind("<Home>", lambda _: self.image_buttons.return_button_command(self))
        self.bind(
            "<Control-Key-1>", lambda _: self.image_buttons.start_button_command(self)
        )
        self.bind(
            "<Control-Key-2>", lambda _: self.image_buttons.add_button_command(self)
        )
        self.bind(
            "<Control-Key-3>", lambda _: self.image_buttons.end_button_command(self)
        )
        self.bind("<Escape>", lambda _: self.reset_play())

    def load_test_play(self):
        self.session_frame.casino.var.set("ilani")
        self.session_date.set(datetime.datetime(2024, 5, 1).strftime("%Y%m%d"))
        self.entry_wigits.dt.var.set(
            datetime.datetime(2024, 5, 1, 12, 3, 5).strftime("%Y-%m-%d %H:%M:%S")
        )
        self.entry_wigits.machine_cb.var.set("Lucky Wealth Cat")
        self.entry_wigits.cashin.var.set("100.00")
        self.entry_wigits.bet.var.set("1.20")
        self.entry_wigits.play_type.var.set("AP")
        self.entry_wigits.initial_state.text.insert("1.0", "This, is; a (state): 1223")
        self.entry_wigits.cashout.var.set("120.00")


if __name__ == "__main__":
    # calls the app
    root = App()
    # runs the main loop
    root.mainloop()
    # saves the external values to their csv files
    root.save_externals()
