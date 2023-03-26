
#TODO Implement as a library and class
import requests
from pytube import YouTube
from tkinter import *
from tkinter import ttk

# Get the URL of the video clip
# video_url = input("Enter the URL of the video clip: ")

# Download the video file using requests
# response = requests.get(video_url)
# video_file = response.content

# Extract the video's metadata using pytube

def format_select(*args):
    print(format.get())
    print("format")

def url_entry_written(*args):
    print(enterUrlVar.get())

def download_progress():
    print("download progress")

def download():
    yt = YouTube(enterUrlVar.get(), download_progress)
    video_title = yt.title
    stream = yt.streams.filter(progressive=True, file_extension=format.get()).order_by('resolution').desc().first()
    print(f"Downloading '{video_title}'...")
    stream.download(output_path='downloads/')
    print("Download complete!")

root = Tk()
root.title("DSDownloader")
# root.geometry("700x400")

mainFrameStyle = ttk.Style()
mainFrameStyle.configure('redStyle.TFrame', background='red', borderwidth=5, relief='raised')

mainFrame = ttk.Frame(root, style='redStyle.TFrame', padding='30 30 30 30')
mainFrame.grid(column=0, row=0)

label = ttk.Label(mainFrame, text="YOU TUBE DOWNLOADER")
label.grid(row=0, column=0)

enterUrlVar = StringVar()
enterUrlVar.set("Type url here: ")
urlEntry = ttk.Entry(mainFrame, textvariable=enterUrlVar, width=31)
enterUrlVar.trace_add("write",url_entry_written)

urlEntry.grid(row=1, column=0)

formatLabel = ttk.Label(mainFrame, text="Format")
formatLabel.grid(row=2, column=0)

format = StringVar()
format.set('mp4')
formatBox = ttk.Combobox(mainFrame,textvariable=format, width=30, height=10)
formatBox.grid(row=4,column=0)
formatBox['values'] = ('mp3', 'mp4')
formatBox.state(["readonly"])
formatBox.bind('<<ComboboxSelected>>', format_select)

# bkgImage = PhotoImage(file="resources/youtube-transparent-youtube-icon-29.png")
# imageLabel = ttk.Label(mainFrame, image=bkgImage)
# imageLabel.pack()

#
downloadBtn = ttk.Button(mainFrame, text="Download", command=download)
downloadBtn.grid(row=1,column=1)

root.mainloop()
