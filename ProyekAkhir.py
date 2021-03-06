# Aplikasi Pengukuran Tanpa Serial

import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pymysql, serial, openpyxl # modul / library pihak ketiga, WAJIB DI-INSTALL
import serial.tools.list_ports 
import matplotlib.pyplot as plt # modul / library pihak ketiga, WAJIB DI-INSTALL
import pandas as pad # modul / library pihak ketiga, WAJIB DI-INSTALL

# UNTUK TUTORIAL INSTALL BISA DILIHAT PADA README.txt

def raise_frame(frame):
    frame.tkraise()
	
def	login_system():
	u = (Username.get())
	p = (Password.get())
	if (u == ('admin') and p == ('password')):
		raise_frame(Window2)
	else:
		messagebox.showinfo('Login Systems', 'Akses Ditolak!!\nCoba Lagi!!')
		Reset()
	
def Reset():
	Username.set("")
	Password.set("")
	txtUsername.focus()

def iExit():
	iExit = tkinter.messagebox.showinfo("Login Systems", "You decided to Exit!!")
	root.destroy()

def serial_ports():
	return serial.tools.list_ports.comports()

def on_select(event = None):
	print('event widgets : ', event.widget.get())
	print('combobox : ', portCombo.get())

def fetch_data():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute("SELECT * from baby WHERE id = %s, nama = %s", ID_vr.get(), Nama.get())
	rows = cur.fetchall()
	if len(rows) != 0:
		tabelUkur.delete(tabelUkur.get_children())
		for row in rows:
			tabelUkur.insert('', END, values = row)
		con.commit()
	con.close()

def pause():
	root.after_cancel(update)
	
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Fungsi untuk membaca serial pada Alat Pembaca Berat Dan Tinggi Balita
# Comment bila tidak diperlukan

arduinoSerialData = serial.Serial('com17', 9600)
	
def nilaiSensor():
	if True:
		global nilaiUkurTinggi, nilaiUkurBerat, root, update
		x = arduinoSerialData.readline()
		values = str(x.decode().strip())
		y = values.split('#')
		Tinggi.set(y[0])
		Berat.set(y[1])
		update = root.after(700, nilaiSensor)
	
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
root = Tk()
root.geometry('1350x690+0-0')
root.title("Pengukuran Tinggi dan Berat Balita")
root.iconbitmap("logo.ico")			#  Membaca logo pada aplikasi || harus di directory atau folder yang sama pada program || comment bila tidak diperlukan
root.config(bg = 'gray')

Window1 = Frame(root, width = 1350, height = 690, bg = 'gray')
Window2 = Frame(root, width = 1350, height = 690)
Window3 = Frame(root, width = 1350, height = 690, bg = '#666699')

for frame in (Window1, Window2, Window3):
	frame.grid(row = 0, column = 0, sticky = 'nesw')

#===================================VARIABEL=========================	
Username = StringVar()
Password = StringVar()

ID_vr = StringVar()
Nama = StringVar()
Jenis_Kelamin = StringVar()
Tempat_Lahir = StringVar()
Tanggal_Lahir = StringVar()
Anak_Ke = StringVar()
Nama_Ayah = StringVar()
Nama_Ibu = StringVar()
txt_Alamat = StringVar()

searchBy = StringVar()
searchTxt = StringVar()

pengukuranKe = StringVar()
tanggalUkur = StringVar()
Tinggi = StringVar()
Berat = StringVar()
	
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#===========================================WINDOW 1=============================================
lblTitle = Label(Window1, text = 'MEASUREMENT LOGIN SYSTEMS', font = ('arial', 20, 'bold'), bg = 'gray', fg = 'black')
lblTitle.place(x = 450, y = 160)

#=============================================================================================
LoginFrame1 = Label(Window1, width = 800, height = 200, font = ('arial', 12, 'bold'), relief = 'ridge', bg = 'white', bd = 10)
LoginFrame1.place(x = 520, y = 210)

LoginFrame2 = Label(Window1, width = 100, height = 200, font = ('arial', 12, 'bold'), relief = 'ridge', bg = 'white', bd = 10)
LoginFrame2.place(x = 420, y = 280)
	
#========================================Label and Entry===================================
lblUsername = Label(LoginFrame1, text = 'Username', font = ('arial', 12, 'bold'))
lblUsername.grid(row = 0, column = 0)
txtUsername = Entry(LoginFrame1, font = ('arial', 12), textvariable = Username)
txtUsername.grid(row = 0, column = 1)

lblPassword = Label(LoginFrame1, text = 'Password', font = ('arial', 12, 'bold'))
lblPassword.grid(row = 1, column = 0)
txtPassword = Entry(LoginFrame1, font = ('arial', 12, 'bold'), show = '*', textvariable = Password)
txtPassword.grid(row = 1, column = 1)

#=========================================Button=================================================
btnLogin = Button(LoginFrame2, text = 'Login', width = 20, command = login_system)
btnLogin.grid(row = 3, column = 0)
btnReset = Button(LoginFrame2, text = 'Reset', width = 20, command = Reset)
btnReset.grid(row = 3, column = 1)
btnExit = Button(LoginFrame2, text = 'Exit', width = 20, command = iExit)
btnExit.grid(row = 3, column = 2)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# WAJIB DIBACA!!!!
# GUNAKAN DATABASE DAN TABLE YANG SESUAI PADA MASING-MASING KEPERLUAN YANG DIGUNAKAN
# (.....database = 'stm') ==> sesuaikan nama dengan database yang digunakan
# (.....INSERT INTO baby) ==> sesuaikan nama dengan table yang diperlukan


def add_balita():
	if ID_vr.get() == '' or Nama.get() == '' or Nama_Ibu.get() == '':
		messagebox.showerror('Error', 'Semua Data Harus Diisi Terlebih Dahulu!!')
	else:
		con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
		cur = con.cursor()
		cur.execute("INSERT INTO baby VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",(ID_vr.get(),
																					Nama.get(),
																					Jenis_Kelamin.get(), 
																					Tempat_Lahir.get(), 
																					Tanggal_Lahir.get(), 
																					Anak_Ke.get(), 
																					Nama_Ayah.get(), 
																					Nama_Ibu.get(),
																					txt_Alamat.get('1.0', END)
																					))
		con.commit()
		fetch_data()
		con.close()
		messagebox.showinfo('Success', 'Biodata Telah Disimpan!!')
	
# // Hapus method yang di bawah ini
	
def fetch_data():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute('SELECT * FROM baby')
	rows = cur.fetchall()
	if len(rows) != 0:
		baby_Table.delete(*baby_Table.get_children())
		for row in rows:
			baby_Table.insert('', END, values = row)
		con.commit()
	con.close()

def clear():
	ID_vr.set('')
	Nama.set('')
	Jenis_Kelamin.set('')
	Tempat_Lahir.set('')
	Tanggal_Lahir.set('')
	Anak_Ke.set('')
	Nama_Ayah.set('')
	Nama_Ibu.set('')
	txt_Alamat.delete('1.0', END)
	
def get_cursor(ev):	
	cursor_row = baby_Table.focus()
	contents = baby_Table.item(cursor_row)
	row = contents['values']
	ID_vr.set(row[0])
	Nama.set(row[1])
	Jenis_Kelamin.set(row[2])
	Tempat_Lahir.set(row[3])
	Tanggal_Lahir.set(row[4])
	Anak_Ke.set(row[5])
	Nama_Ayah.set(row[6])
	Nama_Ibu.set(row[7])
	txt_Alamat.delete('1.0', END)
	txt_Alamat.insert(END, row[8])
	
