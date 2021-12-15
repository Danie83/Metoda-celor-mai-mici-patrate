import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import matplotlib.pyplot as plt


global window
global frame

class Entries:
	def __init__(self):
		self.entries = dict()
		self.length = 0
	
	def handle_add_entry(self):
		if self.length < 24:
			self.length += 1

			entry1 = ttk.Entry(frame)
			entry2 = ttk.Entry(frame)

			self.entries.update({self.length: {"x": entry1, "y": entry2}})

			entry1.grid(ipady=5, column=0, row = self.length)
			entry2.grid(ipady=5, column=1, row = self.length)
   
			return True
		else:
			messagebox.showerror("Add entry error [1]", "Can't have more than 24 entries")
			return False
		
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
		duplicates = []
		check = False
		for position, points in enumerate(self.entries.values()):
			delete_candidate = position + 1
			try:
				if float(points.get("x").get()) and float(points.get("y").get()):
					check = True
				if check == True:
					for element, values in enumerate(self.entries.values()):
						duplicate_candidate = element + 1
						if position != element and position < element and duplicate_candidate not in duplicates:
							if points.get("x").get() == values.get("x").get() and points.get("y").get() == values.get("y").get():
								duplicates.append(duplicate_candidate)
			except ValueError:
				check = False
			if check == False:
				to_delete.append(delete_candidate)
		
		to_delete = to_delete + list(set(duplicates))
		
		for element in to_delete:
			self.entries[element]['x'].grid_forget()
			self.entries[element]['y'].grid_forget()
			self.entries.pop(element)

		temporary_entries = {}

		for position, points in enumerate(self.entries.values()):
			delete_candidate = position + 1
			temporary_entries[delete_candidate] = points
		
		while self.length > 0:
			self.handle_delete_entry()
   
		self.entries = temporary_entries

		for points in self.entries.values():
			self.length += 1

			entry1 = points['x']
			entry2 = points['y']

			entry1.grid(ipady=5,column=0, row = self.length)
			
			entry2.grid(ipady=5, column=1, row = self.length)

		if self.length > 1:
			plot = Plot()
			plot.draw_plot(self.entries)
		elif self.length == 0:
			messagebox.showerror("Calculate error [3]", "There are no points to calculate")
		else:
			messagebox.showerror("Calculate error [4]", "Can't calculate for only 1 point")
	
	def validate_single_entry(self, point):
		check = False
		try:
			if float(point[0]) and float(point[1]):
				check = True
		except ValueError:
			pass
		return check

	# https://pythonguides.com/python-tkinter-save-text-to-file/
	def handle_load_entries(self):
	
		while self.length > 0:
			self.handle_delete_entry()
   
		files = [('Text Files', '*.txt')]
		file_to_open = filedialog.askopenfilename(initialdir="", title="Select your file", filetypes=files, defaultextension= files)
	
		try:
			file = open(file_to_open, 'r')
			lines = file.readlines()
			invalid_lines = 0
			for line in lines:
				line = line.strip()
	
				point = line.split()
				
				if len(point) == 2 and self.length < 24 and self.validate_single_entry(point) == True:
					self.length += 1
					entry1 = ttk.Entry(frame)
					entry2 = ttk.Entry(frame)

					entry1.grid(ipady=5,column=0, row = self.length)
					entry1.insert(0, point[0])
					
					entry2.grid(ipady=5, column=1, row = self.length)
					entry2.insert(0, point[1])
	 
					self.entries.update({self.length: {"x": entry1, "y": entry2}})
				else:
					invalid_lines += 1
		except FileNotFoundError:
			messagebox.showerror("Load entries error [4]","File not found")
		if invalid_lines > 0:
			messagebox.showerror("Loading entries error [5]", "Invalid data found: only loaded the valid data. Check the file again if you want to load all the data")
		if self.length == 24:
			messagebox.showerror("Loading entries limit [6]", "Entries limit reached: 24")
   
	def handle_save_entries(self):
		files = [('Text Files', '*.txt')]
		# Type of file is TextIOWrapper and not the actual path of the file
		file = filedialog.asksaveasfile(title="Save your file", filetypes= files, defaultextension= files)

		file_to_save_to = file.name
		with open(file_to_save_to, "w") as f:
			for point in self.entries.values():
				content = "{x} {y}\n".format(x = point.get("x").get(), y = point.get("y").get())
				f.write(content)

