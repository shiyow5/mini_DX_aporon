#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog

class Main_Win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="center")
        
        master.geometry("570x300")
        master.title("生産スケジューリング")
        
        self.button_file = tk.Button(master, command=self.scheduling_window, text="スケジューリング", width=20)
        self.button_file.place(x=285, y=30, anchor="center")
        
        self.button_search = tk.Button(master, command=self.calc_window, text="統計計算", width=20)
        self.button_search.place(x=285, y=70, anchor="center")
        
    def scheduling_window(self):
        self.newWindow1 = tk.Toplevel(self.master)
        self.subapp_1 = Scheduling_Win(self.newWindow1)
        self.subapp_1.button_1["command"] = self.subapp_1_functions[0]
        self.subapp_1.button_2["command"] = self.subapp_1_functions[1]
        self.subapp_1.button_3["command"] = self.subapp_1_functions[2]
        #self.subapp_1.button_4["command"] = self.subapp_1_functions[3]
        
    def calc_window(self):
        self.newWindow2 = tk.Toplevel(self.master)
        self.subapp_2 = Calc_Win(self.newWindow2)
        #self.subapp_2.button_1["command"] = self.subapp_2_functions[0]
        #self.subapp_2.button_2["command"] = self.subapp_2_functions[1]
        #self.subapp_2.button_3["command"] = self.subapp_2_functions[2]
        #self.subapp_2.button_4["command"] = self.subapp_2_functions[3]
        #self.subapp_2.button_5["command"] = self.subapp_2_functions[4]
        
    def set_winController(self, winName:str, functions:list):
        if (winName == 'scheduling_window'):
            self.subapp_1_functions = functions
        elif (winName == 'calc_window'):
            self.subapp_2_functions = functions
            
            