def update_data():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute(
	"UPDATE baby SET nama = %s, kelamin = %s, tempat = %s, tanggal = %s, anak = %s, ayah = %s, ibu = %s, alamat = %s WHERE id = %s", 
						   Namis_Kelamin.get(),
						   Tempat_Lahir.get(),
						   Tanggal_Lahir.get(),
						   Anak_Ke.get(),
						   Nama_Ayah.get(),
						   Nama_Ibu.get(),
						   txt_Alamat.get('1.0', END),
						   ID_vr.get()
							)
	con.commit()
	fetch_data()
	clear()
	con.close()
	messagebox.showinfo('Success', 'Biodata Telah Diupdate!!')
		
def delete_data():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute('DELETE FROM baby WHERE id = %s', ID_vr.get())
	con.commit()
	con.close()
	fetch_data()
	clear()
	messagebox.showinfo('Success', 'Biodata Telah Dihapus!!')
		
def search_data():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute("SELECT * FROM baby WHERE "+ str(searchBy.get()) + " LIKE '%" + str(searchTxt.get()) + "%'")
	rows = cur.fetchall()
	if len(rows) != 0:
		baby_Table.delete(*baby_Table.get_children())
		for row in rows:
			baby_Table.insert('', END, values = row)
		con.commit()
	con.close()

#=================================================================================================
# Function untuk penyimpanan pengukuran balita

def save_data():
	if pengukuranKe.get() == '' or tanggalUkur.get() == '':
		messagebox.showerror('Error', 'Semua Data Harus Diisi Terlebih Dahulu!!')
	else:
		
		con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
		cur = con.cursor()
		cur.execute("INSERT INTO graph VALUES (%s, %s, %s, %s, %s, %s, %s)", (ID_vr.get(), Nama.get(), pengukuranKe.get(), tanggalUkur.get(), Berat.get(), Tinggi.get(), Jenis_Kelamin.get()))
		con.commit()
		fetch_data2()
		con.close()
		messagebox.showinfo('Success', 'Hasil Pengukuran Telah Disimpan Ke Database!')
		
def fetch_data2():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute("SELECT * FROM graph")
	rows = cur.fetchall()
	if len(rows) != 0:
		tabelUkur.delete(*tabelUkur.get_children())
		for row in rows:
			tabelUkur.insert('', END, values = row)
		con.commit()
	con.close()

def clear2():
	ID_vr.set('')
	Nama.set('')
	Jenis_Kelamin.set('')
	Tempat_Lahir.set('')
	Tanggal_Lahir.set('')
	Nama_Ibu.set('')
	pengukuranKe.set('')
	tanggalUkur.set('')
	Berat.set('')
	Tinggi.set('')
	
def delete_data2():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute("DELETE FROM graph WHERE id = %s AND pengukuran = %s", (ID_vr.get(), pengukuranKe.get()))
	con.commit()
	con.close()
	fetch_data2()
	messagebox.showinfo('Success', 'Hasil Pengukuran Berhasil Dihapus dari Database!!')
	clear2()

def edit_data():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute("UPDATE graph SET pengukuran = %s, tanggal = %s WHERE tinggi = %s", (pengukuranKe.get(), tanggalUkur.get(), Tinggi.get()))
	con.commit()
	fetch_data2()
	con.close()
	messagebox.showinfo('Success', 'Biodata Telah Diupdate!!')
	
def get_cursor2(ev):
	cursor_row = tabelUkur.focus()
	contents = tabelUkur.item(cursor_row)
	row = contents['values']
	ID_vr.set(row[0])
	Nama.set(row[1])
	pengukuranKe.set(row[2])
	tanggalUkur.set(row[3])
	Berat.set(row[4])
	Tinggi.set(row[5])
	Jenis_Kelamin.set(row[6])
	
def sort_column(tabelUkur, col, reverse):
	l = [(tabelUkur.set(k, col), k) for k in tabelUkur.get_children('')]
	l.sort(reverse = reverse)
	
	for index, (val, k) in enumerate(l):
		tabelUkur.move(k, '', index)
		
	tabelUkur.heading(col, command = lambda _col = col : sort_column(tabelUkur, _col, not reverse))

