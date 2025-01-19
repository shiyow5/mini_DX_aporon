from tkinter import filedialog

filename = filedialog.asksaveasfilename(
    title = "名前を付けて保存",
    filetypes = [("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif") ], # ファイルフィルタ
    initialdir = "./", # 自分自身のディレクトリ
    defaultextension = ".bmp"
    )
print(filename)