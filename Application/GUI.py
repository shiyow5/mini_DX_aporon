#!/usr/bin/env python3

import tkinter as tk

class Main_Win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="center")
        
        master.geometry("570x300")
        master.title("生産スケジューリング")
        
        self.button_file = tk.Button(master, command=self.file_window, text="スケジューリング", width=20)
        self.button_file.place(x=285, y=30, anchor="center")
        
        self.button_search = tk.Button(master, command=self.search_window, text="統計計算", width=20)
        self.button_search.place(x=285, y=70, anchor="center")
        
    def file_window(self):
        self.newWindow1 = tk.Toplevel(self.master)
        self.subapp_1 = File_Win(self.newWindow1)
        self.subapp_1.button_1["command"] = self.subapp_1_functions[0]
        self.subapp_1.button_2["command"] = self.subapp_1_functions[1]
        self.subapp_1.button_3["command"] = self.subapp_1_functions[2]
        self.subapp_1.button_4["command"] = self.subapp_1_functions[3]
        
    def search_window(self):
        self.newWindow2 = tk.Toplevel(self.master)
        self.subapp_2 = Search_Win(self.newWindow2)
        self.subapp_2.button_1["command"] = self.subapp_2_functions[0]
        self.subapp_2.button_2["command"] = self.subapp_2_functions[1]
        self.subapp_2.button_3["command"] = self.subapp_2_functions[2]
        self.subapp_2.button_4["command"] = self.subapp_2_functions[3]
        self.subapp_2.button_5["command"] = self.subapp_2_functions[4]
        
    def set_winController(self, winName:str, functions:list):
        if (winName == 'file_window'):
            self.subapp_1_functions = functions
        elif (winName == 'search_window'):
            self.subapp_2_functions = functions
            
            
class File_Win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="center")
        
        master.geometry("600x600")
        master.title("File Controll")
        
        self.label_1 = tk.Label(master, text='file name: ', font = ('Times New Roman',15))
        self.label_1.place(x=20, y=30)
        
        self.file_name = tk.StringVar()
        self.entry_file = tk.Entry(master, textvariable=self.file_name, font = ('Times New Roman',15), width = 20)
        self.entry_file.place(x=120, y=30)
        
        self.label_2 = tk.Label(master, text='new name: ', font = ('Times New Roman',15))
        self.label_2.place(x=350, y=30)
        
        self.new_name = tk.StringVar()
        self.entry_new = tk.Entry(master, textvariable=self.new_name, font = ('Times New Roman',15), width = 10)
        self.entry_new.place(x=450, y=30)
        
        self.button_1 = tk.Button(master, text='Upload', width=10)
        self.button_1.place(x=50, y=100)
        self.upload_error = tk.Label(master, font=('Times New Roman',15), foreground = '#999999')
        self.upload_error.place(x=200, y=100)
        
        self.button_2 = tk.Button(master, text='Search', width=10)
        self.button_2.place(x=50, y=200)
        self.search_error = tk.Label(master, font=('Times New Roman',15), foreground = '#999999')
        self.search_error.place(x=200, y=200)
        self.search_result = tk.Label(master, font=('Times New Roman',15), foreground = '#999999', justify="left")
        self.search_result.place(x=70, y=235)
        
        self.button_3 = tk.Button(master, text='Update', width=10)
        self.button_3.place(x=50, y=300)
        self.update_error = tk.Label(master, font=('Times New Roman',15), foreground = '#999999')
        self.update_error.place(x=200, y=300)
        
        self.button_4 = tk.Button(master, text='Delete', width=10)
        self.button_4.place(x=50, y=400)
        self.delete_error = tk.Label(master, font=('Times New Roman',15), foreground = '#999999')
        self.delete_error.place(x=200, y=400)
        
        self.label_3 = tk.Label(master, text="file status", font = ('Times New Roman',15), foreground = '#999999')
        self.label_3.place(x=20, y=500)
        self.label_4 = tk.Label(master, font = ('Times New Roman',17), foreground = '#999999')
        self.label_4.place(x=40, y=530)
        
        #self.set_file_status(File.get_fileName())
        
        
    def set_upload_error(self, status:bool):
        if (status):
            self.upload_error["text"] = "Success."
        else:
            self.upload_error["text"] = "No such text-file."
            
    def set_search_error(self, result):
        if (result):
            self.search_error["text"] = "Success."
            result = list(result)
            result[2] = '\n' + result[2][:50].replace('\n', ' ') + '...'
            self.search_result["text"] = ', '.join(result)
        else:
            self.search_error["text"] = "No such file."
            self.search_result["text"] = ""
            
    def set_update_error(self):
        self.update_error["text"] = "Tried to update"
        
    def set_delete_error(self):
        self.delete_error["text"] = "Tried to delete" 
        
    def set_file_status(self, files:list):
        self.label_4["text"] = ', '.join(files)
        
    def clear(self):
        self.upload_error["text"] = ""
        self.search_error["text"] = ""
        self.search_result["text"] = ""
        self.update_error["text"] = ""
        self.delete_error["text"] = ""


