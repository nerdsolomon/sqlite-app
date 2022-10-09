from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
from datetime import datetime
import sqlite3
from PIL import Image
from io import *
from pandas import *

page = Tk()
page.title('SQLite App 2.0')
page.geometry('690x1160')
page['bg'] = 'white'

hos = sqlite3.connect('hospital.db')
c = hos.cursor()
date = datetime.now()
Datestring = date.strftime('Date : %d/%m/%y Time : %H:%M:%S')
columns = ('Name','Sex','Age','Address','Phone','Ref_Name','Ref_Address','Ref_Phone')
'''
c.execute("""CREATE TABLE hospital(
               Image blob,
               Name text,
               Sex text,
               Age text,
               Address text,
               Phone text,
               Ref_Name text,
               Ref_Address text,
               Ref_Phone text,
               Date_Time text
               )""")
'''
def submit():
    img = Image.open(image.get(),'r')
    imgByteArr = BytesIO()
    img.save(imgByteArr, format=img.format)
    imgByteArr = imgByteArr.getvalue()
    
    hos = sqlite3.connect('hospital.db')
    c = hos.cursor()
    c.execute("INSERT INTO hospital VALUES(:Image, :Name, :Sex, :Age, :Address, :Phone, :Ref_Name, :Ref_Address, :Ref_Phone, :Date_Time)", {
    'Image': imgByteArr,
    'Name': (name.get()).upper(),
    'Sex': sex.get(),
    'Age': age.get(),
    'Address': address.get(),
    'Phone': phone.get(),
    'Ref_Name': ref_name.get(),
    'Ref_Address': ref_address.get(),
    'Ref_Phone': ref_phone.get(),
    'Date_Time': Datestring
    })
    image.delete(0, END),name.delete(0, END),sex.delete(0, END),age.delete(0, END),address.delete(0, END),phone.delete(0, END),ref_name.delete(0, END),ref_address.delete(0, END),ref_phone.delete(0, END)
    hos.commit()
    hos.close()

def open():
	files = filedialog.askopenfilenames(initialdir='/storage/emulated/0/PhotoEditor/',title='Images',filetypes=(('PNG Files', '*.png'),))
	image.insert(END, files)
		
def query():
    hos = sqlite3.connect('hospital.db')
    c = hos.cursor()
    c.execute("SELECT oid, * FROM hospital")
    records = c.fetchall()
    rd = ''
    for record in records:
        rd = {'Name':[str(record[2]),], 'Sex':[str(record[3]),], 'Age':[str(record[4]),],'Address':[str(record[5]),], 'Phone':[str(record[6]),], 'Ref_Name':[str(record[7]),], 'Ref_Address':[str(record[8]),], 'Ref_Phone':[str(record[9]),], 'Date/Time':[str(record[10]),]}
        df = DataFrame(rd, columns=['Name','Sex','Age','Address','Phone','Ref_Name','Ref_Address','Ref_Phone','Date/Time'])
        output.insert(END, df)
    hos.commit()
    hos.close()
    
    frame1.grid_forget(),frame2.grid_forget(),frame3.grid_forget(),frame4.grid_forget(),frame5.grid(row=3,columnspan=4)

def search(): 
    hos = sqlite3.connect('hospital.db')
    c = hos.cursor()
    c.execute("SELECT oid, * FROM hospital WHERE oid=? OR Name=?", (search_entry.get(),(name_entry.get()).upper()))
    files = c.fetchall()
    x = ''
    b = ''
    for sx in files:
        x += '\nFile Number : '+str(sx[0])+'\n'+'\nName : '+str(sx[2])+'\nSex : '+str(sx[3])+'\nAge : '+str(sx[4])+'\nAddress : '+str(sx[5])+'\nPhone :'+str(sx[6])+'\n'+'\nRef. Name : '+str(sx[7])+'\nRef. Address : '+str(sx[8])+'\nRef. Phone : '+str(sx[9])+'\n'+'\n'+str(sx[10])
        output.insert(END, x)
        
        b = sx[1]
        out = Image.open(BytesIO(b)).save('pic.png')
        p = PhotoImage(file = '/storage/emulated/0/Android/obb/ru.iiec.pydroid3/pic.png')
        pic.config(image = p)
    hos.commit()
    hos.close()
    
    search_entry.delete(0,END), name_entry.delete(0,END)
    frame1.grid_forget(),frame2.grid_forget(),frame3.grid_forget(),frame4.grid_forget(),frame5.grid(row=3,columnspan=4)
         
def delete():
    hos = sqlite3.connect('hospital.db')
    c = hos.cursor()
    c.execute("DELETE FROM hospital WHERE oid=?", del_entry.get())
    hos.commit()
    hos.close()
    del_entry.delete(0,END)

