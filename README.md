# Slot logger
Use at your own risk

# Prerequisites
* Python 3.12 or newer must be installed
* This program: you can get this by selecting the code button above and download zip
* Extract this to a known location
  
# Getting started (do this once the first time you use the program)
* Navigate to where the program was extracted
* Edit the casino_entry_values.csv to include the casinos you are intersted in. You can add to this dynamically while running if you wish.
* Edit the machine_entry_values.csv to include the machines you are interested in. I recommend removing any you are not likely to log. You can always add more later if you start playing them.
* Edit the denom_entry_values.csv to include the denominations you play. There is currently a bug preventing the adding of denominations dynamically.
* Open a command prompt or powershell prompts at this location
* run `pip install -r requirements.txt`

# Running the program
* open a command prompt and navigate to the folder where the program was extracted
* run `py Programs\threaded_main.py`

# Using the program
1. File->Open Folder
   * This can take a while. I had 6000 files. It took 25 minutes to load on my system
   * If the images are not correctly sized you can use File->Set Scale to change the scale. I use 7. Bigger numbers will make the image smaller.
2. Select the casino for this session. If it is not in the list, you can use File->Add Casino to add it to the list
3. Use Prev/Next buttons to navigate to the first picture that is part of the play
4. Use Delete Image to delete the image FROM DISK if you are not intersted in keeping it
5. Select the machine from the machine drop down. If it is not in the list, you can use File->Add Machine to add it to the list
6. Use Set Start to add the first picture for the play. If this is the first play of the session, this will set the session_date
7. Set the bet, playtype, denomination, Cash In, and Initial state as appropriate
8. Navigate to the next picture. If this is a picture of the end state, use Set End If this is a picture relevant to the play that you want to keep but not the end, use Add image.
9. Fill in the Note and Cash Out as appropriate
10. If you have a Hand Pay, you can use "Add Hand Pay" if you wish to associate it with this play.
11. For some machines (Frankenstein, Power Push, Lucky Wealth Cat/Buddha, Pinwheel Prizes) there is a helper to keep the state formatted consistantly. More will be added eventually.
12. Return to start will take you to the first picture
13. Remove Image will remove the current image from the current play
14. Save Play will save the play to memory and a generated id will be listed in the PlayID box
15. Save Session will write the plays to Data\slots_data.csv and will MOVE all the files in the plays to a folder parallel to the current image folder named "Sorted" and in a subfolder named for the session date
16. Shortcuts:
    * Ctrl-s : Save
    * PgUp : Previous Image
    * PgDn : Next Image
    * Home : Return to Start Image
    * Ctrl-1 : Set Start Image
    * Ctrl-2 : Add Image
    * Ctrl-3 : Set End Image

# Known bugs/limitations
* Once you save you cannot open a folder
* Removing an image does not enable the button to allow it to be added, you must navigate away and then back if you want to readd it.
* Add denom does not add a new denomination to the drop-down (but it will add it to the file)
* Tax rate is set to 27% and is not currently configurable.
* Using the state helper does not update the state display. You must click into and then out of the Initial State box to see it
* You cannot reload/edit plays once it's been saved
* You must save a picture to set the session date, so if you don't use pics to track, this will not be useful yet
* You cannot delete a hand pay once added to a play. You need to create a completely new play to fix
* There is no reset button to reset the current play

  