def check_graphics():
	con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	cur = con.cursor()
	cur.execute("SELECT * FROM graph ORDER BY graph . tanggal ASC")
	cur.execute("SELECT tanggal, berat, tinggi FROM graph WHERE id = {}".format(ID_vr.get()))

	query = "SELECT * FROM graph WHERE id = {}".format(ID_vr.get())
	read_SQL = pd.read_sql_query(query, con)
	df = pd.DataFrame(read_SQL, columns = ['nama', 'pengukuran', 'tanggal', 'berat', 'tinggi'])

	query1 = "SELECT * FROM baby WHERE id = {}".format(ID_vr.get())
	read_SQL1 = pd.read_sql_query(query1, con)
	df1 = pd.DataFrame(read_SQL1, columns = ['nama', 'kelamin', 'tanggal'])

	gender = df1['kelamin'].tail(1).str.split().tolist()
	gender_1 = gender[0][0]

	name = df['nama'].tail(1).str.split().tolist()
	name_1 = name[0][0] + " " + name[0][1]
	print(name_1)

	result = cur.fetchall()
	tanggal = []
	berat = []
	berat_new = []
	tinggi = []
	tinggi_new = []

	for record in result:
		tinggi.append(record[2])
		berat.append(record[1])
		tanggal.append(record[0])

	for ax in range(len(berat)):
		new_ax = float(berat[ax])
		berat_new.append(new_ax)
		ax += 1

	for bx in range(len(tinggi)):
		new_bx = float(tinggi[bx])
		tinggi_new.append(new_bx)
		bx += 1

	beratUkur = berat_new[-1]
	tinggiUkur = tinggi_new[-1]

	case = {
			'Januari' : 1,
			'Februari' : 2,
			'Maret' : 3,
			'April' : 4,
			'Mei' : 5,
			'Juni' : 6,
			'Juli' : 7,
			'Agustus' : 8,
			'September' : 9,
			'Oktober' : 10,
			'November' : 11,
			'Desember' : 12
		}

	bulanLahir = df1['tanggal'].tail(1).str.split().tolist()
	bulanLahir_1 = bulanLahir[0][1]
	bulanLahir_2 = case.get(bulanLahir_1)
	tahunLahir_1 = int(bulanLahir[0][2])

	bulanUkur = df['tanggal'].str.split().tolist()

	m = 0
	umurUkur = []
	for umurBulan in bulanUkur:
		umurBulan = bulanUkur[m][1]
		tahunUkur = int(bulanUkur[m][-1])
		umurBulan_1 = case.get(umurBulan)
		umurDalamBulan = umurBulan_1 - bulanLahir_2
		totalUmur = ((tahunUkur - tahunLahir_1) * 12) + umurDalamBulan
		umurUkur.append(totalUmur)
		m += 1

	bulanUkur = df['tanggal'].tail(1).str.split().tolist()
	bulanUkur_1 = bulanUkur[0][1]
	bulanUkur_2 = case.get(bulanUkur_1)
	tahunUkur_1 = int(bulanUkur[0][2])

	batasUmur = [0, 12, 24, 36, 48, 60]

	# KMS laki-laki

	beratLakiBurukOver = [5.0, 13.3, 17.0, 20.6, 23.8, 27.3]
	tinggiLakiBurukOver = [56.0, 83.0, 96.3, 107.2, 115.9, 123.7]

	beratLakiCukupBurukOver = [4.5, 12.0, 15.3, 18.4, 21.2, 24.1]
	tinggiLakiCukupBurukOver = [54.0, 80.5, 93.2, 103.5, 111.7, 119.2]

	beratLakiCukupNormalOver = [3.9, 10.7, 13.7, 16.3, 18.5, 21.0]
	tinggiLakiCukupNormalOver = [52.0, 78.0, 90.2, 99.8, 107.5, 114.6]

	beratLakiNormal = [3.4, 9.6, 12.3, 14.3, 16.3, 18.3]
	tinggiLakiNormal = [50.0, 75.5, 87.1, 96.1, 103.3, 110.0]

	beratLakiCukupNormalUnder = [2.9, 8.6, 10.8, 12.7, 14.5, 16.0]
	tinggiLakiCukupNormalUnder = [48.0, 73.5, 84.1, 92.4, 99.1, 105.3]

	beratLakiCukupBurukUnder = [2.5, 7.7, 9.7, 11.4, 12.7, 14.1]
	tinggiLakiCukupBurukUnder = [46.0, 71.0, 81.0, 88.7, 94.9, 100.7]

	beratLakiBurukUnder = [2.1, 6.9, 8.6, 10.0, 11.4, 12.5]
	tinggiLakiBurukUnder = [44.0, 68.5, 78.0, 85.0, 90.7, 96.1]


	# KMS perempuan

	beratPerempuanBurukOver = [4.8, 12.9, 16.7, 20.5, 24.5, 28.5]
	tinggiPerempuanBurukOver = [55.0, 81.5, 95.4, 106.5, 115.7, 123.7]

	beratPerempuanCukupBurukOver = [4.4, 11.5, 14.8, 18.2, 21.5, 24.9]
	tinggiPerempuanCukupBurukOver = [53.5, 79.0, 92.2, 102.7, 111.3, 118.9]

	beratPerempuanCukupNormalOver = [3.8, 10.2, 13.0, 15.8, 18.5, 21.2]
	tinggiPerempuanCukupNormalOver = [52.5, 76.5, 88.9, 98.9, 107.0, 114.2]

	beratPerempuanNormal = [3.4, 9.0, 11.5, 13.9, 16.1, 18.2]
	tinggiPerempuanNormal = [49.5, 74.0, 85.7, 95.1, 102.7, 109.4]

	beratPerempuanCukupNormalUnder = [2.8, 7.9, 10.2, 12.2, 14.0, 15.8]
	tinggiPerempuanCukupNormalUnder = [47.0, 71.5, 82.5, 91.2, 98.4, 104.7]

	beratPerempuanCukupBurukUnder = [2.4, 7.0, 9.0, 10.8, 12.4, 13.8]
	tinggiPerempuanCukupBurukUnder = [45.5, 69.0, 79.3, 87.4, 94.1, 99.9]

	beratPerempuanBurukUnder = [2.0, 6.4, 8.1, 9.6, 10.9, 12.0]
	tinggiPerempuanBurukUnder = [44.0, 66.5, 76.0, 83.6, 89.8, 95.2]

	fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))
	print('berat_new : ', berat_new)
	print('tinggi_new : ', tinggi_new)

	contohBerat = [15.2, 16.2, 17.2, 18.2, 19.2, 20.2]
	contohTinggi = [90.2, 91.2, 92.2, 93.2, 94.2, 95.2]

	def pesan_berat1():
		pesan_berat1 = messagebox.showinfo('Success', 'Perkembangan Balita Buruk\nBerat Badan Balita Sangat Berlebih Untuk Seusianya. Sangat Disarankan Untuk Menurunkan Berat Badannya!!')
		
	def pesan_berat2():
		pesan_berat2 = messagebox.showinfo('Success', 'Perkembangan Balita Cukup Buruk\nBerat Badan Balita Berlebih Untuk Seusianya. Disarankan Untuk Menurunkan Berat Badannya!!')

	def pesan_berat3():
		pesan_berat3 = messagebox.showinfo('Success', 'Perkembangan Balita Cukup Normal\nBerat Badan Balita Cukup Normal Untuk Seusianya')

	def pesan_berat4():
		pesan_berat4 = messagebox.showinfo('Success', 'Perkembangan Balita Normal\nBerat Badan Balita Normal Untuk Seusianya')

	def pesan_berat5():
		pesan_berat5 = messagebox.showinfo('Success', 'Perkembangan Balita Cukup Normal\nBerat Badan Balita Cukup Normal Untuk Seusianya')

	def pesan_berat6():
		pesan_berat6 = messagebox.showinfo('Success', 'Perkembangan Balita Cukup Buruk\nBerat Badan Balita Kurang Untuk Seusianya. Disarankan Untuk Menambah Gizi dan Asupan Untuk Menaikkan Berat Badannya!!')

	def pesan_berat7():
		pesan_berat7 = messagebox.showinfo('Success', 'Perkembangan Balita Buruk\nBerat Badan Balita Sangat Kurang Untuk Seusianya. Sangat Disarankan Untuk Menambah Gizi dan Asupan Untuk Menaikkan Berat Badannya!!')

	def pesan_tinggi1():
		pesan_tinggi1 = messagebox.showinfo('Success', 'Perkembangan Balita Buruk\nTinggi Badan Balita Sangat Berlebih Untuk Seusianya!!')
		
	def pesan_tinggi2():
		pesan_tinggi2 = messagebox.showinfo('Success', 'Perkembangan Balita Cukup Buruk\nTinggi Badan Balita Berlebih Untuk Seusianya')

	def pesan_tinggi3():
		pesan_tinggi3 = messagebox.showinfo('Success', 'Perkembangan Balita Cukup Normal\nTinggi Badan Balita Cukup Normal Untuk Seusianya')

	def pesan_tinggi4():
		pesan_tinggi4 = messagebox.showinfo('Success', 'Perkembangan Balita Normal\nTinggi Badan Balita Normal Untuk Seusianya')

	def pesan_tinggi5():
		pesan_tinggi5 = messagebox.showinfo('Success', 'Perkembangan Balita Cukup Normal\nTinggi Badan Balita Cukup Normal Untuk Seusianya')

	def pesan_tinggi6():
		pesan_tinggi6 = messagebox.showinfo('Success', 'Perkembangan Balita Cukup Buruk\nTinggi Badan Balita Kurang Untuk Seusianya. Disarankan Untuk Menambah Gizi dan Asupan Untuk Menaikkan Tinggi Badannya!!')

	def pesan_tinggi7():
		pesan_tinggi7 = messagebox.showinfo('Success', 'Perkembangan Balita Buruk\nTinggi Badan Balita Sangat Kurang Untuk Seusianya. Sangat Disarankan Untuk Menambah Gizi dan Asupan Untuk Menaikkan Tinggi Badannya!!')

	# Algoritma penilaian perkembangan balita untuk laki-laki
	if gender_1 == 'Laki-Laki':

	# Umur sampai 12 bulan
		if totalUmur >= 0 and totalUmur <= 12:
			if berat_new[-1] >= beratLakiBurukOver[0]:
				pesan_berat1()
			elif berat_new[-1] >= beratLakiCukupBurukOver[0] and berat_new[-1] <= beratLakiBurukOver[0]:
				pesan_berat2()
			elif berat_new[-1] >= beratLakiCukupNormalOver[0] and berat_new[-1] <= beratLakiCukupBurukOver[0]:
				pesan_berat3()
			elif (berat_new[-1] >= beratLakiNormal[0] and berat_new[-1] <= beratLakiCukupNormalOver[0]) and (berat_new[-1] <= beratLakiNormal[0] and berat_new[-1] >= beratLakiCukupNormalUnder[0]):
				pesan_berat4()
			elif berat_new[-1] <= beratLakiCukupNormalUnder[0] and berat_new[-1] >= beratLakiNormal[0]:
				pesan_berat5()
			elif berat_new[-1] <= beratLakiCukupBurukUnder[0] and berat_new[-1] >= beratLakiCukupNormalUnder[0]:
				pesan_berat6()
			elif berat_new[-1] <= beratLakiBurukUnder[0]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiLakiBurukOver[0]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiLakiCukupBurukOver[0] and tinggi_new[-1] <= tinggiLakiBurukOver[0]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiLakiCukupNormalOver[0] and tinggi_new[-1] <= tinggiLakiCukupBurukOver[0]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiLakiNormal[0] and tinggi_new[-1] <= tinggiLakiCukupNormalOver[0]) and (tinggi_new[-1] <= tinggiLakiNormal[0] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[0]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiLakiCukupNormalUnder[0] and tinggi_new[-1] >= tinggiLakiNormal[0]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiLakiCukupBurukUnder[0] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[0]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiLakiBurukUnder[0]:
				pesan_tinggi7()

		# Umur 13 bulan sampai 24 bulan
		elif totalUmur >= 13 and totalUmur <= 24:
			if berat_new[-1] >= beratLakiBurukOver[1]:
				pesan_berat1()
			elif berat_new[-1] >= beratLakiCukupBurukOver[1] and berat_new[-1] <= beratLakiBurukOver[1]:
				pesan_berat2()
			elif berat_new[-1] >= beratLakiCukupNormalOver[1] and berat_new[-1] <= beratLakiCukupBurukOver[1]:
				pesan_berat3()
			elif (berat_new[-1] >= beratLakiNormal[1] and berat_new[-1] <= beratLakiCukupNormalOver[1]) and (berat_new[-1] <= beratLakiNormal[1] and berat_new[-1] >= beratLakiCukupNormalUnder[1]):
				pesan_berat4()
			elif berat_new[-1] <= beratLakiCukupNormalUnder[1] and berat_new[-1] >= beratLakiNormal[1]:
				pesan_berat5()
			elif berat_new[-1] <= beratLakiCukupBurukUnder[1] and berat_new[-1] >= beratLakiCukupNormalUnder[1]:
				pesan_berat6()
			elif berat_new[-1] <= beratLakiBurukUnder[1]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiLakiBurukOver[1]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiLakiCukupBurukOver[1] and tinggi_new[-1] <= tinggiLakiBurukOver[1]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiLakiCukupNormalOver[1] and tinggi_new[-1] <= tinggiLakiCukupBurukOver[1]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiLakiNormal[1] and tinggi_new[-1] <= tinggiLakiCukupNormalOver[1]) and (tinggi_new[-1] <= tinggiLakiNormal[1] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[1]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiLakiCukupNormalUnder[1] and tinggi_new[-1] >= tinggiLakiNormal[1]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiLakiCukupBurukUnder[1] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[1]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiLakiBurukUnder[1]:
				pesan_tinggi7()

		# Umur 25 bulan sampai 36 bulan
		elif totalUmur >= 25 and totalUmur <= 36:
			if berat_new[-1] >= beratLakiBurukOver[2]:
				pesan_berat1()
			elif berat_new[-1] >= beratLakiCukupBurukOver[2] and berat_new[-1] <= beratLakiBurukOver[2]:
				pesan_berat2()
			elif berat_new[-1] >= beratLakiCukupNormalOver[2] and berat_new[-1] <= beratLakiCukupBurukOver[2]:
				pesan_berat3()
			elif (berat_new[-1] >= beratLakiNormal[2] and berat_new[-1] <= beratLakiCukupNormalOver[2]) and (berat_new[-1] <= beratLakiNormal[2] and berat_new[-1] >= beratLakiCukupNormalUnder[2]):
				pesan_berat4()
			elif berat_new[-1] <= beratLakiCukupNormalUnder[2] and berat_new[-1] >= beratLakiNormal[2]:
				pesan_berat5()
			elif berat_new[-1] <= beratLakiCukupBurukUnder[2] and berat_new[-1] >= beratLakiCukupNormalUnder[2]:
				pesan_berat6()
			elif berat_new[-1] <= beratLakiBurukUnder[2]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiLakiBurukOver[2]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiLakiCukupBurukOver[2] and tinggi_new[-1] <= tinggiLakiBurukOver[2]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiLakiCukupNormalOver[2] and tinggi_new[-1] <= tinggiLakiCukupBurukOver[2]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiLakiNormal[2] and tinggi_new[-1] <= tinggiLakiCukupNormalOver[2]) and (tinggi_new[-1] <= tinggiLakiNormal[2] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[2]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiLakiCukupNormalUnder[2] and tinggi_new[-1] >= tinggiLakiNormal[2]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiLakiCukupBurukUnder[2] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[2]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiLakiBurukUnder[2]:
				pesan_tinggi7()

		# Umur 37 bulan sampai 48 bulan
		elif totalUmur >= 37 and totalUmur <= 48:
			if berat_new[-1] >= beratLakiBurukOver[3]:
				pesan_berat1()
			elif berat_new[-1] >= beratLakiCukupBurukOver[3] and berat_new[-1] <= beratLakiBurukOver[3]:
				pesan_berat2()
			elif berat_new[-1] >= beratLakiCukupNormalOver[3] and berat_new[-1] <= beratLakiCukupBurukOver[3]:
				pesan_berat3()
			elif (berat_new[-1] >= beratLakiNormal[3] and berat_new[-1] <= beratLakiCukupNormalOver[3]) and (berat_new[-1] <= beratLakiNormal[3] and berat_new[-1] >= beratLakiCukupNormalUnder[3]):
				pesan_berat4()
			elif berat_new[-1] <= beratLakiCukupNormalUnder[3] and berat_new[-1] >= beratLakiNormal[3]:
				pesan_berat5()
			elif berat_new[-1] <= beratLakiCukupBurukUnder[3] and berat_new[-1] >= beratLakiCukupNormalUnder[3]:
				pesan_berat6()
			elif berat_new[-1] <= beratLakiBurukUnder[3]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiLakiBurukOver[3]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiLakiCukupBurukOver[3] and tinggi_new[-1] <= tinggiLakiBurukOver[3]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiLakiCukupNormalOver[3] and tinggi_new[-1] <= tinggiLakiCukupBurukOver[3]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiLakiNormal[3] and tinggi_new[-1] <= tinggiLakiCukupNormalOver[3]) and (tinggi_new[-1] <= tinggiLakiNormal[3] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[3]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiLakiCukupNormalUnder[3] and tinggi_new[-1] >= tinggiLakiNormal[3]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiLakiCukupBurukUnder[3] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[3]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiLakiBurukUnder[3]:
				pesan_tinggi7()


		# Umur 49 bulan sampai 60 bulan
		elif totalUmur >= 49 and totalUmur <= 60:
			if berat_new[-1] >= beratLakiBurukOver[4]:
				pesan_berat1()
			elif berat_new[-1] >= beratLakiCukupBurukOver[4] and berat_new[-1] <= beratLakiBurukOver[4]:
				pesan_berat2()
			elif berat_new[-1] >= beratLakiCukupNormalOver[4] and berat_new[-1] <= beratLakiCukupBurukOver[4]:
				pesan_berat3()
			elif (berat_new[-1] >= beratLakiNormal[4] and berat_new[-1] <= beratLakiCukupNormalOver[4]) and (berat_new[-1] <= beratLakiNormal[4] and berat_new[-1] >= beratLakiCukupNormalUnder[4]):
				pesan_berat4()
			elif berat_new[-1] <= beratLakiCukupNormalUnder[4] and berat_new[-1] >= beratLakiNormal[4]:
				pesan_berat5()
			elif berat_new[-1] <= beratLakiCukupBurukUnder[4] and berat_new[-1] >= beratLakiCukupNormalUnder[4]:
				pesan_berat6()
			elif berat_new[-1] <= beratLakiBurukUnder[4]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiLakiBurukOver[4]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiLakiCukupBurukOver[4] and tinggi_new[-1] <= tinggiLakiBurukOver[4]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiLakiCukupNormalOver[4] and tinggi_new[-1] <= tinggiLakiCukupBurukOver[4]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiLakiNormal[4] and tinggi_new[-1] <= tinggiLakiCukupNormalOver[4]) and (tinggi_new[-1] <= tinggiLakiNormal[4] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[4]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiLakiCukupNormalUnder[4] and tinggi_new[-1] >= tinggiLakiNormal[4]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiLakiCukupBurukUnder[4] and tinggi_new[-1] >= tinggiLakiCukupNormalUnder[4]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiLakiBurukUnder[4]:
				pesan_tinggi7()


	# Algoritma penilaian perkembangan balita untuk perempuan
	elif gender_1 == 'Perempuan':
		# Umur sampai 12 bulan
		if totalUmur >= 0 and totalUmur <= 12:
			if berat_new[-1] >= beratPerempuanBurukOver[0]:
				pesan_berat1()
			elif berat_new[-1] >= beratPerempuanCukupBurukOver[0] and berat_new[-1] <= beratPerempuanBurukOver[0]:
				pesan_berat2()
			elif berat_new[-1] >= beratPerempuanCukupNormalOver[0] and berat_new[-1] <= beratPerempuanCukupBurukOver[0]:
				pesan_berat3()
			elif (berat_new[-1] >= beratPerempuanNormal[0] and berat_new[-1] <= beratPerempuanCukupNormalOver[0]) and (berat_new[-1] <= beratPerempuanNormal[0] and berat_new[-1] >= beratPerempuanCukupNormalUnder[0]):
				pesan_berat4()
			elif berat_new[-1] <= beratPerempuanCukupNormalUnder[0] and berat_new[-1] >= beratPerempuanNormal[0]:
				pesan_berat5()
			elif berat_new[-1] <= beratPerempuanCukupBurukUnder[0] and berat_new[-1] >= beratPerempuanCukupNormalUnder[0]:
				pesan_berat6()
			elif berat_new[-1] <= beratPerempuanBurukUnder[0]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiPerempuanBurukOver[0]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiPerempuanCukupBurukOver[0] and tinggi_new[-1] <= tinggiPerempuanBurukOver[0]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiPerempuanCukupNormalOver[0] and tinggi_new[-1] <= tinggiPerempuanCukupBurukOver[0]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiPerempuanNormal[0] and tinggi_new[-1] <= tinggiPerempuanCukupNormalOver[0]) and (tinggi_new[-1] <= tinggiPerempuanNormal[0] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[0]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiPerempuanCukupNormalUnder[0] and tinggi_new[-1] >= tinggiPerempuanNormal[0]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiPerempuanCukupBurukUnder[0] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[0]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiPerempuanBurukUnder[0]:
				pesan_tinggi7()

		# Umur 13 bulan sampai 24 bulan
		elif totalUmur >= 13 and totalUmur <= 24:
			if berat_new[-1] >= beratPerempuanBurukOver[1]:
				pesan_berat1()
			elif berat_new[-1] >= beratPerempuanCukupBurukOver[1] and berat_new[-1] <= beratPerempuanBurukOver[1]:
				pesan_berat2()
			elif berat_new[-1] >= beratPerempuanCukupNormalOver[1] and berat_new[-1] <= beratPerempuanCukupBurukOver[1]:
				pesan_berat3()
			elif (berat_new[-1] >= beratPerempuanNormal[1] and berat_new[-1] <= beratPerempuanCukupNormalOver[1]) and (berat_new[-1] <= beratPerempuanNormal[1] and berat_new[-1] >= beratPerempuanCukupNormalUnder[1]):
				pesan_berat4()
			elif berat_new[-1] <= beratPerempuanCukupNormalUnder[1] and berat_new[-1] >= beratPerempuanNormal[1]:
				pesan_berat5()
			elif berat_new[-1] <= beratPerempuanCukupBurukUnder[1] and berat_new[-1] >= beratPerempuanCukupNormalUnder[1]:
				pesan_berat6()
			elif berat_new[-1] <= beratPerempuanBurukUnder[1]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiPerempuanBurukOver[1]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiPerempuanCukupBurukOver[1] and tinggi_new[-1] <= tinggiPerempuanBurukOver[1]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiPerempuanCukupNormalOver[1] and tinggi_new[-1] <= tinggiPerempuanCukupBurukOver[1]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiPerempuanNormal[1] and tinggi_new[-1] <= tinggiPerempuanCukupNormalOver[1]) and (tinggi_new[-1] <= tinggiPerempuanNormal[1] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[1]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiPerempuanCukupNormal[1] and tinggi_new[-1] >= tinggiPerempuanNormal[1]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiPerempuanCukupBurukUnder[1] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[1]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiPerempuanBurukUnder[1]:
				pesan_tinggi7()

		# Umur 25 bulan sampai 36 bulan
		elif totalUmur >= 25 and totalUmur <= 36:
			if berat_new[-1] >= beratPerempuanBurukOver[2]:
				pesan_berat1()
			elif berat_new[-1] >= beratPerempuanCukupBurukOver[2] and berat_new[-1] <= beratPerempuanBurukOver[2]:
				pesan_berat2()
			elif berat_new[-1] >= beratPerempuanCukupNormalOver[2] and berat_new[-1] <= beratPerempuanCukupBurukOver[2]:
				pesan_berat3()
			elif (berat_new[-1] >= beratPerempuanNormal[2] and berat_new[-1] <= beratPerempuanCukupNormalOver[2]) and (berat_new[-1] <= beratPerempuanNormal[2] and berat_new[-1] >= beratPerempuanCukupNormalUnder[2]):
				pesan_berat4()
			elif berat_new[-1] <= beratPerempuanCukupNormalUnder[2] and berat_new[-1] >= beratPerempuanNormal[2]:
				pesan_berat5()
			elif berat_new[-1] <= beratPerempuanCukupBurukUnder[2] and berat_new[-1] >= beratPerempuanCukupNormalUnder[2]:
				pesan_berat6()
			elif berat_new[-1] <= beratPerempuanBurukUnder[2]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiPerempuanBurukOver[2]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiPerempuanCukupBurukOver[2] and tinggi_new[-1] <= tinggiPerempuanBurukOver[2]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiPerempuanCukupNormalOver[2] and tinggi_new[-1] <= tinggiPerempuanCukupBurukOver[2]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiPerempuanNormal[2] and tinggi_new[-1] <= tinggiPerempuanCukupNormalOver[2]) and (tinggi_new[-1] <= tinggiPerempuanNormal[2] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[2]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiPerempuanCukupNormalUnder[2] and tinggi_new[-1] >= tinggiPerempuanNormal[2]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiPerempuanCukupBurukUnder[2] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[2]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiPerempuanBurukUnder[2]:
				pesan_tinggi7()

		# Umur 37 bulan sampai 48 bulan
		elif totalUmur >= 37 and totalUmur <= 48:
			if berat_new[-1] >= beratPerempuanBurukOver[3]:
				pesan_berat1()
			elif berat_new[-1] >= beratPerempuanCukupBurukOver[3] and berat_new[-1] <= beratPerempuanBurukOver[3]:
				pesan_berat2()
			elif berat_new[-1] >= beratPerempuanCukupNormalOver[3] and berat_new[-1] <= beratPerempuanCukupBurukOver[3]:
				pesan_berat3()
			elif (berat_new[-1] >= beratPerempuanNormal[3] and berat_new[-1] <= beratPerempuanCukupNormalOver[3]) and (berat_new[-1] <= beratPerempuanNormal[3] and berat_new[-1] >= beratPerempuanCukupNormalUnder[3]):
				pesan_berat4()
			elif berat_new[-1] <= beratPerempuanCukupNormalUnder[3] and berat_new[-1] >= beratPerempuanNormal[3]:
				pesan_berat5()
			elif berat_new[-1] <= beratPerempuanCukupBurukUnder[3] and berat_new[-1] >= beratPerempuanCukupNormalUnder[3]:
				pesan_berat6()
			elif berat_new[-1] <= beratPerempuanBurukUnder[3]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiPerempuanBurukOver[3]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiPerempuanCukupBurukOver[3] and tinggi_new[-1] <= tinggiPerempuanBurukOver[3]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiPerempuanCukupNormalOver[3] and tinggi_new[-1] <= tinggiPerempuanCukupBurukOver[3]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiPerempuanNormal[3] and tinggi_new[-1] <= tinggiPerempuanCukupNormalOver[3]) and (tinggi_new[-1] <= tinggiPerempuanNormal[3] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[3]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiPerempuanCukupNormalUnder[3] and tinggi_new[-1] >= tinggiPerempuanNormal[3]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiPerempuanCukupBurukUnder[3] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[3]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiPerempuanBurukUnder[3]:
				pesan_tinggi7()


		# Umur 49 bulan sampai 60 bulan
		elif totalUmur >= 49 and totalUmur <= 60:
			if berat_new[-1] >= beratPerempuanBurukOver[4]:
				pesan_berat1()
			elif berat_new[-1] >= beratPerempuanCukupBurukOver[4] and berat_new[-1] <= beratPerempuanBurukOver[4]:
				pesan_berat2()
			elif berat_new[-1] >= beratPerempuanCukupNormalOver[4] and berat_new[-1] <= beratPerempuanCukupBurukOver[4]:
				pesan_berat3()
			elif (berat_new[-1] >= beratPerempuanNormal[4] and berat_new[-1] <= beratPerempuanCukupNormalOver[4]) and (berat_new[-1] <= beratPerempuanNormal[4] and berat_new[-1] >= beratPerempuanCukupNormalUnder[4]):
				pesan_berat4()
			elif berat_new[-1] <= beratPerempuanCukupNormalUnder[4] and berat_new[-1] >= beratPerempuanNormal[4]:
				pesan_berat5()
			elif berat_new[-1] <= beratPerempuanCukupBurukUnder[4] and berat_new[-1] >= beratPerempuanCukupNormalUnder[4]:
				pesan_berat6()
			elif berat_new[-1] <= beratPerempuanBurukUnder[4]:
				pesan_berat7()

			if tinggi_new[-1] >= tinggiPerempuanBurukOver[4]:
				pesan_tinggi1()
			elif tinggi_new[-1] >= tinggiPerempuanCukupBurukOver[4] and tinggi_new[-1] <= tinggiPerempuanBurukOver[4]:
				pesan_tinggi2()
			elif tinggi_new[-1] >= tinggiPerempuanCukupNormalOver[4] and tinggi_new[-1] <= tinggiPerempuanCukupBurukOver[4]:
				pesan_tinggi3()
			elif (tinggi_new[-1] >= tinggiPerempuanNormal[4] and tinggi_new[-1] <= tinggiPerempuanCukupNormalOver[4]) and (tinggi_new[-1] <= tinggiPerempuanNormal[4] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[4]):
				pesan_tinggi4()
			elif tinggi_new[-1] <= tinggiPerempuanCukupNormalUnder[4] and tinggi_new[-1] >= tinggiPerempuanNormal[4]:
				pesan_tinggi5()
			elif tinggi_new[-1] <= tinggiPerempuanCukupBurukUnder[4] and tinggi_new[-1] >= tinggiPerempuanCukupNormalUnder[4]:
				pesan_tinggi6()
			elif tinggi_new[-1] <= tinggiPerempuanBurukUnder[4]:
				pesan_tinggi7()

	ax1.plot(batasUmur, beratPerempuanNormal, 'g-o')
	ax1.plot(batasUmur, beratPerempuanCukupNormalOver, 'g-o')
	ax1.plot(batasUmur, beratPerempuanCukupNormalUnder, 'g-o')
	ax1.plot(batasUmur, beratPerempuanCukupBurukOver, 'b-o')
	ax1.plot(batasUmur, beratPerempuanCukupBurukUnder, 'b-o')
	ax1.plot(batasUmur, beratPerempuanBurukOver, 'y-o')
	ax1.plot(batasUmur, beratPerempuanBurukUnder, 'y-o')
	ax1.plot(umurUkur, berat_new, 'r-o')

	ax2.plot(batasUmur, tinggiPerempuanNormal, 'g-o')
	ax2.plot(batasUmur, tinggiPerempuanCukupNormalOver, 'g-o')
	ax2.plot(batasUmur, tinggiPerempuanCukupNormalUnder, 'g-o')
	ax2.plot(batasUmur, tinggiPerempuanCukupBurukOver, 'b-o')
	ax2.plot(batasUmur, tinggiPerempuanCukupBurukUnder, 'b-o')
	ax2.plot(batasUmur, tinggiPerempuanBurukOver, 'y-o')
	ax2.plot(batasUmur, tinggiPerempuanBurukUnder, 'y-o')
	ax2.plot(umurUkur, tinggi_new, 'r-o')

	ax1.set_xlabel('Umur')
	ax1.set_ylabel('Berat')
	ax1.grid()

	ax2.set_xlabel('Umur')
	ax2.set_ylabel('Tinggi')
	ax2.grid()

	plt.show()

	
def convert_data():
	conn = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'stm')
	query = "SELECT * FROM graph WHERE id = {}".format(ID_vr.get())
	read_SQL = pd.read_sql_query(query, conn)
	df = pd.DataFrame(read_SQL, columns = ['nama', 'pengukuran', 'tanggal', 'berat', 'tinggi'])
	
	file_path = filedialog.asksaveasfilename(defaultextension = '.xlsx')
	df.to_excel(file_path, index = False, header = True)
	conn.close()
	
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Title = Label(Window2, font =  ('arial', 20, 'bold'), text = 'PENGUKURAN TINGGI DAN BERAT BALITA', fg = 'black', bg = 'blue' , bd = 10)
Title.pack(side = TOP, fill = X)