def update():
    hos = sqlite3.connect('hospital.db')
    c = hos.cursor()
    c.execute(f"UPDATE hospital SET {column.get()}=? WHERE oid=?", (column_entry.get(),(update_entry.get()).upper()))
    hos.commit()
    hos.close()
    column.delete(0,END), column_entry.delete(0,END), update_entry.delete(0,END)
    
hos.commit()
hos.close()

def goto(page):
	if page == 'btn1':
		frame2.grid_forget(),frame3.grid_forget(),frame4.grid_forget(),frame1.grid(columnspan=4)
	elif page == 'btn2':
		frame1.grid_forget(),frame3.grid_forget(),frame4.grid_forget(),frame2.grid(columnspan=4)
	elif page == 'btn3':
		frame2.grid_forget(),frame1.grid_forget(),frame4.grid_forget(),frame3.grid(columnspan=4)
	elif page == 'btn4':
		frame2.grid_forget(),frame3.grid_forget(),frame1.grid_forget(),frame4.grid(columnspan=4)
	elif page == 'back':
		frame5.grid_forget(),frame1.grid(columnspan=4)
	elif page == 'num':
		name_entry.grid_forget(), nam_lab.grid_forget(), swh_num.grid_forget(), num_lab.grid(row=1,sticky='w',pady=10),search_entry.grid(row=2,ipady=50,ipadx=130,pady=10), swh_nam.grid(row=3,pady=10,sticky='e')
	elif page == 'nam':
		num_lab.grid_forget(), search_entry.grid_forget(), swh_nam.grid_forget(), nam_lab.grid(row=1,sticky='w',pady=10), name_entry.grid(row=2,ipady=50,ipadx=130,pady=10), swh_num.grid(row=3,pady=10,sticky='e')

date = Label(page, text= Datestring,bg='white',font=('arial',5)).grid(row=0, columnspan=4,sticky='e')
Label(page, text="PATIENT'S ADMISSION RECORD",bg='white', font=('arial',9,'bold')).grid(row=1,columnspan=4,pady=20)

btn1 = Button(page,width=5,text='File',bg='white',fg='silver',font=('arial',6,'bold'),borderwidth=0,command=lambda:goto('btn1')).grid(row=3,column=0)
btn2 = Button(page,width=5,text='New',bg='white',fg='silver',font=('arial',6,'bold'),borderwidth=0,command=lambda:goto('btn2')).grid(row=3,column=1)
btn3 = Button(page,width=5,text='Update',bg='white',fg='silver',font=('arial',6,'bold'),borderwidth=0,command=lambda:goto('btn3')).grid(row=3,column=2)
btn4 = Button(page,width=5,text='Admin',bg='white',fg='silver',font=('arial',6,'bold'),borderwidth=0,command=lambda:goto('btn4')).grid(row=3,column=3)

frame1 = Frame(page,bg='white')
Label(frame1,text='OPEN FILE',fg='blue',bg='white',font=('arial',9,'bold')).grid(row=0,pady=40)
num_lab = Label(frame1,text='File Number : ',bg='white',font=('arial',6))
num_lab.grid(row=1,sticky='w',pady=10)
search_entry = Entry(frame1)
search_entry.grid(row=2,ipady=50,ipadx=130,pady=10)
nam_lab = Label(frame1,text="Patient's Name : ",bg='white',font=('arial',6))
name_entry = Entry(frame1)
swh_num = Button(frame1, text='Search with File Number', command=lambda:goto('num'),fg='silver',bg='white',borderwidth=0, font=('arial',5,'italic'))
swh_nam = Button(frame1, text='Search with Patient Name', command=lambda:goto('nam'),fg='silver', bg='white',borderwidth=0, font=('arial',5,'italic'))
swh_nam.grid(row=3,pady=10,sticky='e')
Button(frame1, text='Search', command=search, bg='white',borderwidth=0, fg='blue', font=('arial',6,'bold')).grid(row=6,pady=40)

frame2 = Frame(page,bg='white')
image = Entry(frame2)
image.grid(row=2,column=1,pady=10,sticky='e',ipadx=22)
name = Entry(frame2)
name.grid(row=4, column=1,pady=10,ipadx=70)
address = Entry(frame2)
address.grid(row=5, column=1,pady=10,ipadx=70)
sex = Entry(frame2)
sex.grid(row=6, column=1,pady=10,ipadx=70)
age = Entry(frame2)
age.grid(row=7, column=1,pady=10,ipadx=70)
phone = Entry(frame2)
phone.grid(row=8, column=1,pady=10,ipadx=70)
ref_name = Entry(frame2)
ref_name.grid(row=10, column=1,pady=10,ipadx=70)
ref_address = Entry(frame2)
ref_address.grid(row=11, column=1,pady=10,ipadx=70)
ref_phone = Entry(frame2)
ref_phone.grid(row=12, column=1,pady=10,ipadx=70)

