import requests
import json
from tkinter import *
from tkinter import messagebox,Menu
import sqlite3



pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap('favicon.ico')



con=sqlite3.connect("coin.db")
cursorobj = con.cursor()

cursorobj.execute("CREATE TABLE  IF NOT EXISTS coins(Id INTEGER PRIMARY KEY,Symbol TEXT,price REAL,amount INTEGER)")
con.commit()


def app_nav():
	def clear():
		cursorobj.execute('DELETE FROM coins')
		con.commit()
		reset()
		messagebox.showinfo("Notification","Portfolio Cleared Successfully")

	def close_app():
		pycrypto.destroy()
		
	menu = Menu(pycrypto)
	file_item = Menu(menu)
	file_item.add_command(label = 'Clear Portfolio',command=clear)
	file_item.add_command(label = 'Close App',command=close_app)
	menu.add_cascade(label="File",menu=file_item)
	pycrypto.config(menu=menu)



def reset():
	for frame in pycrypto.winfo_children():
		frame.destroy()

	app_nav()	
	my_portfolio()
	app_header()

def my_portfolio():

	api_request= requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=xxxx')

	api = json.loads(api_request.content)

	# print(api)

	cursorobj.execute('SELECT * FROM coins')
	coins=cursorobj.fetchall()


	def insert_coin():
		cursorobj.execute('INSERT INTO coins(Symbol,price,amount) VALUES(?,?,?)',(symbol_txt.get(),price_txt.get(),amount_txt.get(),))
		con.commit()
		
		reset()
		messagebox.showinfo('Notification','Coin added Successfully!!!')

	def update_coin():
		cursorobj.execute('UPDATE coins SET Symbol=?,price=?,amount=? WHERE Id= ?',(symbol_upd.get(),price_upd.get(),amount_upd.get(),port_id_upd.get()))
		con.commit()
		reset()
		messagebox.showinfo('Notification','Coin Updated Successfully!!!')

	def delete_coin():
		cursorobj.execute('DELETE FROM coins WHERE Id = ?',(port_id_del.get(),))
		con.commit()
		reset()	
		messagebox.showinfo('Notification','Coin Deleted Successfully!!!')			


	def color_option(amount):
		if amount > 0:
			return 'green'
		elif amount == 0:
			return 'black'
		else:
			return 'red'	

	total = 0
	coin_row=1
	total_p_amount=0
	total_c_amount=0
			
	for i in range (0,300):

		a1= api["data"][i]["name"]
		a2 = api["data"][i]["symbol"]
		a3 = api["data"][i]["quote"]['USD']["price"]

		for coin in coins:
			if 	a2 == coin[1]:

				total_amount_paid = coin[3]*coin[2]
				current_worth = coin[3]*a3
				pl_percoin=a3-coin[2]
				profit_or_loss_for_coin = current_worth - total_amount_paid
				total = total + profit_or_loss_for_coin




				name = Label(pycrypto, text= a1,bg = "white",fg = "black",font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				name.grid(row=coin_row,column=0,sticky=N+S+E+W)

				c_price = Label(pycrypto, text= "{0:0.3f}".format(a3),bg = "white",fg = "black",font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				c_price.grid(row=coin_row,column=1,sticky=N+S+E+W)

				port_id = Label(pycrypto, text= coin[0],bg = "white",fg = "black",font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				port_id.grid(row=coin_row,column=2,sticky=N+S+E+W)

				coin_symbol = Label(pycrypto, text= coin[1],bg = "white",fg = "black",font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				coin_symbol.grid(row=coin_row,column=3,sticky=N+S+E+W)

				b_price = Label(pycrypto, text= coin[2],bg = "white",fg = "black",font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				b_price.grid(row=coin_row,column=4,sticky=N+S+E+W)

				number = Label(pycrypto, text=coin[3] ,bg = "white",fg = "black",font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				number.grid(row=coin_row,column=5,sticky=N+S+E+W)

				p_amount = Label(pycrypto, text= "${0:0.3f}".format(total_amount_paid),bg = "white",fg = "black",font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				p_amount.grid(row=coin_row,column=6,sticky=N+S+E+W)

				c_amount = Label(pycrypto, text= "${0:0.3f}".format(current_worth),bg = "white",fg = "black",font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				c_amount.grid(row=coin_row,column=7,sticky=N+S+E+W)

				p_l_per_coin = Label(pycrypto, text= "${0:0.3f}".format(pl_percoin),bg = "white",fg = color_option(pl_percoin),font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				p_l_per_coin.grid(row=coin_row,column=8,sticky=N+S+E+W)

				total_p_l_for_coin = Label(pycrypto, text= "${0:0.3f}".format(profit_or_loss_for_coin),bg = "white",fg = color_option(profit_or_loss_for_coin),font="Lato 10",padx='2',pady='2',borderwidth=2,relief="groove")
				total_p_l_for_coin.grid(row=coin_row,column=9,sticky=N+S+E+W)

				coin_row=coin_row+1
				total_c_amount=total_c_amount+current_worth
				total_p_amount=total_p_amount+total_amount_paid
	# print("Total P/L for the Portfolio - ", "${0:0.3f}".format(total))

	symbol_txt = Entry(pycrypto,borderwidth=2,relief="groove")
	symbol_txt.grid(row=coin_row+1,column=3,sticky=N+S+E+W)

	price_txt = Entry(pycrypto,borderwidth=2,relief="groove")
	price_txt.grid(row=coin_row+1,column=4,sticky=N+S+E+W)	

	amount_txt = Entry(pycrypto,borderwidth=2,relief="groove")
	amount_txt.grid(row=coin_row+1,column=5,sticky=N+S+E+W)	

	symbol_upd = Entry(pycrypto,borderwidth=2,relief="groove")
	symbol_upd.grid(row=coin_row+2,column=3,sticky=N+S+E+W)

	price_upd = Entry(pycrypto,borderwidth=2,relief="groove")
	price_upd.grid(row=coin_row+2,column=4,sticky=N+S+E+W)	

	amount_upd = Entry(pycrypto,borderwidth=2,relief="groove")
	amount_upd.grid(row=coin_row+2,column=5,sticky=N+S+E+W)

	port_id_upd = Entry(pycrypto,borderwidth=2,relief="groove")
	port_id_upd.grid(row=coin_row+2,column=2,sticky=N+S+E+W)

	port_id_del = Entry(pycrypto,borderwidth=2,relief="groove")
	port_id_del.grid(row=coin_row+3,column=2,sticky=N+S+E+W)	

				

	tap = Label(pycrypto, text= "${0:0.3f}".format(total_p_amount),bg = "white",fg = 'black',font="Helvetica 12",padx='2',pady='2',borderwidth=2,relief="groove")
	tap.grid(row=coin_row,column=6,sticky=N+S+E+W)

	tcw = Label(pycrypto, text= "${0:0.3f}".format(total_c_amount),bg = "white",fg = 'black',font="Helvetica 12",padx='2',pady='2',borderwidth=2,relief="groove")
	tcw.grid(row=coin_row,column=7,sticky=N+S+E+W)

	total_p_l = Label(pycrypto, text= "${0:0.3f}".format(total),bg = "white",fg = color_option(total),font="Helvetica 12",padx='2',pady='2',borderwidth=2,relief="groove")
	total_p_l.grid(row=coin_row,column=9,sticky=N+S+E+W)

	api=""

	add_coin = Button(pycrypto, text="Add",command = insert_coin ,bg = "grey",fg ='white',font="Helvetica 12",padx='2',pady='2',borderwidth=2,relief="groove")
	add_coin.grid(row=coin_row+1,column=6,sticky=N+S+E+W)	

	update_coin = Button(pycrypto, text="Update",command = update_coin ,bg = "grey",fg ='white',font="Helvetica 12",padx='2',pady='2',borderwidth=2,relief="groove")
	update_coin.grid(row=coin_row+2,column=1,sticky=N+S+E+W)	

	delete_coin = Button(pycrypto, text="Delete",command = delete_coin ,bg = "grey",fg ='white',font="Helvetica 12",padx='2',pady='2',borderwidth=2,relief="groove")
	delete_coin.grid(row=coin_row+3,column=1,sticky=N+S+E+W)			

	refresh = Button(pycrypto, text="Refresh",command = reset ,bg = "grey",fg ='white',font="Helvetica 12",padx='2',pady='2',borderwidth=2,relief="groove")
	refresh.grid(row=coin_row+1,column=9,sticky=N+S+E+W)



def app_header():




	name = Label(pycrypto, text= "Coin Name",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	name.grid(row=0,column=0,sticky=N+S+E+W)

	c_price = Label(pycrypto, text= "Current Price",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	c_price.grid(row=0,column=1,sticky=N+S+E+W)

	portfolio_id = Label(pycrypto, text= "Portfolio Id",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	portfolio_id.grid(row=0,column=2,sticky=N+S+E+W)

	symbol = Label(pycrypto, text= "Symbol",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	symbol.grid(row=0,column=3,sticky=N+S+E+W)

	b_price = Label(pycrypto, text= "Bought Price",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	b_price.grid(row=0,column=4,sticky=N+S+E+W)

	number = Label(pycrypto, text= "Number of Coins",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	number.grid(row=0,column=5,sticky=N+S+E+W)

	p_amount = Label(pycrypto, text= "Total amount paid",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	p_amount.grid(row=0,column=6,sticky=N+S+E+W)

	c_amount = Label(pycrypto, text= "Current worth",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	c_amount.grid(row=0,column=7,sticky=N+S+E+W)

	p_l_per_coin = Label(pycrypto, text= "P/L per coin",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	p_l_per_coin.grid(row=0,column=8,sticky=N+S+E+W)

	total_p_l = Label(pycrypto, text= "Total P/L for coin",bg = "#2F4F4F",fg ="white",font="Helvetica 12",padx='5',pady='5',borderwidth=2,relief="groove")
	total_p_l.grid(row=0,column=9,sticky=N+S+E+W)


app_nav()
app_header()
my_portfolio()



# cursorobj.close()
# con.close()
pycrypto.mainloop()
cursorobj.close()
con.close()
print("My Crypto Portfolio interrupted")
