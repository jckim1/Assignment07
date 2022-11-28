#------------------------------------------#
# Title: CD Inventory.py
# Desc: Adapting the previous exercises with Classes and Functions to maintain CD inventory
# Change Log:
# DBiesinger, 2030-Jan-01, Created File
# Jesse Kim, 2022-Nov-20, Modified File
#------------------------------------------#

import pickle as p

# -- DATA -- #
uChoice = '' # User input
lstTbl = []  # list of lists to hold data
dRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing data for inventory"""

    @staticmethod
    def new_row():
        """Function to create a dictionary row from user inputs and append to list
        Args:
            None.
        Returns:
            None.
        """
        intID, album, artist = IO.user_input()
        dRow = {'ID': intID, 'Title': album, 'Artist': artist}
        lstTbl.append(dRow)
        
    @staticmethod
    def cd_delete(delete_id):
        """Function to search for the CD user wants to delete, if the matching ID for the CD is found, delete row
        Args:
            CD user wants to delete
        Returns:
            None.
        """
        
        index = -1
        for count, value in enumerate(lstTbl): # if cdid matches user key, then delete the data from list of dict
            if delete_id == value['ID']:
                index = count
                break
        if index != -1:
            lstTbl.pop(index)

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries
        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        Returns:
            None.
        """
        with open(file_name, 'rb') as f:
            t_file = p.load(f)
            for row in t_file:
                table.append(row)

    @staticmethod
    def save_inventory(filename, table):
        """Function to save list of dictionaries to file
        Args:
            None.
        Returns:
            None.
        """

        with open(filename, 'wb') as f:
            p.dump(table, f)


# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user
        Args:
            None.
        Returns:
            None.
        """
        print('Menu\n\n[l] Load Inventory from file\n[a] Add CD\n[i] Display Current Inventory\n[d] Delete CD from Inventory\n[s] Save Inventory to file\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection
        Args:
            None.
        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('What would you like to do? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def disp_inv(table):
        """Displays current inventory table
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        Returns:
            None.
        """
        print('======= Current Inventory: =======')
        print('ID\tAlbum (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def user_input():
        """Asks user to input values for ID, Album, and Artist
        Args:
            None
        Returns:
            User inputs for ID, Album, and Artist name
        """
        while True:
            try:
                cd_id = int(input('Enter ID: '))
            except ValueError as e:
                print('You must enter an integer to continue.') 
            album = input('Enter the title of the album: ').strip()
            artist = input('Enter the name of the artist: ').strip()
            return cd_id, album, artist
          
        
        
# 1. When program starts, read in the currently saved Inventory
# FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    uChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if uChoice == 'x':
        break
    # 3.2 process load inventory
    if uChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled ')
        if strYesNo.lower() == 'yes':
            print('loading...')
            try:
                FileProcessor.read_file(strFileName, lstTbl)
            except FileNotFoundError as e:
                print('That file does not exist in this directory.')
        else:
            input('canceling...Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.disp_inv(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif uChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # method call to IO.user_input() in line 29 so no need to add here or it creates an infinite add loop
        # 3.3.2 Add item to the table
        DataProcessor.new_row()
        IO.disp_inv(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif uChoice == 'i':
        IO.disp_inv(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif uChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.disp_inv(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                deliD = int(input('Which ID would you like to delete? ').strip())
            except ValueError as e:
                print('You must enter an integer.')
        # 3.5.2 search thru table and delete CD
            DataProcessor().cd_delete(deliD)
            IO.disp_inv(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif uChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.disp_inv(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor().save_inventory(strFileName, lstTbl)
#        else:
#           input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')
