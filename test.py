from tksheet import Sheet
import tkinter as tk
import tkinter.messagebox as msg
import tkinter.simpledialog as sd

class demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight=1)  # This configures the window's escalators
        self.grid_rowconfigure(0, weight=1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.sheet = Sheet(self.frame, data=[[]])  # set up empty table
        self.sheet.grid(row=0, column=0, sticky="nswe")
        self.sheet.enable_bindings(bindings=  # enable table behavior
                                   ("single_select",
                                    "select_all",
                                    "column_select",
                                    "row_select",
                                    "drag_select",
                                    "arrowkeys",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",  # rc = right click
                                    "copy",
                                    "cut",
                                    "paste",
                                    "delete",
                                    "undo",
                                    "edit_cell"
                                    ))
        # Note that options that change the structure/size of the table (e.g. insert/delete col/row) are disabled

        # make sure that pasting data won't change table size
        self.sheet.set_options(expand_sheet_if_paste_too_big=False)
        # bind specific events to my own functions
        self.sheet.extra_bindings("end_edit_cell", func=self.cell_edited)
        self.sheet.extra_bindings("end_paste", func=self.cells_pasted)
        label = "Change column name"  # Add option to the right-click menu for column headers
        self.sheet.popup_menu_add_command(label, self.column_header_change, table_menu=False, index_menu=False, header_menu=True)

    # Event functions
    def cell_edited(self, info_tuple):
        r, c, key_pressed, updated_value = info_tuple  # break the info about the event to individual variables
        if check_input(updated_value):
            pass  # go do stuff with the updated table
        else:
            msg.showwarning("Input Error", "'" + updated_value + "' is not a legal value")
            pass  # what do I do here? How do I make tksheet *not* insert the change to the table?

    def cells_pasted(self, info_tuple):
        key_pressed, rc_tuple, updated_array = info_tuple  # break the info about the event to individual variables
        r, c = rc_tuple  # row & column where paste begins
        if check_input(updated_array):
            pass  # go do stuff with the updated table
        else:
            msg.showwarning("Input Error", "pasted array contains illegal values")
            pass  # what do I do here? How do I make tksheet *not* insert the change to the table?

    def column_header_change(self):
        r, c = self.sheet.get_currently_selected()
        col_name = sd.askstring("User Input", "Enter column name:")
        if col_name is not None and col_name != "":  # if user cancelled (or didn't enter anything), do nothing
            self.sheet.headers([col_name], index=c)  # This does not work - it always changes the 1st col
            self.sheet.redraw()


# from here down is test code
def check_input(value):  # instead of actual data testing we let the tester choose a pass/fail response
    return msg.askyesno("Instead of input checking","Did input pass entry checks?")


test = demo()
lst = ["hello", "world"]
test.sheet.insert_column(values=lst)
lst = [0, "hello", "yourself"]
test.sheet.insert_column(values=lst)
test.mainloop()