Label(frame2, text="CREATE NEW FILE",bg='white', font=('arial',6,'bold')).grid(row=0, columnspan=2, pady=10)
Label(frame2, text="Passport Photo : ",bg='white', font=('arial',6)).grid(row=2, columnspan=2, pady=20, sticky='w')
Label(frame2, text="Patient's Information",bg='white', fg='blue', font=('arial',6,'bold')).grid(row=1, columnspan=2, pady=20, sticky='w')
Label(frame2, text='Name :',bg='white', font=('arial',6)).grid(row=4, column=0, sticky='w')
Label(frame2, text='Address :',bg='white', font=('arial',6)).grid(row=5, column=0, sticky='w')
Label(frame2, text='Sex :',bg='white', font=('arial',6)).grid(row=6, column=0, sticky='w')
Label(frame2, text='Age :',bg='white', font=('arial',6)).grid(row=7, column=0, sticky='w')
Label(frame2, text='Phone :',bg='white', font=('arial',6)).grid(row=8, column=0, sticky='w')
Label(frame2,text="Reference's Information",bg='white',fg='blue',font=('arial',6,'bold')).grid(row=9,columnspan=2,pady=20,sticky='w')
Label(frame2,text='Name :',bg='white',font=('arial',6)).grid(row=10,column=0,sticky='w')
Label(frame2,text='Address :',bg='white',font=('arial',6)).grid(row=11,column=0,sticky='w')
Label(frame2,text='Phone :',bg='white',font=('arial',6)).grid(row=12,column=0,sticky='w')
Button(frame2,text='Submit',bg='white',borderwidth=0,command=submit,font=('arial',5,'bold')).grid(row=13, columnspan=2,pady=20)
Button(frame2,text='Open',bg='white',borderwidth=0,command=open,font=('arial',4,'bold')).grid(row=3, column=1,sticky='e')

frame3 = Frame(page,bg='white')
Label(frame3, text="UPDATE FILE",bg='white',fg='green', font=('arial',9,'bold')).grid(row=0, columnspan=2, pady=10)
Label(frame3, text="File Number : ",bg='white', font=('arial',6)).grid(row=1, column=0, pady=20, sticky='w')
update_entry = Entry(frame3)
update_entry.grid(row=1,column=1,ipadx=40,pady=20,sticky=E)
Label(frame3, text="Column : ",bg='white', font=('arial',6)).grid(row=2, column=0, pady=20, sticky='w')
column = Combobox(frame3,values=columns)
column.grid(row=2,column=1,ipadx=10,pady=20,sticky='w')
Label(frame3, text="New Content : ",bg='white', font=('arial',6)).grid(row=3, column=0, pady=20, sticky='w')
column_entry = Entry(frame3)
column_entry.grid(row=3,column=1,ipadx=40,pady=20,sticky=E)
Button(frame3,text='Update',bg='white',font=('arial',5,'bold'), fg='green', borderwidth=0, command=update).grid(row=12, columnspan=2,pady=10)

frame4 = Frame(page,bg='white')
Label(frame4,text='ADMINISTRATION',fg='grey',bg='white',font=('arial',9,'bold')).grid(row=0,columnspan=2,pady=20)
Label(frame4,text='To Show Database',bg='white',font=('arial',6)).grid(row=1,columnspan=2,sticky='w')
Button(frame4,bg='white',text='Click Here...', borderwidth=0, command=query, font=('arial',5,'bold')).grid(row=2, columnspan=2, pady=20)
Label(frame4, text='DELETE FILE',bg='white',fg='red',font=('arial',6,'bold')).grid(row=3, columnspan=2, sticky='w')
Label(frame4,text='File Number : ',bg='white',font=('arial',6)).grid(row=4,column=0,sticky='w',pady=10)
del_entry = Entry(frame4)
del_entry.grid(row=4, column=1,ipadx=45,pady=20)
del_btn = Button(frame4,bg='white',text='Click Here to Delete...', borderwidth=0, fg='red',command=delete, font=('arial',5,'bold')).grid(row=5, columnspan=2, pady=(0,20))

frame5 = Frame(page,bg='white')
Button(frame5,bg='white',text='✘',borderwidth=0, fg='red',command=lambda:goto('back'), font=('arial',7,'bold')).grid(row=0, column=1, pady=10,sticky='e')
pic = Label(frame5)
pic.grid(row=1,columnspan=2)
output = Text(frame5,width=36, height=17)
output.grid(row=2,columnspan=2)

page.mainloop()