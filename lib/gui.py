import logging
import tkinter
import datetime
import tkinter.scrolledtext as ScrolledText
from tkinter import ttk
from lib import main

# (but you can also reference this getLogger instance from other modules and other threads by passing the same argument name...allowing you to share and isolate loggers as desired)
# ...so it is module-level logging and it takes the name of this module (by using __name__)
# recommended per https://docs.python.org/2/library/logging.html
module_logger = logging.getLogger(__name__)


class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent

        self.grid()

        var1 = tkinter.IntVar()
        pcbc = tkinter.IntVar()
        pci = tkinter.IntVar()
        pcmf = tkinter.IntVar()
        pcfd = tkinter.IntVar()
        pcbs = tkinter.IntVar()
        pc = tkinter.IntVar()
        npcbc = tkinter.IntVar()
        npcfd = tkinter.IntVar()
        npcbs = tkinter.IntVar()
        npc = tkinter.IntVar()
        ecm = tkinter.IntVar()

        # combo_d = tkinter.IntVar()
        # combo_d.set(2)

        def start():
            global drones
            drones = 0
            drones = (int(self.combo_drones.get()))
            module_logger.info((str(drones)) + ' drones set')
            print('drones is ', drones)
            main.miner()

        self.t = tkinter.Label(self, text="title here")
        self.t.grid(column=0, row=0, columnspan=2, sticky='W', padx=15)

        self.start = tkinter.Button(self, text="Start", command=start)
        self.start.grid(column=0, row=1, sticky='W')
        self.start.config(width='13', height='1')

        self.stop = tkinter.Button(self, text="Stop")
        self.stop.grid(column=1, row=1, columnspan=1, sticky='W')
        self.stop.config(width='13', height='1')

        self.end = tkinter.Button(self, text="End Run")
        self.end.grid(column=1, row=2, columnspan=1, sticky='W')
        self.end.config(width='13', height='1')

        self.combo_m = ttk.Combobox(self, values=[1, 2, 3, 4])
        self.combo_m.current(1)
        self.combo_m.grid(column=1, row=3, columnspan=1, sticky='W')
        self.combo_m.config(width='4', height='5')
        self.m = tkinter.Label(self, text="mc")
        self.m.grid(column=0, row=3, columnspan=1, sticky='W', padx=5)

        self.combo_drones = ttk.Combobox(self, values=[1, 2, 3, 4, 5])
        self.combo_drones.current(1)
        self.combo_drones.grid(column=1, row=4, columnspan=1, sticky='W')
        self.combo_drones.config(width='4', height='5')
        self.label_drones = tkinter.Label(self, text="drones")
        self.label_drones.grid(column=0, row=4, columnspan=1, sticky='W',
                               padx=5)

        self.check_pc = tkinter.Checkbutton(self, text='pc check', variable=pc)
        self.check_pc.grid(column=0, row=5, columnspan=1, sticky='W')
        self.check_pc = tkinter.Checkbutton(self, text='pc frig/des check',
                                            variable=pcfd)
        self.check_pc.grid(column=1, row=5, columnspan=1, sticky='W')
        self.check_pc = tkinter.Checkbutton(self, text='pc cru/bc check',
                                            variable=pcbc)
        self.check_pc.grid(column=0, row=6, columnspan=1, sticky='W')
        self.check_pc = tkinter.Checkbutton(self, text='pc bs check',
                                            variable=pcbs)
        self.check_pc.grid(column=1, row=6, columnspan=1, sticky='W')
        self.check_pc = tkinter.Checkbutton(self, text='pc min frig check',
                                            variable=pcmf)
        self.check_pc.grid(column=0, row=7, columnspan=1, sticky='W')
        self.check_pc = tkinter.Checkbutton(self, text='pc indy check',
                                            variable=pci)
        self.check_pc.grid(column=1, row=7, columnspan=1, sticky='W')

        self.check_pc = tkinter.Checkbutton(self, text='npc check',
                                            variable=npc)
        self.check_pc.grid(column=0, row=8, columnspan=1, sticky='W')
        self.check_pc = tkinter.Checkbutton(self, text='npc frig/des check',
                                            variable=npcfd)
        self.check_pc.grid(column=1, row=8, columnspan=1, sticky='W')
        self.check_pc = tkinter.Checkbutton(self, text='npc cru/bc check',
                                            variable=npcbc)
        self.check_pc.grid(column=0, row=9, columnspan=1, sticky='W')
        self.check_pc = tkinter.Checkbutton(self, text='npc bs check',
                                            variable=npcbs)
        self.check_pc.grid(column=1, row=9, columnspan=1, sticky='W')

        self.check_pc = tkinter.Checkbutton(self, text='ecm check',
                                            variable=ecm)
        self.check_pc.grid(column=0, row=10, columnspan=1, sticky='W')

        self.mytext = ScrolledText.ScrolledText(self, state="disabled")
        self.mytext.grid(column=0, row=99, columnspan=99)
        self.mytext.grid_columnconfigure(0, weight=1)
        self.mytext.grid_rowconfigure(0, weight=1)
        self.mytext.config(width='40', height='8')

        self.mybutton = tkinter.Button(self, text="ClickMe")
        self.mybutton.grid(column=0, row=2, sticky='W')
        self.mybutton.bind("<ButtonRelease-1>", self.button_callback)
        self.mybutton.config(width='13', height='1')

    def button_callback(self, event):
        now = datetime.datetime.now()
        module_logger.info(now)