Data_Frame = Frame(Window2, bd = 4, relief = RIDGE, bg = 'yellow')
Data_Frame.place(x = 0, y = 120, width = 550, height = 540)

#============Membuat Judul Frame Data==========
lbl_title1 = Label(Data_Frame, text = 'Manage Data', bg = 'yellow' , fg = 'red' ,font = ('arial', 16, 'bold'))
lbl_title1.grid(row = 0, column = 0, padx = 220, pady = 0, sticky = 'w')

#============Membuat Label - No. Registrasi==========
lbl_search = Label(Data_Frame, text = 'No. Registrasi', bg = 'yellow', fg = 'black', font = ('arial', 12))
lbl_search.grid(row = 1 , column = 0, padx = 10, pady = 10, sticky = 'w')

#===========Membuat ID Entry================
txt_ID = Entry(Data_Frame, textvariable = ID_vr, font = ('arial', 11))
txt_ID.grid(row = 1, column = 0, padx = 180, pady = 10, ipadx = 80)

#============Membuat Label - Nama==========
lbl_ID = Label(Data_Frame, text = 'Nama', bg = 'yellow', fg = 'black', font = ('arial', 12))
lbl_ID.grid(row = 2 , column = 0, padx = 10, pady = 0, sticky = 'w',)

#===========Membuat Nama Entry================
txt_ID = Entry(Data_Frame, textvariable = Nama, font = ('arial', 11))
txt_ID.grid(row = 2, column = 0, padx = 180, pady = 0, ipadx = 80)

