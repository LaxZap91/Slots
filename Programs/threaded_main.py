
# imports basic tkinter stuff
import ttkbootstrap as ttk
# imports external dialog boxes
from ttkbootstrap.dialogs import Querybox, Messagebox

# imports dialog box for opening a directory
from tkinter.filedialog import askdirectory

# imports custom label and other combos
from Scripts.ComboboxLabel import ComboboxLabel
from Scripts.EntryLabel import EntryLabel
from Scripts.MoneyEntryLabel import MoneyEntryLabel
from Scripts.LabelLabel import LabelLabel
from Scripts.LargeEntryLabel import LargeEntryLabel

# imports threaded getting image date
from Scripts.get_imgs_data import multi_get_img_data

# imports file maipulations
from os import makedirs, remove
from os.path import join, dirname, basename, join

from shutil import move

# imports image access
from PIL import Image, ImageTk

# imports access to HEIC files with pillow ( PIL )
from pillow_heif import register_heif_opener

# imports csv access
import csv

# allows pillow to open HEIC images, using 8 threads
register_heif_opener(decode_threads=8, thumbnails=False)



class App(ttk.Window):
    def __init__(self):
        # list of all image data ( image path, image type, image time )
        self.imgs = []
        # list of image paths for a single play
        self.play_imgs = []
        # tuple of all play types
        self.play_type = ('AP', 'Gamble', 'Misplay', 'Non-play', 'Science', 'Tip', 'Tax Consequence')
        
        # gets the values that goes in the casino entry field
        with open(f'casino_entry_values.csv', 'r') as csvfile:
            # reads the casino entry values from the csv file
            casino_values = list(csv.reader(csvfile))
            # gets the values in a readable format, also flattens any lists
            self.casino_values = [val for sublist in casino_values for val in sublist]
        
        # gets the values that goes in the machine entry field
        with open(f'machine_entry_values.csv', 'r') as csvfile:
            # readse the machine entry values from the csv file
            machine_values = list(csv.reader(csvfile))
            self.machine_values = [val for sublist in machine_values for val in sublist]
            
        # the pointer that points to the current image
        self.pointer = 0
        
        # initializes the window
        super().__init__()
        # sets the window title to slots
        self.title('Slots')
        # sets the minimum size to 450 wide and 705 tall
        self.minsize(450, 705)
        # sets the starting size to 1000 wide and 800 tall
        self.geometry('1000x800')
        # sets the icon photo to a little slot machine
        self.iconphoto(False, ttk.PhotoImage(file=r'Programs\Icon\slot_machine_icon.png'))
        
        # initializes tkinter string variables for the image for the start and end of a play
        self.start_img = ttk.StringVar()
        self.end_img = ttk.StringVar()
        
        # creates the data entry wigits and places them on the left
        self.entry_wigits = EntryWigits(self)
        self.entry_wigits.place(x=5, y=5)
        
        # creates the image display and places them on the right
        self.image_display = ImageDisplay(self)
        self.image_display.place(x=440, y=5)
        
        # creates the buttons that control the play and places them in the middle
        self.image_buttons = ImageButtons(self)
        self.image_buttons.place(x=220, y=5)
        
        # creates the file menu at the top
        self.make_menu()
        
        # binds focusing in or out of an wigit to checking if you are able to save
        self.bind('<FocusIn>', lambda _: self.check_save_valid())
        self.bind('<FocusOut>', lambda _: self.check_save_valid())
        # binds CTRL-s to save the current play
        self.bind('Control-s', lambda _: self.save())
    
    def make_menu(self):
        # creates the menu wigit
        menu = ttk.Menu(master=self)
        self.configure(menu=menu)
        
        # creates sub menu
        file_menu = ttk.Menu(menu, tearoff=False)
        # adds a button in the sub menu that opens a folder
        file_menu.add_command(label='Open Folder', command=self.open_folder)
        file_menu.add_separator()
        # adds a button that will open a sub window to enter a casino in
        file_menu.add_command(label='Add Casino', command=self.add_casino)
        # adds a button that will open a sub window to enter a machine in
        file_menu.add_command(label='Add Machine', command=self.add_machine)
        menu.add_cascade(label='File', menu=file_menu)
    
    def open_folder(self):
        # opens a file menu to open a directory
        directory = askdirectory(mustexist=True)
        if directory == '':
            return
        
        # multi threads geting the image data ( image path, image type, image date )
        self.imgs = multi_get_img_data(directory)
        self.imgs = [t for t in self.imgs if t is not None]
        print('Loaded')
        
        # does nothing else if there are not images in the directory
        if len(self.imgs) == 0:
            return
        
        # sorts images in the image list by date
        self.imgs = sorted(self.imgs, key=lambda item: item[2])
        # displays the oldest image
        self.display_image()   
    
    def add_casino(self):
        # opens a window to ask for a casino
        new_casino = Querybox.get_string(prompt='Enter a casino', title='Casino Entry')
        
        # adds the new value to the casino values list if it is not None and not in it already
        if (new_casino is not None) and (new_casino not in self.casino_values):
            self.casino_values.append(new_casino)
    
    def add_machine(self):
        # opens a window to ask for a machine
        new_machine = Querybox.get_string(prompt='Enter a machine', title='Machine Entry')
        
        # adds the new value to the machine values list if it is not None and not in it already
        if (new_machine is not None) and (new_machine not in self.machine_values):
            self.machine_values.append(new_machine)

    def display_image(self):
        # opens the image at the current pointer
        with Image.open(self.imgs[self.pointer][0]) as image:
            # reduces the image size if it larger than 450 by 450 pixels
            if image.size[0] >= 450 or image.size[1] >= 450:
                # reduces the image by a factor of 10 if it is a .HEIC or .PNG file
                if self.imgs[self.pointer][1] =='.HEIC' or self.imgs[self.pointer][1] == '.PNG':
                    image = image.reduce(10)
                # otherwise reduces the image by a factor of 2
                else:
                    image = image.reduce(5)
            
            global imagetk
            # turns the image into a image that tkinter can display
            imagetk = ImageTk.PhotoImage(image)
            
            # gets the image dimensions and divides them by 2
            x, y = image.size
            x, y = x/2, y/2
            
            # clears the image canvas
            self.image_display.canvas.delete('all')
            # adds the image to the canvas
            self.image_display.canvas.create_image(x, y, image=imagetk)
    
    def save(self):
        # does nothing if the save button is disabled
        if self.image_buttons.save_button.state() == 'disabled':
            return
        
        # gets all entry values
        casino = self.entry_wigits.casino.var.get()
        date = self.entry_wigits.date.var.get()
        machine = self.entry_wigits.machine.var.get()
        cash_in = self.entry_wigits.cashin.var.get()
        bet = self.entry_wigits.bet.var.get()
        play_type = self.entry_wigits.play_type.var.get()
        initial_state = self.entry_wigits.initial_state.get_text()
        cash_out = self.entry_wigits.cashout.var.get()
        note = self.entry_wigits.note.get_text()
        start_img = self.entry_wigits.start_entry.var.get()
        end_img = self.entry_wigits.end_entry.var.get() 
        other = self.play_imgs
        # makes all the values into a list
        values = [casino, date, machine, cash_in, bet, play_type, initial_state, cash_out, note, start_img, end_img, other]
        
        # gets the path to the data save
        file_path = join(dirname(dirname(__file__)), 'Data\\slots_data.csv')
        # writes the entry values to the path
        with open(file_path, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(values)
        
        # clears all entry values
        self.entry_wigits.casino.var.set('')
        self.entry_wigits.date.var.set('')
        self.entry_wigits.machine.var.set('')
        self.entry_wigits.cashin.var.set('0')
        self.entry_wigits.bet.var.set('0')
        self.entry_wigits.play_type.var.set('')
        self.entry_wigits.initial_state.clear()
        self.entry_wigits.cashout.var.set('0')
        self.entry_wigits.note.clear()
        self.entry_wigits.start_entry.var.set('')
        self.entry_wigits.end_entry.var.set('') 
        self.play_imgs.clear()

        self.entry_wigits.update_table()

        # resets the save button to disabled
        self.image_buttons.save_button.configure(state='disabled')
    
    def check_save_valid(self):
        # gets the entry values that need to be filled to save
        casino = self.entry_wigits.casino.var.get()
        date = self.entry_wigits.date.var.get()
        machine = self.entry_wigits.machine.var.get()
        play_type = self.entry_wigits.play_type.var.get()
        
        # checks if they are empty
        if casino=='' or date=='' or machine=='' or play_type=='':
            # disables the save button
            self.image_buttons.save_button.configure(state='disabled')
        else:
            # enables the save button
            self.image_buttons.save_button.configure(state='normal')
        
    def save_externals(self):
        # gets the path to casino entry values csv file
        file_path = join(dirname(dirname(__file__)), 'casino_entry_values.csv')
        # saves the casino entry values to the csv file
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for item in self.casino_values:
                writer.writerow([item])
        
        # gets teh path to the machine entry values csv file
        file_path = join(dirname(dirname(__file__)), 'machine_entry_values.csv')
        # saves the machine entry values to the csv file
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for item in self.machine_values:
                writer.writerow([item])

class EntryWigits(ttk.Frame):
    def __init__(self, parent):
        # initializes the frame
        super().__init__(master=parent)
        
        # adds the casino entry, readonly so you cannot enter your own values
        self.casino = ComboboxLabel(self, 'Casino', parent.casino_values, state='readonly')
        self.casino.pack(fill='x')
        
        # adds the date entry, readonly so you cannot enter your own values
        self.date = EntryLabel(self, 'Date', state='readonly')
        self.date.pack(fill='x')
        
        # adds the machine entry, readonly so you cannot enter your own values
        self.machine = ComboboxLabel(self, 'Machine', parent.machine_values, state='readonly')
        self.machine.pack(fill='x')
        
        # adds the cash in entry label, only allows float-likes
        self.cashin = MoneyEntryLabel(self, 'Cash In')
        self.cashin.pack(fill='x')
        # binds entering the entry to selecting all characters
        self.cashin.bind('<FocusIn>', lambda _: self.cashin.entry.selection_range(0, ttk.END))
        
        # adds the bet entry label, only allows float-likes
        self.bet = MoneyEntryLabel(self, 'Bet')
        self.bet.pack(fill='x')
        # binds entering the entry to selecting all characters
        self.bet.bind('<FocusIn>', lambda _: self.bet.entry.selection_range(0, ttk.END))
        
        # adds the play type entry, readonly so you cannot enter your own values
        self.play_type = ComboboxLabel(self, 'Play Type', parent.play_type, state='readonly')
        self.play_type.pack(fill='x')
        
        # adds the initial state entry
        self.initial_state = LargeEntryLabel(self, 'Initial State')
        self.initial_state.pack(fill='x')
        
        # adds the cash out entry, only allows float-likes
        self.cashout = MoneyEntryLabel(self, 'Cash Out')
        self.cashout.pack(fill='x')
        # binds entering the entry to selecting all characters
        self.cashout.bind('<FocusIn>', lambda _: self.cashout.entry.selection_range(0, ttk.END))
        
        # adds the profit loss amount
        self.profit_loss = LabelLabel(self, 'Profit/Loss', self.cashout.var.get() - self.cashin.var.get())
        # binds keypresses to updating the ammount
        parent.bind('<Key>', lambda _: self.profit_loss.var.set(self.cashout.var.get() - self.cashin.var.get()))
        self.profit_loss.pack(fill='x')
        
        # adds the note entry
        self.note = LargeEntryLabel(self, 'Note', height=8)
        self.note.pack(fill='x')
        
        # adds the start image entry, readonly so you cannot enter your own values
        self.start_entry = EntryLabel(self, 'Start Image', parent.start_img, state='readonly')
        self.start_entry.pack(fill='x')

        # adds the end image entry, readonly so you cannot enter your own values
        self.end_entry = EntryLabel(self, 'End Image', parent.end_img, state='readonly')
        self.end_entry.pack(fill='x')
        
        # adds the image table,
        self.table = ttk.Treeview(self, columns='imgs', show='headings')
        self.table.heading('imgs', text='Images')
        self.table.pack()
    
    def update_table(self, parent):
        # clears the table
        self.table.delete(*self.table.get_children())
        # adds all play imgs to the table
        for item in parent.play_imgs:
            self.table.insert(parent='', index=ttk.END, values=item)
    
class ImageButtons(ttk.Frame):
    def __init__(self, parent):
        # initializes the frame
        super().__init__(master=parent)
        # adds 2 columns and 4 rows
        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        
        # adds the previous button that calls self.prev_button_command when pressed
        self.prev_button = ttk.Button(self, text='Prev', command=lambda: self.prev_button_command(parent))
        self.prev_button.grid(column=0, row=0, sticky='nsew', padx=(0, 3), pady=(0, 3))
        
        # adds the next button that calls self.next_button_command when pressed
        self.next_button = ttk.Button(self, text='Next', command=lambda: self.next_button_command(parent))
        self.next_button.grid(column=1, row=0, sticky='nsew', padx=(3, 0), pady=(0, 3))
        
        # adds the set start button that calls self.start_button_command when pressed
        self.start_button = ttk.Button(self, text='Set Start', command=lambda: self.start_button_command(parent))
        self.start_button.grid(column=0, row=1, sticky='nsew', padx=(0, 3), pady=(3, 3))
        
        # adds the set end button that calls self.end_button_command when pressed
        self.end_button = ttk.Button(self, text='Set End', command=lambda: self.end_button_command(parent))
        self.end_button.grid(column=1, row=1, sticky='nsew', padx=(3, 0), pady=(3, 3))
        
        # adds the add image button that calls self.add_button_command when pressed
        self.add_button = ttk.Button(self, text='Add Image', command=lambda: self.add_button_command(parent))
        self.add_button.grid(column=0, row=2, sticky='nsew', padx=(0, 3), pady=(3, 3))
        
        # adds the remove image button that calls self.remove_button_command when pressed
        self.remove_button = ttk.Button(self, text='Remove Image', command=lambda: self.remove_button_command(parent))
        self.remove_button.grid(column=1, row=2, sticky='nsew', padx=(3, 0), pady=(3, 3))
        
        # adds the save button that calls parent.save when pressed
        self.save_button = ttk.Button(self, text='Save Play', command=lambda: parent.save(), bootstyle='success')
        self.save_button.grid(column=0, row=3, sticky='nsew', padx=(0, 3), pady=(3, 0))
        
        # adds the delete image button that calls self.delete_button_command when pressed
        self.delete_button = ttk.Button(self, text='Delete Image', command=lambda: self.delete_button_command(parent), bootstyle='danger')
        self.delete_button.grid(column=1, row=3, sticky='nsew', padx=(3, 0), pady=(3, 0))

    def next_button_command(self, parent):
        # increases the pointer by one to the max of the length of the image list
        parent.pointer = min((parent.pointer+1), (len(parent.imgs)-1))
        # updates the image display
        parent.display_image()
    
    def prev_button_command(self, parent):
        # decreases the pointer by one to the minimum of 0
        parent.pointer = max((parent.pointer-1), 0)
        parent.display_image()
    
    def start_button_command(self, parent):
        # does nothing if there are no images
        if len(parent.imgs) == 0:
            return
        
        # gets the path of the current image
        old_path = parent.imgs[parent.pointer][0]
        
        # does nothing if the image is already in
        if 'Sorted' in old_path:
            return
        
        # gets the file name from the path
        file_name = basename(old_path)
        
        # sets the date to the date of the image
        parent.entry_wigits.date.var.set(parent.imgs[parent.pointer][2][:8])
        
        # makes the new path
        new_path = join(dirname(dirname(old_path)), fr'Sorted\{parent.imgs[parent.pointer][2][:8]}')
        
        # makes a directory at the new path if it does not exist
        try: makedirs(new_path)
        except FileExistsError: pass
        
        # moves the image to the new path
        move(old_path, new_path)
        
        # sets the image path in the image list to the new path
        parent.imgs[parent.pointer][0] = join(new_path, file_name)
        # resorts the image list by date
        parent.imgs = list(sorted(parent.imgs, key=lambda item: item[2]))
        
        # sets the start entry to the new path of the image
        parent.entry_wigits.start_entry.var.set(parent.imgs[parent.pointer][0])
    
    def end_button_command(self, parent):
        # does nothing if there is no start image
        if parent.entry_wigits.start_entry.var.get() == '':
            return
        
        # does nothing if ther are no images
        if len(parent.imgs) == 0:
            return
        
        # gets the path of the current image
        old_path = parent.imgs[parent.pointer][0]
        
        # does nothing if the image is already in
        if 'Sorted' in old_path:
            return
        
        # gets the file name from the path
        file_name = basename(old_path)
        
        # makes the new path
        new_path = join(dirname(dirname(old_path)), fr'Sorted\{parent.entry_wigits.date.var.get()}')
        
        # makes a directory at the new path if it does not exist
        try: makedirs(new_path)
        except FileExistsError: pass
        
        # moves the image to the new path
        move(old_path, new_path)
        
        # sets the image path in the image list to the new path
        parent.imgs[parent.pointer][0] = join(new_path, file_name)
        # resorts the image list by date
        parent.imgs = list(sorted(parent.imgs, key=lambda item: item[2]))
        
        # sets the end entry to the new path of the image
        parent.entry_wigits.end_entry.var.set(parent.imgs[parent.pointer][0])
    
    def add_button_command(self, parent):
        # does nothing if there is no start image
        if parent.entry_wigits.start_entry.var.get() == '':
            return
        
        # does nothing if there are no images
        if len(parent.imgs) == 0:
            return
        
        # gets the path of the current image
        old_path = parent.imgs[parent.pointer][0]
        
        # does nothing if the image is already in
        if 'Sorted' in old_path:
            return
        
        # gets the file name from the path
        file_name = basename(old_path)
        
        # makes the new path
        new_path = join(dirname(dirname(old_path)), fr'Sorted\{parent.entry_wigits.date.var.get()}')
        
        # makes a directory at the new path if it does not exist
        try: makedirs(new_path)
        except FileExistsError: pass
        
        # moves the image to the new path
        move(old_path, new_path)
        
        # sets the image path in the image list to the new path
        parent.imgs[parent.pointer][0] = join(new_path, file_name)
        # resorts the image list by date
        parent.imgs = list(sorted(parent.imgs, key=lambda item: item[2]))
        
        # adds the new image path to the play images list
        parent.play_imgs.append(parent.imgs[parent.pointer][0])
        
        # updates the table
        parent.entry_wigits.update_table(parent)
    
    def delete_button_command(self, parent):
        # does nothing if there are no images
        if len(parent.imgs) == 0:
            return
        
        # gets the path of the image to be deleted
        path = parent.imgs[parent.pointer][0]
        # opens a confirmation that you want to delete the image
        confirmation = Messagebox.show_question(f'Are you sure you want to delete this image:\n{path}',
                                                'Image Deletion Confirmation',
                                                buttons=['No:secondary', 'Yes:warning'])
        
        # does not nothing if the confimation result is not Yes
        if confirmation != 'Yes':
            return
        
        # deletes the image
        remove(path)
        # removes the image from the images list
        parent.imgs.pop(parent.pointer)
        
        # removes the image from the start entry, end entry and play images table
        if parent.entry_wigits.start_entry.var.get() == path:
            parent.entry_wigits.start_entry.var.set('')
        elif parent.entry_wigits.end_entry.var.get() == path:
            parent.entry_wigits.end_entry.var.set('')
        elif path in parent.play_imgs:
            parent.play_imgs.remove(path)
            parent.entry_wigits.update_table(parent)
    
    def remove_button_command(self, parent):
        # does nothing if there are no images
        if len(parent.imgs) == 0:
            return
        
        # gets path of the image to be removed from the play
        path = parent.imgs[parent.pointer][0]
        
        # removes the image from the start entry, end entry, and play images table
        if parent.entry_wigits.start_entry.var.get() == path:
            parent.entry_wigits.start_entry.var.set('')
        elif parent.entry_wigits.end_entry.var.get() == path:
            parent.entry_wigits.end_entry.var.set('')
        elif path in parent.play_imgs:
            parent.play_imgs.remove(path)
            parent.entry_wigits.update_table(parent)

class ImageDisplay(ttk.Frame):
    def __init__(self, parent):
        # initializes the frame
        super().__init__(master=parent)
        # creates the canvas with width 750 and height 750
        self.canvas = ttk.Canvas(master=self, width=750, height=750)
        self.canvas.pack(fill='both')



if __name__ == '__main__':
    # calls the app
    root = App()
    # runs the main loop
    root.mainloop()
    # saves the external values to their csv files
    root.save_externals()