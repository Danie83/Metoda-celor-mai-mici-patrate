import tkinter as tk
from tkinter import Entry, ttk, messagebox, filedialog
from tkinter.constants import W
import matplotlib.pyplot as plt
import os

global window
global frame

input = [[2,4], [3,5], [5,7], [7,10], [9,15]]

def sol(input):
	xpatrat = []
	xy = []
	for i in input:
		xpatrat.append(i[0] * i[0])
		xy.append(i[0] * i[1])
	sumx = sum(i[0] for i in input)
	sumy = sum(i[1] for i in input)
	sumxpatrat = sum(i for i in xpatrat)
	sumxy = sum(i for i in xy)
	
	n = len(input)
	m = (n * sumxy - sumx * sumy) / (n * sumxpatrat - sumx * sumx)
	b = (sumy - m * sumx) / n
	result = "y = mx + b equals to y = {m} * x + {b}".format(m = str(m), b = str(b))
	#print("y = mx + b este " + "y = " + str(m) + " * x + " + str(b))
	print(result)

	def f(x): return m * x + b
	return f

f = sol(input)

for i in input:
	point = "x: {i0} y: {i1} f(x) = {fi0} error [f(x) - y]: {error}".format(i0 = str(i[0]), 
																		i1 = str(i[1]),
																		fi0 = str(f(i[0])),
																		error = str((f(i[0]) - i[1])))
	print(point)
	#print("x: " + str(i[0]) + " y: " + str(i[1]) + " f(x): " + str(f(i[0])) + " error [f(x) - y]: " + str((f(i[0]) - i[1])))


class Entries:
	entries = dict()
	length = 0
	
	def handle_add_entry(self):
		if self.length < 11:
			self.length += 1

			entry1 = ttk.Entry(frame)
			entry2 = ttk.Entry(frame)

			self.entries.update({self.length: {"x": entry1, "y": entry2}})

			entry1.grid(ipady=5,column=0, row = self.length)
			entry2.grid(ipady=5, column=1, row = self.length)
		else:
			messagebox.showerror("Add entry error [1]", "Can't have more than 11 entries")
		

	def handle_delete_entry(self):
		try:
			if self.length > 0:
				self.entries[self.length]['x'].grid_forget()
				self.entries[self.length]['y'].grid_forget()
				self.entries.popitem()
				self.length -= 1
			elif self.length == 0:
				messagebox.showerror("Delete entry error [2]", "You don't have any entry to delete")
		except KeyError:
			self.length -= 1
   
	

	def handle_validate_entries(self):
		to_delete = []
		for i,points in enumerate(self.entries.values()):
			j = i + 1
			try:
				check = True if float(points.get("x").get()) and float(points.get("y").get()) else False
			except ValueError:
				check = False
			if check == False:
				to_delete.append(j)
		
		for k in to_delete:
			self.entries[k]['x'].grid_forget()
			self.entries[k]['y'].grid_forget()
			self.entries.pop(k)

		tmp_entries = {}

		for i, points in enumerate(self.entries.values()):
			j = i + 1
			tmp_entries[j] = points
		
		while self.length > 0:
			self.handle_delete_entry()
   
		self.entries = tmp_entries
  
		self.length = 0

		for points in self.entries.values():
			self.length += 1

			entry1 = ttk.Entry(frame)
			entry2 = ttk.Entry(frame)

			entry1.grid(ipady=5,column=0, row = self.length)
			entry1.insert(0,points['x'].get())
			
			entry2.grid(ipady=5, column=1, row = self.length)
			entry2.insert(0,points['y'].get())	
	
	def validate_single_entry(self, point):
		try:
			check = True if float(point[0]) and float(point[1]) else False
		except ValueError:
			check = False
		return check

	# https://pythonguides.com/python-tkinter-save-text-to-file/
	def handle_load_entries(self):
    
		while self.length > 0:
			self.handle_delete_entry()
   
		files = [('Text Files', '*.txt')]
		file_to_open = filedialog.askopenfilename(initialdir="", title="Select your file", filetypes=files, defaultextension= files)
  
		self.length = 0
    
		try:
			file = open(file_to_open, 'r')
			lines = file.readlines()
   
			for line in lines:
				line = line.strip("\n")
				point = line.split(" ")
				
				if self.validate_single_entry(point) == True:
					self.length += 1
					entry1 = ttk.Entry(frame)
					entry2 = ttk.Entry(frame)

					entry1.grid(ipady=5,column=0, row = self.length)
					entry1.insert(0,point[0])
					
					entry2.grid(ipady=5, column=1, row = self.length)
					entry2.insert(0,point[1])
     
					self.entries.update({self.length: {"x": entry1, "y": entry2}})
		except FileNotFoundError:
			messagebox.showerror("Load entries error [3]","File not found")
   
	def handle_save_entries(self):
		files = [('Text Files', '*.txt')]
		# Type of file is TextIOWrapper and not the actual path of the file
		file = filedialog.asksaveasfile(title="Save your file", filetypes= files, defaultextension= files)

		file_to_save_to = file.name
		with open(file_to_save_to, "w") as f:
			for point in self.entries.values():
				content = "{x} {y}\n".format(x = point.get("x").get(), y = point.get("y").get())
				f.write(content)


	def handle_draw_plot(self):
		plt.plot([1,2,3,4])
		plt.ylabel('Y values')
		plt.xlabel('X values')
		plt.show()

	def handle_validate_entries_and_draw_plot(self):
		self.handle_validate_entries()
		self.handle_draw_plot()

if __name__ == "__main__":
	window = tk.Tk(className = 'metoda celor mai mici patrate')
	window.geometry("400x400")
 
	frame = ttk.Frame(window, padding = 5)
	frame.grid()

	entries = Entries()
 
	entries.handle_add_entry()
 
	ttk.Label(frame, text="X").grid(column = 0, row = 0)
	ttk.Label(frame, text="Y").grid(column = 1, row = 0)

	ttk.Button(frame, text = "New Entry", padding=5, width=20, command = entries.handle_add_entry).grid(column=2,row=1)
	ttk.Button(frame, text = "Delete Entry", padding=5, width=20, command = entries.handle_delete_entry).grid(column=2,row=2)
	ttk.Button(frame, text = "Load Entries", padding=5, width=20, command = entries.handle_load_entries).grid(column=2, row=3)
	ttk.Button(frame, text = "Save Entries", padding=5, width=20, command = entries.handle_save_entries).grid(column=2, row=4)
	ttk.Button(frame, text = "Calculate", padding=5, width=20, command=entries.handle_validate_entries_and_draw_plot).grid(column=2,row=5)
 
	window.mainloop()

