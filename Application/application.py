#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

class Main_Win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="center")
        
        master.geometry("570x300")
        master.title("生産スケジューリング")
        
        self.button_file = tk.Button(master, command=self.scheduling_window, text="スケジューリング", width=30, height=3)
        self.button_file.place(x=285, y=100, anchor="center")
        
        self.button_search = tk.Button(master, command=self.calc_window, text="統計計算", width=30, height=3)
        self.button_search.place(x=285, y=200, anchor="center")
        
    def scheduling_window(self):
        self.newWindow1 = tk.Toplevel(self.master)
        self.subapp_1 = Scheduling_Win(self.newWindow1)
        self.subapp_1.button_1["command"] = self.subapp_1_functions[0]
        self.subapp_1.button_2["command"] = self.subapp_1_functions[1]
        self.subapp_1.button_3["command"] = self.subapp_1_functions[2]
        self.subapp_1.button_4["command"] = self.subapp_1_functions[3]
        
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
        self.save_path = ""
        
    def file_dialog(self, label_name: str):
        fTyp = [("Excel", ".xlsx")]
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
                
    def file_save(self, save_data: pd.DataFrame):
        file_name = filedialog.asksaveasfilename(
            title = "名前を付けて保存",
            filetypes = [("Excel", ".xlsx")], # ファイルフィルタ
            initialdir = "./", # 自分自身のディレクトリ
            defaultextension = ".xlsx"
            )
        if len(file_name) != 0:
            self.save_path = file_name
            self.error_4['text'] = file_name
            
        save_data.to_excel(file_name, sheet_name="sheet1")


class Calc_Win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="center")
        
        self.result_num = 10
        self.cursol = 0
        self.files = []
        
        master.geometry("1140x700")
        master.title("統計計算")

    
def main():
    # View
    win = tk.Tk()
    app = Main_Win(master = win)
    
    # Controller(File Controll)
    set_data1 = lambda : app.subapp_1.file_dialog('error_1')
    set_data2 = lambda : app.subapp_1.file_dialog('error_2')
    set_data3 = lambda : app.subapp_1.file_dialog('error_3')
    def save_file():
        df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]],
                  index=['one', 'two', 'three'], columns=['a', 'b', 'c'])
        app.subapp_1.file_save(df)
        
    app.set_winController(winName='scheduling_window', functions=[set_data1, set_data2, set_data3, save_file])
    
    # Controller(Search Window)
        
    #app.set_winController()
    
    
    app.mainloop()
    
if __name__ == "__main__":
    main()