import os
import tkinter as tk
import tkinter.filedialog

class TkinterClass:
    def __init__(self):
        root = tk.Tk()
        root.geometry("500x350")

        button = tk.Button(root, text='ファイルダイアログを開く', font=('', 20),
                           width=24, height=1, bg='#999999', activebackground="#aaaaaa")
        button.bind('<ButtonPress>', self.file_dialog)
        button.pack(pady=40)

        self.file_name = tk.StringVar()
        self.file_name.set('未選択です')
        label = tk.Label(textvariable=self.file_name, font=('', 12))
        label.pack(pady=0)

        button = tk.Button(root, text='フォルダダイアログを開く', font=('', 20),
                           width=24, height=1, bg='#999999', activebackground="#aaaaaa")
        button.bind('<ButtonPress>', self.folder_dialog)
        button.pack(pady=40)

        self.folder_name = tk.StringVar()
        self.folder_name.set('未選択です')
        label = tk.Label(textvariable=self.folder_name, font=('', 12))
        label.pack(pady=10)

        root.mainloop()

    def file_dialog(self, event):
        fTyp = [("", "*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_name = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if len(file_name) == 0:
            self.file_name.set('選択をキャンセルしました')
        else:
            self.file_name.set(file_name)

    def folder_dialog(self, event):
        iDir = os.path.abspath(os.path.dirname(__file__))
        folder_name = tk.filedialog.askdirectory(initialdir=iDir)
        if len(folder_name) == 0:
            self.folder_name.set('選択をキャンセルしました')
        else:
            self.folder_name.set(folder_name)


if __name__ == '__main__':
    TkinterClass()