#============Membuat Label - Jenis Kelamin==========
lbl_Gender = Label(Data_Frame, text = 'Jenis Kelamin', bg = 'yellow', fg = 'black', font = ('arial', 12))
lbl_Gender.grid(row = 3 , column = 0, padx = 10, pady = 5, sticky = 'w',)

#============Membuat Combo Box - Jenis Kelamin=================
combo_Gender = ttk.Combobox(Data_Frame, textvariable = Jenis_Kelamin, font = ('arial', 10))
combo_Gender['values'] = ('Laki-Laki', 'Perempuan')
combo_Gender.grid(row = 3, column = 0, padx = 10, pady = 0, ipadx = 80)

#============Membuat Label - TTL==========
lbl_TTL = Label(Data_Frame, text = 'Tempat / Tanggal Lahir', bg = 'yellow', fg = 'black', font = ('arial', 12))
lbl_TTL.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'w',)

#============Membuat Box Frame - Tempat Lahir=============
box_Frame1 = Frame(Data_Frame, bg = 'yellow')
box_Frame1.place(x = 180, y = 145, width = 120, height = 30)

#===========Membuat Entry Tempat Lahir================
txt_Tempat = Entry(box_Frame1, textvariable = Tempat_Lahir, font = ('arial', 11))
txt_Tempat.grid(row = 4, column = 0, padx = 0, pady = 0, ipadx = 120)