class Scheduling_Win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="center")
        
        master.geometry("600x600")
        master.title("スケジューリング")
        
        self.label_1 = tk.Label(master, text='納期についてのExcelファイル', font = ('Times New Roman',15))
        self.label_1.place(x=20, y=30)
        self.button_1 = tk.Button(master, text='選択', width=10)
        self.button_1.place(x=70, y=70)
        self.error_1 = tk.Label(master, text='未選択です', font=('Times New Roman',15), foreground = '#999999')
        self.error_1.place(x=200, y=70)
        self.data1_path = ""
        
        self.label_2 = tk.Label(master, text='製品名-工程名対応表についてのExcelファイル', font = ('Times New Roman',15))
        self.label_2.place(x=20, y=140)
        self.button_2 = tk.Button(master, text='選択', width=10)
        self.button_2.place(x=70, y=180)
        self.error_2 = tk.Label(master, text='未選択です', font=('Times New Roman',15), foreground = '#999999')
        self.error_2.place(x=200, y=180)
        self.data2_path = ""
        
        self.label_3 = tk.Label(master, text='1人あたりの日産数についてのExcelファイル', font = ('Times New Roman',15))
        self.label_3.place(x=20, y=250)
        self.button_3 = tk.Button(master, text='選択', width=10)
        self.button_3.place(x=70, y=290)
        self.error_3 = tk.Label(master, text='未選択です', font=('Times New Roman',15), foreground = '#999999')
        self.error_3.place(x=200, y=290)
        self.data3_path = ""
        
        self.button_4 = tk.Button(master, text='スケジューリング実行', width=20, height=4)
        self.button_4.place(x=350, y=400)
        self.error_4 = tk.Label(master, text='エラー特になし', font=('Times New Roman',15), foreground = '#999999')
        self.error_4.place(x=20, y=500)
        
    def file_dialog(self, label_name):
        fTyp = [("", "*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_name = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if len(file_name) != 0:
            if label_name == 'error_1':
                self.data1_path = file_name
                self.error_1['text'] = file_name
            elif label_name == 'error_2':
                self.data2_path = file_name
                self.error_2['text'] = file_name
            elif label_name == 'error_3':
                self.data3_path = file_name
                self.error_3['text'] = file_name


class Calc_Win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="center")
        
        self.result_num = 10
        self.cursol = 0
        self.files = []
        
        master.geometry("1140x700")
        master.title("統計計算")
        
        self.label_1 = tk.Label(master, text="file select: ", font = ('Times New Roman',20))
        self.label_1.place(x=20, y=30)
        
        self.file_name = tk.StringVar()
        self.entry_file = tk.Entry(master, textvariable=self.file_name, font = ('Times New Roman',20), width = 10)
        self.entry_file.place(x=150, y=30)
        
        self.button_1 = tk.Button(master, text = 'Add', width = 10)
        self.button_1.place(x=300, y=32)
        
        self.file_error = tk.Label(master, font=('Times New Roman',15), foreground = '#999999')
        self.file_error.place(x=160, y=70)
        self.file_selected = tk.Label(master, font=('Times New Roman',15), foreground = '#999999')
        self.file_selected.place(x=160, y=90)
        
        self.label_2 = tk.Label(master, text="search type: ", font = ('Times New Roman',20))
        self.label_2.place(x=500, y=30)
        
        self.search_type = tk.StringVar()
        self.entry_type = tk.Entry(master, textvariable=self.search_type, font = ('Times New Roman',20), width = 10)
        self.entry_type.place(x=650, y=30)
        
        self.button_2 = tk.Button(master, text = 'OK', width = 10)
        self.button_2.place(x=800, y=32)
        
        self.type_error = tk.Label(master, font=('Times New Roman',15), foreground = '#999999')
        self.type_error.place(x=650, y=70)
        self.type_selected = tk.Label(master, font=('Times New Roman',15), foreground = '#999999')
        self.type_selected.place(x=650, y=90)
        
        self.label_3 = tk.Label(master, text="search word: ", font = ('Times New Roman',20))
        self.label_3.place(x=20, y=130)
        
        self.word = tk.StringVar()
        self.entry_search = tk.Entry(master, textvariable=self.word, font = ('Times New Roman',20), width = 33)
        self.entry_search.place(x=200, y=130)
        
        self.button_3 = tk.Button(master, text = 'OK', width = 10)
        self.button_3.place(x=680, y=132)
        
        self.results_c = [tk.Label(master, font=('Times New Roman',20), foreground = '#1155ee', width=10, anchor="center") for i in range(self.result_num)] # relief=tk.SOLID
        for i, result_c in enumerate(self.results_c):
            result_c.place(x=550, y=200+i*40, anchor="center")
            
        self.results_l = [tk.Label(master, font=('Times New Roman',20), width=30, anchor="e") for i in range(self.result_num)]
        for i, result_l in enumerate(self.results_l):
            result_l.place(x=450, y=200+i*40, anchor="e")
            
        self.results_r = [tk.Label(master, font=('Times New Roman',20), width=30, anchor="w") for i in range(self.result_num)]
        for i, result_r in enumerate(self.results_r):
            result_r.place(x=650, y=200+i*40, anchor="w")
            
        self.button_4 = tk.Button(master, text = 'Next', width = 10)
        self.button_4.place(x=550, y=650, anchor="center")
        
        self.button_5 = tk.Button(master, text = 'Clear', width = 10, height=3)
        self.button_5.place(x=1000, y=650, anchor="center")

    
def main():
    # View
    win = tk.Tk()
    app = Main_Win(master = win)
    
    # Controller(File Controll)
    set_data1 = lambda : app.subapp_1.file_dialog('error_1')
    set_data2 = lambda : app.subapp_1.file_dialog('error_2')
    set_data3 = lambda : app.subapp_1.file_dialog('error_3')
    app.set_winController(winName='scheduling_window', functions=[set_data1, set_data2, set_data3])
    
    # Controller(Search Window)
        
    #app.set_winController()
    
    
    app.mainloop()
    
if __name__ == "__main__":
    main()