class MyHandlerText(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self) # initialize parent
        self.textctrl = textctrl

    def emit(self, record):
        msg = self.format(record)
        self.textctrl.config(state="normal")
        self.textctrl.insert(tkinter.END, msg + "\n")
        self.flush()
        self.textctrl.config(state="disabled")
        self.textctrl.yview(tkinter.END)


if __name__ == "__main__":
    # create Tk object instance
    app = simpleapp_tk(None)
    app.title('my application')

    # setup logging handlers using the Tk instance created above
    # the pattern below can be used in other threads...
    # ...to allow other thread to send msgs to the gui
    # in this example, we set up two handlers just for demonstration (you could add a fileHandler, etc)
    stderrHandler = logging.StreamHandler()  # no arguments => stderr
    module_logger.addHandler(stderrHandler)
    guiHandler = MyHandlerText(app.mytext)
    module_logger.addHandler(guiHandler)
    module_logger.setLevel(logging.INFO)
    module_logger.info("from main")

    # start Tk
    app.mainloop()
    
'''
from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as ScrolledText
import tkinter as tk
import logging

window = Tk()
window.title("NEOBOT")
miner_modules = IntVar()

# Set number of miner modules (miner script only)
rad1 = Radiobutton(window, text='1', value=1, variable=miner_modules)
rad2 = Radiobutton(window, text='2', value=2, variable=miner_modules)
rad3 = Radiobutton(window, text='3', value=3, variable=miner_modules)
rad4 = Radiobutton(window, text='4', value=4, variable=miner_modules)
rad1.grid(column=1, row=1)
rad2.grid(column=2, row=1)
rad3.grid(column=3, row=1)
rad4.grid(column=4, row=1)

# Script selection
script = Combobox(window)
script['values'] = ("Miner", "Autopilot", "Collector")
script.current(0)  # set the default selected item
script.grid(column=0, row=0)


class TextHandler(logging.Handler):
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


class myGUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build_gui()

    def build_gui(self):
        # Build GUI
        self.root.title('TEST')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew')
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure(2, weight=1, uniform='a')
        self.grid_columnconfigure(3, weight=1, uniform='a')

        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self, state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(column=0, row=1, sticky='w', columnspan=3)

        # Create textLogger
        text_handler = TextHandler(st)

        # Logging configuration
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)


def start():
    if script.get() == "Miner":
        logging.info('selected ' + script.get())

        logging.info((str(miner_modules.get())) + ' mining module(s)')
        script_var = script.get()
        modules_var = miner_modules.get()

    elif script.get() == "Autopilot":
        logging.info('selected ' + script.get())
        script_var = script.get()

    elif script.get() == "Collector":
        logging.info('selected ' + script.get())
        script_var = script.get()


def main():
    root = tk.Tk()
    myGUI(root)

    btn = Button(window, text="Start", command=start)
    btn.grid(column=2, row=3)

    root.mainloop()


main()

"""
OLD GUI BASED ON PYGUBU

import traceback
import sys
import os
import threading

import tkinter as tk  # for python 3
import pygubu

from lib import main


class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('gui.ui')
        self.mainwindow = builder.get_object('main_window', master)
        builder.connect_callbacks(self)

    def start_button_click(self):
        threading.Thread(main.collector())

    def stop_button_click(self):
        raise SystemExit

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
"""



# GUI WITH BUTTONS IN SAME WINDOW


import logging
import tkinter
import datetime
import tkinter.scrolledtext as ScrolledText

# (but you can also reference this getLogger instance from other modules and other threads by passing the same argument name...allowing you to share and isolate loggers as desired)
# ...so it is module-level logging and it takes the name of this module (by using __name__)
# recommended per https://docs.python.org/2/library/logging.html
module_logger = logging.getLogger(__name__)

class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent

        self.grid()

        self.start = tkinter.Button(self, text="Start")
        self.start.grid(column=1,row=0,sticky='W')

        self.stop = tkinter.Button(self, text="Stop")
        self.stop.grid(column=2,row=0,sticky='W')

        self.radio1 = tkinter.Radiobutton(self, text="radio")
        self.radio1.grid(column=1,row=2,sticky='S')

        self.mybutton = tkinter.Button(self, text="ClickMe")
        self.mybutton.grid(column=0,row=0,sticky='EW')
        self.mybutton.bind("<ButtonRelease-1>", self.button_callback)

        self.mytext = ScrolledText.ScrolledText(self, state="disabled")
        self.mytext.grid(column=2, row=2,sticky='SE')
        self.mytext.config(width='50', height='10')

    def button_callback(self, event):
        now = datetime.datetime.now()
        module_logger.info(now)

class MyHandlerText(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self) # initialize parent
        self.textctrl = textctrl

    def emit(self, record):
        msg = self.format(record)
        self.textctrl.config(state="normal")
        self.textctrl.insert(tkinter.END, msg + "\n")
        self.flush()
        self.textctrl.config(state="disabled")
        self.textctrl.yview(tkinter.END)

if __name__ == "__main__":

    # create Tk object instance
    app = simpleapp_tk(None)
    app.title('my application')

    # setup logging handlers using the Tk instance created above
    # the pattern below can be used in other threads...
    # ...to allow other thread to send msgs to the gui
    # in this example, we set up two handlers just for demonstration (you could add a fileHandler, etc)
    stderrHandler = logging.StreamHandler()  # no arguments => stderr
    module_logger.addHandler(stderrHandler)
    guiHandler = MyHandlerText(app.mytext)
    module_logger.addHandler(guiHandler)
    module_logger.setLevel(logging.INFO)
    module_logger.info("from main")    

    # start Tk
    app.mainloop()
   
   import logging
import tkinter
import datetime
import tkinter.scrolledtext as ScrolledText
from tkinter import ttk

# (but you can also reference this getLogger instance from other modules and other threads by passing the same argument name...allowing you to share and isolate loggers as desired)
# ...so it is module-level logging and it takes the name of this module (by using __name__)
# recommended per https://docs.python.org/2/library/logging.html
module_logger = logging.getLogger(__name__)

class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent

        self.grid()

        m = tkinter.IntVar()
        m.set(2)
        d = tkinter.IntVar()
        d.set(2)

        def start():
          print(m.get())
          print(d.get())

        self.start = tkinter.Button(self, text="Start", command=start)
        self.start.grid(column=0,row=0,sticky='W')

        self.stop = tkinter.Button(self, text="Stop")
        self.stop.grid(column=0, row=1, columnspan=1, sticky='W')

        self.radio_m1 = tkinter.Radiobutton(self, text='1', value=1, variable=m)
        self.radio_m1.grid(column=0, row=2, columnspan=1, sticky='W')

        self.radio_m2 = tkinter.Radiobutton(self, text='2', value=2, variable=m)
        self.radio_m2.grid(column=1, row=2, columnspan=1, sticky='W')
        #self.radio_m2.current(2)

        self.radio_m3 = tkinter.Radiobutton(self, text='3', value=3, variable=m)
        self.radio_m3.grid(column=2, row=2, columnspan=1, sticky='W')

        self.radio_m4 = tkinter.Radiobutton(self, text='4', value=4, variable=m)
        self.radio_m4.grid(column=3, row=2, columnspan=1, sticky='W')

        self.mybutton = tkinter.Button(self, text="ClickMe")
        self.mybutton.grid(column=0,row=4,sticky='W')
        self.mybutton.bind("<ButtonRelease-1>", self.button_callback)

        self.combo_d = ttk.Combobox(self, values=[1,2,3,4], variable=d)
        self.combo_d.current(1)
        self.combo_d.grid(column=0, row=3, columnspan=1, sticky='W')
        self.combo_d.config(width='4', height='1')

        self.mytext = ScrolledText.ScrolledText(self, state="disabled")
        self.mytext.grid(column=0, row=99, columnspan=99)
        self.mytext.grid_columnconfigure(0, weight=1)
        self.mytext.grid_rowconfigure(0, weight=1)
        self.mytext.config(width='50', height='8')

    def button_callback(self, event):
        now = datetime.datetime.now()
        module_logger.info(now)

class MyHandlerText(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self) # initialize parent
        self.textctrl = textctrl

    def emit(self, record):
        msg = self.format(record)
        self.textctrl.config(state="normal")
        self.textctrl.insert(tkinter.END, msg + "\n")
        self.flush()
        self.textctrl.config(state="disabled")
        self.textctrl.yview(tkinter.END)

if __name__ == "__main__":

    # create Tk object instance
    app = simpleapp_tk(None)
    app.title('my application')

    # setup logging handlers using the Tk instance created above
    # the pattern below can be used in other threads...
    # ...to allow other thread to send msgs to the gui
    # in this example, we set up two handlers just for demonstration (you could add a fileHandler, etc)
    stderrHandler = logging.StreamHandler()  # no arguments => stderr
    module_logger.addHandler(stderrHandler)
    guiHandler = MyHandlerText(app.mytext)
    module_logger.addHandler(guiHandler)
    module_logger.setLevel(logging.INFO)
    module_logger.info("from main")    

    # start Tk
    app.mainloop()
'''