class Plot():
	
	def __init__(self):
		self.points_array = []
		self.m = 0
		self.b = 0
  
	def get_array(self, object):
		array = []
		for point in object.values():
			array.append([float(point['x'].get()), float(point['y'].get())])
		return array
	
	def calculate(self):
		square_x = []
		x_times_y = []
		for point in self.points_array:
			square_x.append(point[0] * point[0])
			x_times_y.append(point[0] * point[1])
		sum_x = sum(point[0] for point in self.points_array)
		sum_y = sum(point[1] for point in self.points_array)
		sum_square_x = sum(value for value in square_x)
		sum_x_times_y = sum(value for value in x_times_y)

		n = len(self.points_array)
		try:
			self.m = (n * sum_x_times_y - sum_x * sum_y) / (n * sum_square_x - sum_x * sum_x)
		except ZeroDivisionError:
			pass
		
		self.b = (sum_y - self.m * sum_x) / n

		def least_square_liniar_calculator(x): return self.m * x + self.b
  
		return least_square_liniar_calculator

	def draw_plot(self, object):
		self.points_array = self.get_array(object)
		linear_function = self.calculate()

		x_points = []
		y_points = []
		function_points = []
		if type(self.m) == int:
			function_to_title = "x = {point} [note: x, not y]".format(point = self.points_array[0][0])
		else:
			function_to_title = "f(x) = {m} * x + {b}".format(m = round(self.m, 4) , b = round(self.b, 4))
   
		#just checking the values in case something happens
		print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		print("Function is {function}".format(function = function_to_title))
		for point in self.points_array:
			x_points.append(point[0])
			y_points.append(point[1])
			function_points.append(linear_function(point[0]))
			point = "x: {point_0} y: {point_1} f(x) = {fi0} error (f(x) - y): {error}".format(point_0 = str(point[0]), 
																		point_1 = str(point[1]),
																		fi0 = str(linear_function(point[0])),
																		error = str((linear_function(point[0]) - point[1])))
			print(point)
		print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
  
		plt.xlabel("X")
		plt.ylabel("Y")
		plt.clf()
		plt.title(function_to_title)
		plt.plot(x_points, y_points)
		plt.scatter(x_points, y_points, color='black')
		plt.plot(x_points, y_points, color='black', label='Line between points')

		maximum = max(max(x_points), max(y_points))
		minimum = min(min(x_points), min(y_points))

		plt.plot(x_points, function_points, color='red', label='Function line')
  
		plt.plot([x_points[0], x_points[0]], [y_points[0], function_points[0]], linestyle= 'dashed', color='blue', label="Error")
		for i in range(1, len(x_points)):
			plt.plot([x_points[i], x_points[i]], [y_points[i], function_points[i]], linestyle= 'dashed', color='blue')
  
		plt.xlim([minimum - 1, maximum + 1])
		plt.ylim([minimum - 1, maximum + 1])

		plt.legend()
  
		plt.show()
  
		del self.points_array[:]

if __name__ == "__main__":
	window = tk.Tk(className = 'metoda celor mai mici patrate')
 
	frame = ttk.Frame(window, padding = 5)
	frame.grid()

	entries = Entries()
 
	entries.handle_add_entry()
	entries.handle_add_entry()
 
	ttk.Label(frame, text="X").grid(column = 0, row = 0)
	ttk.Label(frame, text="Y").grid(column = 1, row = 0)

	ttk.Button(frame, text = "New Entry", padding=5, width=20, command = entries.handle_add_entry).grid(column=2,row=1)
	ttk.Button(frame, text = "Delete Entry", padding=5, width=20, command = entries.handle_delete_entry).grid(column=2,row=2)
	ttk.Button(frame, text = "Load Entries", padding=5, width=20, command = entries.handle_load_entries).grid(column=2, row=3)
	ttk.Button(frame, text = "Save Entries", padding=5, width=20, command = entries.handle_save_entries).grid(column=2, row=4)
	ttk.Button(frame, text = "Calculate", padding=5, width=20, command=entries.handle_validate_entries).grid(column=2,row=5)
 
	window.mainloop()

