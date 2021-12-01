import tkinter as tk
from tkinter import Entry, ttk
import matplotlib.pyplot as plt

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
	print("y = mx + b este " + "y = " + str(m) + " * x + " + str(b))

	def f(x): return m * x + b
	return f

f = sol(input)

for i in input:
	print("x: " + str(i[0]) + " y: " + str(i[1]) + " f(x): " + str(f(i[0])) + " error [f(x) - y]: " + str((f(i[0]) - i[1])))


class Entries:
	entries = dict()
	length = 0
	
	def handle_add_entry(self):
		self.length += 1

		entry1 = ttk.Entry(frame)
		entry2 = ttk.Entry(frame)

		self.entries.update({self.length: {"x": entry1, "y": entry2}})

		entry1.grid(ipady=5,column=0, row = self.length)
		entry2.grid(ipady=5, column=1, row = self.length)

	def handle_delete_entry(self):
	
		if self.length > 0:
			self.entries[self.length]['x'].destroy()
			self.entries[self.length]['y'].destroy()
			self.entries.popitem()

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
			self.length -= 1
   
		tmp_entries = {}

		for i, points in enumerate(self.entries.values()):
			j = i + 1
			tmp_entries[j] = points
		
		self.entries = tmp_entries
		print(self.entries)


if __name__ == "__main__":
	window = tk.Tk(className = 'metoda celor mai mici patrate')
	window.geometry("500x500")
 
	frame = ttk.Frame(master = window, padding = 5)
	frame.grid()

	entries = Entries()
 
	ttk.Label(frame, text="X").grid(column = 0, row = 0)
	ttk.Label(frame, text="Y").grid(column = 1, row = 0)

	ttk.Button(frame, text = "New Entry", padding=5, width=20, command = entries.handle_add_entry).grid(column=2,row=1)
	ttk.Button(frame, text = "Delete Entry", padding=5, width=20, command = entries.handle_delete_entry).grid(column=2,row=2)
	ttk.Button(frame, text="Calculate", padding=5, width=20, command=entries.handle_validate_entries).grid(column=2,row=3)
 
	window.mainloop()