#============Membuat Box Frame - Tanggal Lahir=============
box_Frame2 = Frame(Data_Frame, bg = 'yellow')
box_Frame2.place(x = 310, y = 145, width = 193, height = 30)

#===========Membuat Entry Tanggal Lahir================
txt_Tempat = Entry(box_Frame2, textvariable = Tanggal_Lahir, font = ('arial', 11))
txt_Tempat.grid(row = 4, column = 0, padx = 0, pady = 0, ipadx = 193)

#============Membuat Label - Anak ke-berapa==========
lbl_Anak = Label(Data_Frame, text = 'Anak Ke- (Angka)', bg = 'yellow', fg = 'black', font = ('arial', 12))
lbl_Anak.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = 'w',)

#===========Membuat Entry - Anak ke-berapa================
txt_Anak = Entry(Data_Frame, textvariable = Anak_Ke, font = ('arial', 11))
txt_Anak.grid(row = 5, column = 0, padx = 180, pady = 10, ipadx = 80)

#============Membuat Label - Nama Ayah==========
lbl_Ayah = Label(Data_Frame, text = 'Nama Ayah', bg = 'yellow', fg = 'black', font = ('arial', 12))
lbl_Ayah.grid(row = 6 , column = 0, padx = 10, pady = 10, sticky = 'w',)

