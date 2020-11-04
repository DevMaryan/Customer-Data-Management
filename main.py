from os import error
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import sqlite3
import csv
import os

mydata = []


# DB
mydb = sqlite3.connect('treemp.db')
cursor = mydb.cursor()

def update(rows):
    global mydata
    mydata = rows
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('','end', values = i, tags = 'unchecked')


def toggleCheck(event):
    rowid = trv.identify_row(event.y)
    tag = trv.item(rowid, "tags")[0]
    tags = list(trv.item(rowid, "tags"))
    tags.remove(tag)
    trv.item(rowid, tags = tags)
    if tag == 'checked':
        trv.item(rowid, tags = 'unchecked')
    else:
        trv.item(rowid, tags = 'checked')

def search():
    q2 = q.get()
    query = "SELECT id, first_name, last_name, age FROM customers WHERE first_name LIKE '%"+q2+"%' OR last_name LIKE '%"+q2+"%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)


def clear():
    query = "SELECT id, first_name, last_name, age FROM customers"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)


def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])

def update_customer():
    fname = t2.get()
    lname = t3.get()
    age = t4.get()
    custid = t1.get()

    if messagebox.askyesno('Confirm Please', 'Are you sure you want to update this customer?'):
        query = "UPDATE customers SET first_name = ?, last_name = ?, age = ? WHERE id = ?"
        cursor.execute(query, (fname, lname, age, custid))
        clear()
    else:
        return True

def add_new():
    fname = t2.get()
    lname = t3.get()
    age = t4.get()
    try:           
        query = "INSERT INTO customers(id, first_name, last_name, age) VALUES (NULL, ?, ?, ?)"
        cursor.execute(query, (fname, lname, age))
        mydb.commit()
        clear()
    except EOFError as e:
        print(e)

def delete_customer():
    customer_id = t1.get()
    if messagebox.askyesno('Confirm Delete?', 'Are you sure you want to delete this customer?'):
        try:              
            query = "DELETE FROM customers WHERE id = ?"
            cursor.execute(query,(customer_id,))
            mydb.commit()
            clear()
        except EOFError as e:
            print(e)

    else:
        return True

def export():
    if len(mydata) < 1:
        messagebox.showerror('No Data', 'No data avialable to export')
        return FALSE
    fln = filedialog.asksaveasfilename(initialdir = os.getcwd(), title = 'Save CSV', filetypes = (("CSV File", "*.csv"), ("All Files", "*.*")), defaultextension=True)
    with open(fln, mode = 'w') as myfile:
        exp_writer = csv.writer(myfile, lineterminator='\n')
        for i in mydata:
            exp_writer.writerow(i)
    messagebox.showinfo('Data Exported', 'Your data has been exported to ' + os.path.basename(fln)+ 'successfully')


def importcsv():
    mydata.clear()
    fln = filedialog.askopenfilename(initialdir = os.getcwd(), title = 'Open CSV', filetypes = (("CSV File", "*.csv"), ("All files", "*.*")), defaultextension=True)
    with open(fln) as myfile:
        csvread = csv.reader(myfile, delimiter = ',')
        for i in csvread:
            mydata.append(i)
    update(mydata)

def savedb():
    if messagebox.askyesno('Confirmation', 'Are you sure you want to save the data to Database?'):
        try:

            for i in mydata:
                uid = i[0]
                fname = i[1]
                lname = i[2]
                age = i[3]
                query = "INSERT INTO customers(id, first_name, last_name, age) VALUES (Null,?, ?, ?)"
                cursor.execute(query, (fname, lname, age))
            mydb.commit()
            clear()
            messagebox.showinfo('Data Saved', 'Data has been saved to database!')
        except EOFError as a:
            messagebox.showerror(a)
    else:
        return False



root = Tk()

q = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()


# Label Frames 
wrapper1 = LabelFrame(root, text = 'Customer List')
wrapper1.pack(fill = BOTH, expand = 'yes', padx = 20, pady = 10)
wrapper2 = LabelFrame(root, text = 'Search')
wrapper2.pack(fill = BOTH, expand = 'yes', padx = 20, pady = 10)
wrapper3 = LabelFrame(root, text = 'Customer Data')
wrapper3.pack(fill = BOTH, expand = 'yes', padx = 20, pady = 10)



trv = ttk.Treeview(wrapper1, columns = (1,2,3,4))
trv = ttk.Treeview(wrapper1, columns = (1,2,3,4), show = 'headings', height = 6)
style = ttk.Style(trv)
style.configure('Treeview', rowheight = 30)
trv.pack()


trv.heading('#0', text = '')
trv.heading('#1', text = 'Customer ID')
trv.heading('#2', text = 'First Name')
trv.heading('#3', text = 'Last Name')
trv.heading('#4', text = 'Age')


trv.bind('<Double 1>', getrow)

expbtn = Button(wrapper1, text = 'Export CSV', command = export)
expbtn.pack(side = tk.LEFT, padx = 10, pady = 10)

impbtn = Button(wrapper1, text = 'Import CSV', command = importcsv)
impbtn.pack(side = tk.LEFT, padx = 10, pady = 10)

savebtn = Button(wrapper1, text = 'Save Data', command = savedb)
savebtn.pack(side = tk.LEFT, padx = 10, pady = 10)

extbtn = Button(wrapper1, text = 'Exit', command = lambda: exit())
extbtn.pack(side = tk.LEFT, padx = 10, pady = 10)

query = "SELECT id, first_name, last_name, age FROM customers"
cursor.execute(query)
rows = cursor.fetchall()
update(rows)


# Search Section
lbl = Label(wrapper2, text = 'Search')
lbl.pack(side = tk.LEFT, padx = 10)
ent = Entry(wrapper2, textvariable = q)
ent.pack(side = tk.LEFT, padx = 6)

btn = Button(wrapper2, text = 'Search', command = search)
btn.pack(side = tk.LEFT, padx = 6)

cbtn = Button(wrapper2, text = 'Clear', command = clear)
cbtn.pack(side = tk.LEFT, padx = 6)


# User Data Section
lbl1 = Label(wrapper3, text = 'Customer ID')
lbl1.grid(row = 0, column = 0, padx = 5, pady = 3)
ent1 = Entry(wrapper3, textvariable = t1)
ent1.grid(row = 0, column = 1, padx = 5, pady = 3)

lbl2 = Label(wrapper3, text = 'First Name')
lbl2.grid(row = 1, column = 0, padx = 5, pady = 3)
ent2 = Entry(wrapper3, textvariable = t2)
ent2.grid(row = 1, column = 1, padx = 5, pady = 3)

lbl3 = Label(wrapper3, text = 'Last Name')
lbl3.grid(row =2, column = 0, padx = 5, pady = 3)
ent3 = Entry(wrapper3, textvariable = t3)
ent3.grid(row = 2, column = 1, padx = 5, pady = 3)

lbl4 = Label(wrapper3, text = 'Age')
lbl4.grid(row = 3, column = 0, padx = 5, pady = 3)
ent4 = Entry(wrapper3, textvariable = t4)
ent4.grid(row = 3, column = 1, padx = 5, pady = 3)

up_btn = Button(wrapper3, text = 'Update', command = update_customer)
up_btn.grid(row = 4, column = 1, padx = 5, pady = 3)
add_btn = Button(wrapper3, text = 'Add New', command = add_new)
add_btn.grid(row = 4, column = 0, padx = 5, pady = 3)
delete_btn = Button(wrapper3, text = 'Delete', command = delete_customer)
delete_btn.grid(row = 4, column = 2, padx = 5, pady = 3)




root.title('My Application')
root.geometry('800x700')
root.mainloop()