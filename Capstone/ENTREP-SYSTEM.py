# pylint: disable=bad-indentation
from tkinter import*
from tkinter import simpledialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os
from venv import create

class main():
	def __init__(self, root):
		self.root = root
		self.root.title('Food Pandas Canteen System')
		self.root.geometry('1040x500')
		self.root.resizable(0, 0)
		if os.path.exists('items.txt'):
			with open('items.txt', 'r') as file:
				self.data = [[j.strip() for j in i.split(':')] for i in file.readlines()]
		else: raise FileNotFoundError('item.txt not exists!')
		self.menu_frame = Frame(self.root, width=500, height=500)
		self.order_frame = Frame(self.root, width=500, height=500)
		self.menu_scroll = Scrollbar(self.menu_frame, orient=VERTICAL)
		self.order_scroll = Scrollbar(self.order_frame, orient=VERTICAL)
		self.data = [[i[0], float(i[1])] for i in self.data]
		self.title_label = Label(self.root, text='Food Pandas Canteen System', font=("calibri",30, 'bold'))
		self.welcome_label = Label(self.root, text='Welcome, Ateneans!', font=("calibri",15))
		self.description_label = Label(self.root, anchor='e', text = """Select an item from the right panel and press the Add button to add the item in your order. Your orders will appear on the left panel.
To cancel an order, select the order from the left a and click the Remove button. Press the Proceed button to confirm your order.""", font=("calibri",12))
		self.menu_header_text = ['Item', 'Price']
		self.column_names = ("1", '2')
		self.menu = ttk.Treeview(self.menu_frame, column=self.column_names, selectmode='browse', yscrollcommand=self.menu_scroll.set)
		self.menu.column('#0', width=0, minwidth=0, stretch=NO)
		self.menu_scroll.config(command=self.menu.yview)
		for i in self.column_names:
			self.menu.heading(i, text=self.menu_header_text[int(i)-1])
		self.order_header_text = ['Item', 'Subtotal']
		self.order = ttk.Treeview(self.order_frame, column=self.column_names, selectmode='browse', yscrollcommand=self.order_scroll.set)
		self.order.column('#0', width=0, minwidth=0, stretch=NO)
		self.order_scroll.config(command=self.order.yview)
		for i in self.column_names:
			self.order.heading(i, text=self.order_header_text[int(i)-1])
		for i in self.data:
			self.menu.insert('', END, value=[i[0], 'PHP '+format(i[1], '.2f')])
		self.add_button = Button(self.root, text='Add ->', command=self.add_item)
		self.remove_button = Button(self.root, text='<- Remove', command=self.remove_item)
		self.proceed_button = Button(self.root, text='Proceed', command=self.proceed)

	def widget(self):
		self.title_label.place(relx=0.5, y=50, anchor='center')
		self.welcome_label.place(relx=0.5, y=90, anchor='center')
		self.description_label.place(relx=0.5, y=140, anchor='center')
		self.menu_frame.place(x=30, y=200)
		self.order_frame.place(x=1090, y=200, anchor=NE)
		self.menu.place(x=0, y=0)
		self.order.place(x=0, y=0)
		self.root.update()
		self.menu_scroll.place(x=403, y=0, height=self.menu.winfo_height())
		self.order_scroll.place(x=403, y=0, height=self.order.winfo_height())
		self.add_button.place(relx=0.5, y=250, width=100, anchor='center')
		self.remove_button.place(relx=0.5, y=310, width=100, anchor='center')
		self.proceed_button.place(relx=0.5, y=370, width=100, anchor='center')

	def add_item(self):
		if not self.menu.focus():
			messagebox.showerror('Add Item', 'Please select an item from the left')
			return
		self.cur_item = self.menu.item(self.menu.focus())['values']
		self.amount = simpledialog.askinteger("Add Items","Enter Quantity (1-50)", minvalue=1, maxvalue=50)
		if self.amount:
			self.order.insert('', END, values=[str(self.amount)+' pc(s) '+self.cur_item[0], 'PHP '+str(format(float(self.cur_item[1].replace('PHP ', ''))*self.amount, '.2f'))])

	def remove_item(self):
		if not self.order.selection():
			messagebox.showerror('Remove Order', 'Please select an item from right panel')
			return
		self.order.delete(self.order.selection()[0])

	def proceed(self):
		if not self.order.get_children():
			messagebox.showerror('Confirm Order', 'No orders taken yet. Please take at least one order')
			return
		self.proceed = messagebox.askyesno('Confirm Order', 'Confirm Order?')
		if self.proceed:
			self.show_total_and_discount()
		else:
			return

	def show_total_and_discount(self):
		self.total_amount = sum([float(self.order.item(i)['values'][1].replace('PHP ', '')) for i in self.order.get_children()])
		self.discount_content = ['None', 'Senior (20%)', 'Admin and Personnels (30%)']
		self.discount_text = 'Total cost is PHP {}\n\nPlease enter which discount code applies:{}\n'.format(format(self.total_amount, '.2f'), ''.join(['\n['+str(i)+'] '+self.discount_content[i] for i in range(len(self.discount_content))]))
		self.discount_code = simpledialog.askinteger('Discount', self.discount_text, minvalue=0, maxvalue=2)
		if self.discount_code != None:
			self.mode_of_payment()

	def mode_of_payment(self):
		self.total_amount = sum([float(self.order.item(i)['values'][1].replace('PHP ', '')) for i in self.order.get_children()])
		self.mode_content = ['Pay In-Cash', 'G-Cash', 'Paymaya']
		self.mode_text = 'Total cost is PHP {}\n\nPlease enter mode of payment:{}\n'.format(format(self.total_amount, '.2f'), ''.join(['\n['+str(i)+'] '+self.mode_content[i] for i in range(len(self.mode_content))]))
		self.mode_code = simpledialog.askinteger('Mode of Payment', self.mode_text, minvalue=0, maxvalue=2)
		if self.mode_code == 1:
			self.account_number()
		elif self.mode_code == 2:
			self.account_number()
		else:
			self.pay(self.discount_code, self.total_amount)

	def account_number(self):
		self.number_text = 'Please input your account (+63):'
		self.number_code = simpledialog.askinteger("Account Number", self.number_text)
		if self.number_code != None:
			self.pay(self.discount_code, self.total_amount)
            
	def pay(self, discount_code, total_amount):
		self.discount = 80 if self.discount_code == 1 else 70 if self.discount_code == 2 else 100
		self.real_amount = total_amount * self.discount / 100
		self.discount_amount = self.total_amount - self.real_amount
		self.paid_money = simpledialog.askinteger('Payment', 'You need to pay PHP {}\nPlease enter your payment:'.format(format(self.real_amount, '.2f')))
		if not self.paid_money:
			messagebox.showerror('Error', 'No payment was given! You need to pay PHP {}'.format(format(self.real_amount, '.2f')))
			self.pay(discount_code, total_amount)
			return
		elif self.paid_money < self.real_amount:
			messagebox.showerror('Error', 'Payment is insuffecient! You need to pay PHP {}'.format(format(self.real_amount, '.2f')))
			self.pay(discount_code, total_amount)

		self.schedule(self.total_amount)
    
	def schedule(self, total_amount):
		self.real_amount = total_amount * self.discount / 100
		self.discount_amount = self.total_amount - self.real_amount
		self.schedule_content = ['10:00 AM - 10:20 AM', '11:20 AM - 11:50 AM', '12:20 PM - 12:50 PM', '1:50 PM - 2:10 PM', '2:50 PM - 3:10 PM',]
		self.schedule_text = 'Total cost is PHP {}\n\nPlease enter which time code applies:{}\n'.format(format(self.real_amount, '.2f'), ''.join(['\n['+str(i)+'] '+self.schedule_content[i] for i in range(len(self.schedule_content))]))
		self.schedule_code = simpledialog.askinteger('Pick-up Time',self.schedule_text, minvalue = 0, maxvalue = 4)
		if self.schedule_code != None:
			self.show_receipt(self.discount_code, self.total_amount, self.real_amount, self.paid_money, self.mode_code, self.schedule_code, self.number_code)

	def show_receipt(self, discount_code, total_amount, real_amount, paid_money, mode_code, schedule_code, number_code):
		self.receipt_content = []
		self.receipt_content.append('{:^50}'.format('Food Pandas Canteen'))
		self.receipt_content.append('-'*50)
		for i in [self.order.item(i)['values'] for i in self.order.get_children()]:
			self.receipt_content.append(i[0]+' costs '+ i[1])
		self.receipt_content.append('-'*50)
		self.receipt_content.append("Total Cost: PHP {}".format(format(total_amount, '.2f')))
		self.receipt_content.append('Discount: {}'.format(self.discount_content[discount_code]))
		if discount_code != 0:
			self.receipt_content.append('Discounted Price: PHP {}'.format(format(real_amount, '.2f')))
		self.receipt_content.append('Cash Tendered: PHP {}'.format(format(paid_money, '.2f')))
		self.receipt_content.append('Change: PHP {}'.format(format(paid_money-real_amount, '.2f')))
		self.receipt_content.append('Mode of Payment: {}'.format(self.mode_content[mode_code]))
		if mode_code == 1:
			self.receipt_content.append('Account Number: (+63){}'.format(number_code))
		elif mode_code == 2:
			self.receipt_content.append('Account Number: (+63){}'.format(number_code))
		else:
			self.receipt_content.append('Mode of Payment: {}'.format(self.mode_content[mode_code]))
		self.receipt_content.append('Time of Pickup: {}'.format(self.schedule_content[schedule_code]))        
		self.receipt_content.append('-'*50)
		self.receipt_content.append('{:^50}'.format('Thank you for using this facility!'))
		self.receipt_content.append('{:^50}'.format('Come again!'))
		messagebox.showinfo('Receipt', '\n'.join(self.receipt_content))
		self.save_receipt_prompt = messagebox.askyesno('Save Receipt', 'Do you want to save receipt?')
		if self.save_receipt_prompt:
			self.save_receipt(self.receipt_content)
		self.order_items = []
		for i in [self.order.item(i)['values'] for i in self.order.get_children()]:
			self.order_items.append(i[0])
		self.save_order_items(self.order_items)
		self.total_cost = []
		self.total_cost.append(format(total_amount, '.2f'))
		self.save_total_cost (self.total_cost)
		self.mode_of_payment = []
		self.mode_of_payment.append(self.mode_content[mode_code])
		self.save_mode_of_payment(self.mode_of_payment)
		self.time_of_pickup = []
		self.time_of_pickup.append(self.schedule_content[schedule_code])
		self.save_time_of_pickup(self.time_of_pickup)
	
		self.ask_if_again()
	
	def save_receipt(self, receipt_content):
		with open('123.txt', 'w') as file:
			file.write('\n'.join(receipt_content))
	def save_order_items(self, order_items):
		with open('order_items.txt') as file:
			text = file.read()
		with open('order_items.txt', 'a') as file:
			if not text.endswith('\n'):
				file.write('\n')
			file.write('\n'.join(order_items))
	def save_total_cost (self, total_cost):
		with open('total_cost.txt') as file:
			text = file.read()
		with open('total_cost.txt', 'a') as file:
			if not text.endswith('\n'):
				file.write('\n')
			file.write('\n'.join(total_cost))
	def save_mode_of_payment(self, mode_of_payment):
		with open('mode_of_payment.txt') as file:
			text = file.read()
		with open('mode_of_payment.txt', 'a') as file:
			if not text.endswith('\n'):
				file.write('\n')
			file.write('\n'.join(mode_of_payment))
	def save_time_of_pickup(self, time_of_pickup):
		with open('time_of_pickup.txt') as file:
			text = file.read()
		with open('time_of_pickup.txt', 'a') as file:
			if not text.endswith('\n'):
				file.write('\n')
			file.write('\n'.join(time_of_pickup))

	def ask_if_again(self):
		self.again_prompt = messagebox.askyesno('Take Order', 'Thank you for your order! Do you want to use this facility again? Press No to exit this program.')
		if self.again_prompt:
			[self.order.delete(i) for i in self.order.get_children(0)]
		else:
			quit()

	def run(self):
		self.widget()
		self.root.mainloop()

class driver():
	def __init__(self, username, password):
		self.root = Tk()
		self.root.withdraw()
		self.username = simpledialog.askstring('Security Login', 'Enter username:')
		if self.username != username:
			messagebox.showerror('Error', 'Invalid or incorrect username! The program will exit')
			return
		self.password = simpledialog.askstring('Security Login', 'Enter password:', show='*')
		if self.password != password:
			messagebox.showerror('Error', 'Invalid or incorrect password! The program will exit')
			return

		self.root.destroy()

		self.main = main(Tk())
		self.main.run()

app = driver('capstone', 'itmgt25')