#===========Membuat Entry - Nama Ayah================
txt_Ayah = Entry(Data_Frame, textvariable = Nama_Ayah, font = ('arial', 11))
txt_Ayah.grid(row = 6, column = 0, padx = 180, pady = 10, ipadx = 80)

#============Membuat Label - Nama Ibu==========
lbl_Ibu = Label(Data_Frame, text = 'Nama Ibu', bg = 'yellow', fg = 'black', font = ('arial', 12))
lbl_Ibu.grid(row = 7 , column = 0, padx = 10, pady = 10, sticky = 'w',)

#===========Membuat Box - Nama Ibu================
txt_Ibu = Entry(Data_Frame, textvariable = Nama_Ibu, font = ('arial', 11))
txt_Ibu.grid(row = 7, column = 0, padx = 180, pady = 10, ipadx = 80)

#=============Membuat Label - Alamat===================
lbl_Alamat = Label(Data_Frame, text = 'Alamat\n\n' , bg = 'yellow' , fg = 'black' , font =('arial', 12))
lbl_Alamat.grid(row = 8 , column = 0 , padx = 10, pady = 10 , sticky = 'w')

#=============Membuat Entry - Alamat====================
txt_Alamat = Text(Data_Frame, width = 20 , height = 4 , font = ('', 11))
txt_Alamat.grid(row = 8 , column = 0 , padx = 180 , pady = 10 , ipadx = 80 , ipady = 5)

#===============Membuat Frame Tombol===========
btn_Frame2 = Frame(Data_Frame, bg = 'yellow')
btn_Frame2.place(x = 120, y = 490, width = 400, height = 35)
	
#================Membuat Tombol Navigasi=============

Newbtn = Button(btn_Frame2, text = 'New', width = 10, command = add_balita).grid(row = 0, column = 0, padx = 5, pady = 2)
Updatebtn = Button(btn_Frame2, text = 'Update', width = 10, command = update_data).grid(row = 0, column = 2, padx = 5, pady = 2)
Clearbtn = Button(btn_Frame2, text = 'Clear', width = 10, command = clear).grid(row = 0, column = 4, padx = 5, pady = 2)
Delbtn = Button(btn_Frame2, text = 'Delete', width = 10, command = delete_data).grid(row = 0, column = 6, padx = 5, pady = 2)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#============Membuat Frame Tabel==============================
Table_Frame = Frame(Window2, bd = 4, relief = RIDGE, bg = 'yellow')
Table_Frame.place(x = 600, y = 120, width = 750, height = 540)

#==============Membuat Judul Frame Data Tabel======================
lbl_title2 = Label(Table_Frame , text = 'Data List' , bg = 'yellow' , fg = 'red' , font = ('arial', 16 , 'bold'))
lbl_title2.grid(row = 0 , column = 2 , padx = 20, pady = 0, sticky = 'w')
	
#===================Membuat Label Searh==========
lbl_search = Label(Table_Frame, text = 'Search By', bg = 'yellow', fg = 'black', font = ('arial', 12))
lbl_search.grid(row = 1, column = 0, padx = 10, pady = 0, sticky = 'w' )
	
#=================Membuat Searching Option=================
combo_Search2 = ttk.Combobox(Table_Frame, textvariable = searchBy, width = 10, font =('arial', 13), state = 'readonly')
combo_Search2['values'] = ('ID', 'Nama', 'Nama Ibu')
combo_Search2.grid(row = 1, column = 1, padx = 10, pady = 0, sticky = 'w')
	
#================Membuat Search Engine============
txt_Search2 = Entry(Table_Frame, textvariable = searchTxt, font = ('arial', 12), bd = 2)
txt_Search2.grid(row = 1, column = 2, padx = 10, pady = 0, sticky = 'w')
	
#================Membuat Search Button===============
search_Button2 = Button(Table_Frame, text = 'Seach', width = 10, command = search_data).grid(row = 1, column = 3, padx = 10, pady = 0, sticky ='w')
	
#================Membuat Show All Button================
showall_Button = Button(Table_Frame, text = 'Show All', width = 10, command = fetch_data).grid(row = 1, column = 4, padx = 10, pady = 0, sticky = 'w')
	
#================Membuat Tombol untuk Pengukuran================
measureBtn = Button(Table_Frame, text = 'Measurement', width = 10, command = lambda : raise_frame(Window3)).grid(row = 4, column = 4, padx = 50, ipadx = 20 , pady = 440, sticky = 'e')
	
#=============Membuat Frame Data Tabel=========================
data_Frame = Frame(Table_Frame , bd = 4 , relief = RIDGE , bg = 'yellow') 
data_Frame.place(x = 10 , y = 60 , width = 725 , height = 420)

#=============Membuat Tabel===============
scroll_x = Scrollbar(data_Frame, orient = HORIZONTAL)
scroll_y = Scrollbar(data_Frame, orient = VERTICAL)
baby_Table = ttk.Treeview(data_Frame, column = ('ID', 'Nama', 'Jenis Kelamin', 'Tempat Lahir', 'Tanggal Lahir', 'Anak Ke-' , 'Nama Ayah' , 'Nama Ibu' , 'Alamat'), xscrollcommand = scroll_x.set , yscrollcommand = scroll_y.set)
scroll_x.pack(side = BOTTOM , fill = X)
scroll_y.pack(side = RIGHT, fill = Y)
scroll_x.config(command = baby_Table.xview)
scroll_y.config(command = baby_Table.yview)
baby_Table.heading('ID', text = 'ID')
baby_Table.heading('Nama', text = 'Nama')
baby_Table.heading('Jenis Kelamin' , text = 'Jenis Kelamin')
baby_Table.heading('Tempat Lahir', text = 'Tempat Lahir')
baby_Table.heading('Tanggal Lahir' , text = 'Tanggal Lahir')
baby_Table.heading('Anak Ke-', text = 'Anak Ke-')
baby_Table.heading('Nama Ayah', text = 'Nama Ayah')
baby_Table.heading('Nama Ibu', text = 'Nama Ibu')
baby_Table.heading('Alamat', text = 'Alamat')
baby_Table['show'] = 'headings'
baby_Table.column('ID', width = 50)
baby_Table.column('Nama', width = 150)
baby_Table.column('Jenis Kelamin', width = 150)
baby_Table.column('Tempat Lahir', width = 150)
baby_Table.column('Tanggal Lahir', width = 150)
baby_Table.column('Anak Ke-', width = 150)
baby_Table.column('Nama Ayah', width = 150)
baby_Table.column('Nama Ibu', width = 150)
baby_Table.column('Alamat', width = 150)
baby_Table.pack(fill = BOTH, expand = 1)
fetch_data()
baby_Table.bind('<ButtonRelease-1>', get_cursor)

