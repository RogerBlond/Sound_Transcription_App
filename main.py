""" 
    -==Created by RogerBlond==-

    NAME
	    SoundTranscriptApp.py
    DESC
        pl language need to use http reqeusts to server through recognize_google method
        other languages can use streaming via IBM Cloud Api (its much faster)
    REQUIREMENTS
        stereo mix enabled on audio card and chosen from device's list,
    MODYFIED   (DD/MM/YYYY)
		rfbom   19/10/2022 - created
"""
#https://stackoverflow.com/questions/4122188/how-can-i-invoke-a-thread-multiple-times-in-python
import speech_recognition as sr
import threading
import concurrent.futures
import tkinter as tk
from tkinter import *

#global
event_obj = threading.Event()
r = sr.Recognizer()
r.pause_threshold = 0.5
text =""
running = True


#Functions
def start_thread():
   
   with concurrent.futures.ThreadPoolExecutor() as excecuter:
        thread_list = excecuter.submit(start)


def start():
  event_obj.clear()
  global running 
  running = True

  mic = sr.Microphone(device_index=1)  # stereo mix as default
  while running:
      with mic as source, open("outputs.txt","a+", encoding="utf-8") as f:
        
          audio = r.listen(source, phrase_time_limit=5)

          try:
            global text
            text = r.recognize_google(audio, language="pl-PL").lower()
            print(text)
            display.config(text=text)
            f.write(text + "\n")
            f.close() 
          except Exception as e:
            print(e)
            print("Sorry... can't hear anything")
  return text
  
def stop():
  global running
  event_obj.set()

  if event_obj.is_set():
    running = False
  else:
    print('No recording')


#GUI
def gui():
  global display
  root = tk.Tk()
  root.title('SoundTranscriptionApp')
  root.geometry("450x150")

  Toplabel=Label(root,text=' Click start button to transcript listening speech from your speakers ',fg='#263D42')
  Toplabel.pack()

  canvas = tk.Canvas(root, height=150, width=450, bg="#263D42")
  canvas.pack()
  frame = tk.Frame(root, bg='white')
  frame.pack(side="bottom", fill="x", expand=False)

  StartButton=tk.Button(frame, text='START', bg='#263D42',fg='white', command=lambda: threading.Thread(target=start_thread).start())
  StopButton=tk.Button(frame, text='STOP', bg='#263D42',fg='white', command=stop)
  ExitButton=tk.Button(frame, text='EXIT', bg='#263D42',fg='white', command=root.destroy)

  frame.grid_columnconfigure(0, weight=1)
  StartButton.grid(row=0, column=1, sticky="ew")
  StopButton.grid(row=0, column=2, sticky="ew")
  ExitButton.grid(row=1, column=2, sticky="ew")

  scroll_bar = Scrollbar(root)
  scroll_bar.pack(side = RIGHT, fill = Y)
  
  
  display=Label(canvas,text='',fg='blue', wraplength=400)
  display.pack()

  root.mainloop()



if __name__ == '__main__':
  gui()
