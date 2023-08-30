from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import  *
from sqlite3 import *
import requests
import matplotlib.pyplot as plt

def f1():
	mw.withdraw()
	aw.deiconify()

def f2():
	aw.withdraw()
	mw.deiconify()

def f3():
	mw.withdraw()
	vw.deiconify()
	vw_st_data.delete(1.0,END)
	con=None
	try:
		con=connect("proj.db")
		cursor=con.cursor()			
		sql="select * from emp"
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for d in data:
			info=info+"id="+str(d[0])+"  "+"name="+str(d[1])+"  "+"salary="+str(d[2])+"\n"
		vw_st_data.insert(INSERT,info)
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
def f4():
	vw.withdraw()
	mw.deiconify()

def f5():
	mw.withdraw()
	uw.deiconify()

def f6():
	uw.withdraw()
	mw.deiconify()

def f7():
	mw.withdraw()
	dw.deiconify()

def f8():
	dw.withdraw()
	mw.deiconify()

def  charts():
	
	con=None
	try:
		con=connect("proj.db")
		cursor=con.cursor()
		sql="SELECT name,salary FROM emp ORDER BY salary DESC  LIMIT 5"
		cursor.execute(sql)
		data=cursor.fetchall()		
		name=[d[0] for d in data]
		salary=[d[1] for d in data]
		plt.bar(name,salary,width=1.0, color=["green","yellow"])
		plt.xlabel("name")
		plt.ylabel("salary")
		plt.title("bargraph")
		plt.xticks(rotation=45) 
		plt.tight_layout()
		plt.show()
	except Exception as e:
		showerror("issues",e)
	finally:
		if con is not None:
			con.close()

def add():
	con=None
	try:
		con=connect("proj.db")
		cursor=con.cursor()			
		sql="insert into  emp values('%d','%s','%d')"
		id=int(aw_ent_id.get())
		name=aw_ent_name.get()
		if not name.isalpha() or len(name) < 2:
			raise Exception("name should contain more than  two alphabhets") 
		salary=int(aw_ent_salary.get())
		cursor.execute(sql%(id,name,salary))
		con.commit()		
		showinfo("Sucess","info SAVED")
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
		aw_ent_id.delete(0,END)
		aw_ent_name.delete(0,END)
		aw_ent_salary.delete(0,END)
		aw_ent_id.focus()

def update():
	con=None
	try:
		con=connect("proj.db")
		cursor=con.cursor()			
		sql="update  emp set name='%s',salary='%d' where id='%d'"
		name=uw_ent_name.get()
		salary=int(uw_ent_salary.get())
		id=int(uw_ent_id.get())
		cursor.execute(sql%(name,salary,id))
		if cursor.rowcount == 1:
			con.commit()		
			showinfo("Sucess","record updated")
		else:
			showinfo("record does not exists")
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
		uw_ent_id.delete(0,END)
		uw_ent_name.delete(0,END)
		uw_ent_salary.delete(0,END)
		uw_ent_id.focus()

def delete():
	con=None
	try:
		con=connect("proj.db")
		cursor=con.cursor()			
		sql="delete  from emp  where id='%d'"
		id=int(dw_ent_id.get())
		cursor.execute(sql % (id))
		if cursor.rowcount == 1:
			con.commit()		
			showinfo("Sucess","record deleted")
		else:
			showinfo(" record does not exists")
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
		dw_ent_id.delete(0,END)
		dw_ent_id.focus()

def temperature():
	try:
		wa = "https://ipinfo.io/"
		res = requests.get(wa)
		data = res.json()
		city_name=data["city"]
		loc = data["loc"]										
		loc_var.set(f"Loc:{data['loc']}")

		a1="https://api.openweathermap.org/data/2.5/weather"
		a2="?q="+city_name
		a3="&appid="+"c6e315d09197cec231495138183954bd"		#key
		a4="&units="+"metric"
		webadd=a1+a2+a3+a4
		res=requests.get(webadd)
		weather_data=res.json()
		actual_temp=weather_data["main"]["temp"]
		temp_var.set(f"temp:{actual_temp} \u00B0C")
	except Exception as e:
		showerror("issue",e)




mw=Tk()
mw.configure(bg="lightyellow")
mw.title("EMS")
mw.geometry("700x700+50+50")
f=("Simsum",30,"bold")

loc_var=StringVar()
temp_var=StringVar()


