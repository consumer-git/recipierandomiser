import tkinter as tk
from PIL import ImageTk
import sqlite3 as lite
from numpy import random

bg_color='#3d6466'
# initiallize app

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    connection=lite.connect("./db/recipes.db")
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
    all_tables=cursor.fetchall()
    idx= random.randint(0,len(all_tables)-1)
    table_name= all_tables[idx][1]
    cursor.execute("SELECT * FROM "+table_name+";")
    table_records=cursor.fetchall()
    connection.close()
    return table_name, table_records

def pre_process(table_name,table_records):
    title= table_name[:-6]
    title="".join([char if char.islower() else " "+char for char in title ])
    #extracting the table records
    ingredients=[]
    for i in table_records:
        name=i[1]
        qty=i[2]
        unit=i[3]
        #writing in format '2 cups of sugar'
        ingredients.append("{} {} of {}".format(qty,unit,name))
    return title,ingredients



def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    logo_img = ImageTk.PhotoImage(file='assets/RRecipe_logo.png')
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(
            frame1,
            text='ready for your random recipie?',
            bg=bg_color,
            fg='white',
            font=("TkMenuFont", 14)
        ).pack()

    tk.Button(frame1, text='SHUFFLE', font=('TkHeadingFont', 20), bg='#28393a', fg='black', cursor='hand2',
        activebackground='#badee2', activeforeground='black', command=lambda: load_frame2()).pack(pady=20)



def load_frame2():
    #print('sup?')
    clear_widgets(frame1)
    frame1.tkraise()
    frame1.pack_propagate(False)
    table_name, table_records=fetch_db()
    title,ingredients= pre_process(table_name, table_records)

    #logo widget
    logo_img = ImageTk.PhotoImage(file='assets/RRecipe_logo_bottom.png')
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    #logo label
    tk.Label(
        frame2,
        text=title,
        bg=bg_color,
        fg='white',
        font=("TkHeadingFont", 20)
    ).pack(pady=25)

    for i in ingredients:
        tk.Label(
            frame2,
            text=i,
            bg=bg_color,
            fg='white',
            font=("TkMenuFont", 14)
        ).pack()
    tk.Button(frame2, text='BACK', font=('TkHeadingFont', 18), bg='#28393a', fg='black', cursor='hand2',
              activebackground='#badee2', activeforeground='black', command=lambda: load_frame1()).pack(pady=20)


root = tk.Tk()
root.title("Merrill's Recipie Picker" )
root.eval("tk::PlaceWindow . center")
frame1=tk.Frame(root, width=500, height=600, bg=bg_color)
frame2=tk.Frame(root,bg=bg_color)

frame1.grid(row=0, column=0)
frame2.grid(row=0, column=0)

load_frame1()

# run app
root.mainloop()