#===========================================================
exitBtn = Button(Window2, font = ('times new roman', 12), text = 'EXIT', width = 15, fg = 'white', bg = 'black', command = lambda : raise_frame(Window1)).place(x = 620, y = 615)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Title2 = Label(Window3, font =  ('arial', 20, 'bold'), text = 'MEASUREMENT', fg = 'black', bg = 'blue' , bd = 10).pack(side = TOP, fill = X)

#======================================================================
	
measureFrame = Frame(Window3, bg = '#666699')
measureFrame.place(x = 0, y = 54, width = 1200, height = 600)
	
#===================================================================

portLabel = Label(Window3, font = ('times new roman', 12, 'bold'), text = 'PORT', bg = '#666699').place(x = 1050, y = 55)
portCombo = ttk.Combobox(Window3, font = ('calibri', 10), values = serial_ports(), width = 25)
portCombo.place(x = 1100, y = 55)
portCombo.bind('<<ComboboxSelected>>', on_select)

#==============================================================================

calibrateBtn = Button(Window3, font = ('times new roman', 12), text = 'MEASURE', width = '15').place(x = 150, y = 100)
saveBtn = Button(Window3, font = ('times new roman', 12), text = 'SAVE', width = '15', command = save_data).place(x = 400, y = 100)
delBtn = Button(Window3, font = ('times new roman', 12), text = 'DELETE', width = '15', command = delete_data2).place(x = 650, y = 100)
editBtn = Button(Window3, font = ('times new roman', 12), text = 'EDIT', width = '15', command = edit_data).place(x = 900, y = 100)
	
#===========================================================================

labelCount = Label(measureFrame, font = ('arial', 16), text = 'Pengukuran Ke-', fg = 'black', bg = '#666699').place(x = 100, y = 170)
labelDate = Label(measureFrame, font = ('arial', 16), text = 'Tanggal', fg = 'black', bg = '#666699').place(x = 100, y = 210)
	
countMeasure = Entry(measureFrame, font = ('arial', 16), textvariable = pengukuranKe).place(x = 280, y = 170)
dateMeasure = Entry(measureFrame, font = ('arial', 16), textvariable = tanggalUkur).place(x = 280, y = 210)
	
labelHeight = Label(measureFrame, font = ('arial', 18, 'bold'), text = 'TINGGI', fg = 'black', bg = '#666699').place(x = 650, y = 150)
	
labelWeight = Label(measureFrame, font = ('arial', 18, 'bold'), text = 'BERAT', fg = 'black', bg = '#666699').place(x = 654, y = 210)

heightMeasure = Entry(measureFrame, font = ('arial', 20, 'bold'), textvariable = Tinggi)
heightMeasure.place(x = 760, y = 140, width = 200, height = 50)

weightMeasure = Entry(measureFrame, font = ('arial', 20, 'bold'), textvariable = Berat)
weightMeasure.place(x = 760, y = 205, width = 200, height = 50)

cmUnit = Label(measureFrame, font = ('arial', 18, 'bold'), text = 'cm', fg = 'black', bg = '#666699').place(x = 980, y = 150)
kgUnit = Label(measureFrame, font = ('arial', 18, 'bold'), text = 'kg', fg = 'black', bg = '#666699').place(x = 980, y = 210)

getData = Button(measureFrame, font = ('times new roman', 12), text = 'GET', width = '10', command = pause).place(x = 1040, y = 180)

#====================================================================================

#======================================================================================================

outputFrame = Frame(Window3, bg = '#666699').place(x = 0, y = 320, width = 1200, height = 350)

#===================================================================

regisLabel = Label(Window3, font = ('arial', 12), text = 'No. Registrasi', bg = '#666699').place(x = 20, y = 340)
regisEntry = Entry(Window3, font = ('arial', 12), width = 30, textvariable = ID_vr).place(x = 150, y = 340)
		
nameLabel = Label(Window3, font = ('arial', 12), text = 'Nama', bg = '#666699').place(x = 20, y = 370)
nameEntry = Entry(Window3, font = ('arial', 12), width = 30, textvariable = Nama).place(x = 150, y = 370)
	
jenisLabel = Label(Window3, font = ('arial', 12), text = 'Jenis Kelamin', bg = '#666699').place(x = 20, y = 400)
jenisEntry = Entry(Window3, font = ('arial', 12), width = 30, textvariable = Jenis_Kelamin).place(x = 150, y = 400)
	
tempat_lahirLabel = Label(Window3, font = ('arial', 12), text = 'Tempat Lahir', bg = '#666699').place(x = 20, y = 430)
tempat_lahirEntry = Entry(Window3, font = ('arial', 12), width = 30, textvariable = Tempat_Lahir).place(x = 150, y = 430)

tanggal_lahirLabel = Label(Window3, font = ('arial', 12), text = 'Tanggal Lahir', bg = '#666699').place(x = 20, y = 460)
tanggal_lahirEntry = Entry(Window3, font = ('arial', 12), width = 30, textvariable = Tanggal_Lahir).place(x = 150, y = 460)
		
nama_ibuLabel = Label(Window3, font = ('arial', 12), text = 'Nama Ibu', bg = '#666699').place(x = 20 ,y = 490)
nama_ibuEntry = Entry(Window3, font = ('arial', 12), width = 30, textvariable = Nama_Ibu).place(x = 150, y = 490)
		
#=============================================================================
		
tabelFrame = Frame(Window3, bd = 4, relief = RIDGE, bg = 'white')
tabelFrame.place(x = 460, y = 340, height = 280, width = 820)

#=============================================================================

columns = ('ID', 'Nama', 'Pengukuran Ke-','Terakhir Mengukur', 'Berat', 'Tinggi', 'Jenis Kelamin')

Xscroll = Scrollbar(tabelFrame, orient = HORIZONTAL)
Yscroll = Scrollbar(tabelFrame, orient = VERTICAL)
tabelUkur = ttk.Treeview(tabelFrame, column = columns, xscrollcommand = Xscroll.set, yscrollcommand = Yscroll.set)
Xscroll.pack(side = BOTTOM, fill = X)
Yscroll.pack(side = RIGHT, fill = Y)
Xscroll.config(command = tabelUkur.xview)
Yscroll.config(command = tabelUkur.yview)

for col in columns:
	tabelUkur.heading(col, text = col, command = lambda _col = col : sort_column(tabelUkur, _col, False))

tabelUkur['show'] = 'headings'
tabelUkur.column('ID', width = 20)
tabelUkur.column('Nama', width = 100)
tabelUkur.column('Pengukuran Ke-', width = 80) 
tabelUkur.column('Terakhir Mengukur', width = 100)
tabelUkur.column('Berat', width = 50)
tabelUkur.column('Tinggi', width = 50)
tabelUkur.column('Jenis Kelamin', width = 50)
tabelUkur.pack(fill = BOTH, expand = 1)
fetch_data2()
tabelUkur.bind('<ButtonRelease-1>', get_cursor2)
	
#================================================================================
backBtn = Button(Window3, font = ('times new roman', 12), text = 'BACK', width = 20, fg = 'white', bg = 'black', command = lambda : raise_frame(Window2)).place(x = 0, y = 645)

graphicBtn = Button(Window3, text = 'Check Graphic', width = 15, command = check_graphics).place(x = 1150, y = 640)

toExcel = Button(Window3, text = 'Convert To Excel', width = 15, command = convert_data).place(x = 950, y = 640)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

raise_frame(Window1)
root.mainloop()