mw_btn_add=Button(mw,text="Add",font=f,bg="azure",width=15,command=f1)
mw_btn_view=Button(mw,text="View",font=f,bg="azure",width=15,command=f3)
mw_btn_update=Button(mw,text="Update",font=f,bg="azure",width=15,command=f5)
mw_btn_delete=Button(mw,text="Delete",font=f,bg="azure",width=15,command=f7)
mw_btn_charts=Button(mw,text="Charts",font=f,bg="azure",width=15,command=charts)
mw_lab_loc=Label(mw,textvariable=loc_var,font=f,bg="white",width=18)
mw_lab_temp=Label(mw,textvariable=temp_var,font=f,bg="white",width=12)

mw_btn_add.pack(pady=10)
mw_btn_view.pack(pady=10)
mw_btn_update.pack(pady=10)
mw_btn_delete.pack(pady=10)
mw_btn_charts.pack(pady=10)
mw_lab_loc.pack(side=LEFT,pady=10)

mw_lab_temp.pack(side=LEFT,pady=10)
temperature()

aw=Toplevel(mw)
aw['bg']='lightyellow'
aw.title("Add Emp")
aw.geometry("500x700+50+50")

aw_lab_id=Label(aw,text="enter id ",bg="lightyellow",font=f)
aw_ent_id=Entry(aw,font=f)
aw_lab_name=Label(aw,text="enter  name",bg="lightyellow",font=f)
aw_ent_name=Entry(aw,font=f)
aw_lab_salary=Label(aw,text="enter salary ",bg="lightyellow",font=f)
aw_ent_salary=Entry(aw,font=f)
aw_btn_save=Button(aw,text="Save",bg="azure",font=f,command=add)
aw_btn_back=Button(aw,text="Back",font=f,bg="azure",command=f2)

aw_lab_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lab_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lab_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)
aw.withdraw()
aw.resizable(0,0)


vw=Toplevel(mw)
vw['bg']='lightyellow'
vw.title("View Emp")
vw.geometry("800x700+50+50")

vw_st_data=ScrolledText(vw,width=50,height=10,bg="azure",font=f )
vw_btn_back=Button(vw,text="Back",font=f,bg="azure",command=f4)
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=10)
vw.withdraw()
vw.resizable(0,0)

uw=Toplevel(mw)
uw['bg']='lightyellow'
uw.title("Update Emp")
uw.geometry("700x700+50+50")
s=IntVar()
uw_lab_id=Label(uw,text="enter id ",bg="lightyellow",font=f)
uw_ent_id=Entry(uw,font=f)
uw_lab_name=Label(uw,text="enter  name",bg="lightyellow",font=f)
uw_ent_name=Entry(uw,font=f)
uw_lab_salary=Label(uw,text="enter salary ",bg="lightyellow",font=f)
uw_ent_salary=Entry(uw,font=f)
uw_btn_save=Button(uw,text="Save",bg="azure",font=f,command=update)
uw_btn_back=Button(uw,text="Back",font=f,bg="azure",command=f6)

uw_lab_id.pack(pady=10)
uw_ent_id.pack(pady=10)
uw_lab_name.pack(pady=10)
uw_ent_name.pack(pady=10)
uw_lab_salary.pack(pady=10)
uw_ent_salary.pack(pady=10)
uw_btn_save.pack(pady=10)
uw_btn_back.pack(pady=10)
uw.withdraw()
uw.resizable(0,0)



dw=Toplevel(mw)
dw['bg']='lightyellow'
dw.title("Delete Emp")
dw.geometry("500x500+50+50")

dw_lab_id=Label(dw,text="enter id ",bg="lightyellow",font=f)
dw_ent_id=Entry(dw,font=f)
dw_btn_save=Button(dw,text="Save",bg="azure",font=f ,command=delete)
dw_btn_back=Button(dw,text="Back",font=f,bg="azure",command=f8)

dw_lab_id.pack(pady=10)
dw_ent_id.pack(pady=10)
dw_btn_save.pack(pady=10)
dw_btn_back.pack(pady=10)
dw.withdraw()
dw.resizable(0,0)

def windowclose():
	if askyesno("	Quit","tussi ja rahe ho"):
		if askyesno("	Quit","Sacchi"):
			if askyesno("	Quit","tussi na jao"):
				mw.destroy()
mw.protocol("WM_DELETE_WINDOW",windowclose)
mw.resizable(0,0)
mw.mainloop()