class Search_Win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="center")
        
        self.result_num = 10
        self.cursol = 0
        self.files = []
        
        master.geometry("1140x700")
        master.title("Search Window")
        
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
        
        
    def set_file(self, file:str):
        self.files.append(file)
        
    def set_LR_sentences(self, LR_sentences:list=None):
        self.LR_sentences = LR_sentences
    
    def move_cursol(self):
        self.cursol += self.result_num
        
    def reset_files(self):
        self.files = []
        
    def reset_cursol(self):
        self.cursol = 0
        
    def set_file_error(self, status:bool):
        if (status):
            self.file_error["text"] = "Success."
            self.file_selected["text"] = ', '.join(self.files)
        else:
            self.file_error["text"] = "'No such file.' OR 'Same file input.'"
            self.file_selected["text"] = ', '.join(self.files)
            
    def set_type_error(self, status:bool):
        if (status):
            self.type_error["text"] = "Success."
            self.type_selected["text"] = f"Selected type: {self.search_type.get()}"
        else:
            self.type_error["text"] = "This is not implemented."
            self.type_selected["text"] = "Selected type: 'None'"
        
    def set_result(self):
        for i, LR_sentence in enumerate(self.LR_sentences[self.cursol:self.cursol+self.result_num]):
            self.results_c[i]["text"] = self.word.get()
            self.results_l[i]["text"] = LR_sentence[0]
            self.results_r[i]["text"] = LR_sentence[1]
        
        return
        
    def clear(self):
        self.file_error["text"] = ""
        self.type_error["text"] = ""
        
        for results in [self.results_c, self.results_l, self.results_r]:
            for result in results:
                result["text"] = ""
                
        return

    
def main():
    # View
    win = tk.Tk()
    app = Main_Win(master = win)
    
    # Controller(File Controll)
    def upload_file():
        """app.subapp_1.clear()
        status = File.create_file(file_name=app.subapp_1.file_name.get(), new_name=app.subapp_1.new_name.get())
        app.subapp_1.set_upload_error(status=status)
        app.subapp_1.set_file_status(File.get_fileName())"""
        return
    
    def search_file():
        """app.subapp_1.clear()
        result = File.retrieve_file(file_name=app.subapp_1.file_name.get())
        app.subapp_1.set_search_error(result=result)"""
        return
    
    def update_file():
        """app.subapp_1.clear()
        File.update_file(file_name=app.subapp_1.file_name.get(), new_name=app.subapp_1.new_name.get())
        app.subapp_1.set_update_error()
        app.subapp_1.set_file_status(File.get_fileName())"""
        return
    
    def delete_file():
        """app.subapp_1.clear()
        File.delete_file(file_name=app.subapp_1.file_name.get())
        app.subapp_1.set_delete_error()
        app.subapp_1.set_file_status(File.get_fileName())"""
        return
    
    app.set_winController(winName='file_window', functions=[upload_file, search_file, update_file, delete_file])
    
    # Controller(Search Window)
    def select_file():
        """app.subapp_2.clear()
        file_name = app.subapp_2.file_name.get()
        if (File.retrieve_file(file_name) and file_name not in app.subapp_2.files):
            app.subapp_2.set_file(file=file_name)
            app.subapp_2.set_file_error(status=True)
        else:
            app.subapp_2.set_file_error(status=False)"""
        
        return
    
    def select_search_type():
        app.subapp_2.clear()
        search_type = app.subapp_2.search_type.get()
        if (search_type == "word-token"):
            app.subapp_2.set_type_error(status=True)
        else:
            app.subapp_2.set_type_error(status=False)
            
        return
    
    def search_word():
        """LR_sentences = NLP.search_word(word=app.subapp_2.word.get(), files=app.subapp_2.files, type=app.subapp_2.search_type.get())
        app.subapp_2.clear()
        app.subapp_2.reset_cursol()
        app.subapp_2.set_LR_sentences(LR_sentences)
        app.subapp_2.set_result()"""
        return
    
    def next_result():
        app.subapp_2.clear()
        app.subapp_2.move_cursol()
        app.subapp_2.set_result()
        return
    
    def clear_search():
        app.subapp_2.file_name.set("")
        app.subapp_2.search_type.set("")
        app.subapp_2.word.set("")
        app.subapp_2.clear()
        app.subapp_2.reset_cursol()
        app.subapp_2.reset_files()
        app.subapp_2.file_selected["text"] = ""
        app.subapp_2.type_selected["text"] = ""
        return
        
    app.set_winController(winName='search_window', functions=[select_file, select_search_type, search_word, next_result, clear_search])
    
    
    app.mainloop()
    
if __name__ == "__main__":
    main()