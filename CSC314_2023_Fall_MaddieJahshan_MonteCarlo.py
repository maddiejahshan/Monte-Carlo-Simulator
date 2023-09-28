import math
import random
import tkinter as tk
from tkinter import ttk

class MonteCarloSIM:
    def __init__ (self, root):
# First, create a GUI window and give it a title and an icon
        self.window = root
        self.window.wm_title('MonteCarloSIM')
        self.window.resizable(False, False)
        self.dot_color_hit = tk.StringVar(value = 'cornflowerblue')
        self.dot_color_miss = tk.StringVar(value = 'darkseagreen')
        self.drawing_canvas = tk.Canvas(self.window, width=300, height=300, highlightthickness=1, highlightbackground='black', bg='white')
        self.drawing_canvas.grid(row=2, column=1, rowspan=4, padx=10, pady=10)

        # Create a circle to represent the target area
        self.circle_origin_x = 150
        self.circle_origin_y = 150
        self.circle_radius = 150
        self.drawing_canvas.create_oval(
            self.circle_origin_x - self.circle_radius,
            self.circle_origin_y - self.circle_radius,
            self.circle_origin_x + self.circle_radius,
            self.circle_origin_y + self.circle_radius,
            outline="black"
        )
        self.drawing_canvas.create_line(self.circle_origin_x, 0, self.circle_origin_x, 300, fill="black")
        self.drawing_canvas.create_line(0, self.circle_origin_y, 300, self.circle_origin_y, fill="black")

        # Create the GUI widgets
        self.enable_ani_lbl = tk.Label(self.window, text='Animate Simulation')
        self.enable_ani = ttk.Checkbutton(self.window)
        self.enable_ani.grid(row=1, column=2,)
        self.enable_ani_lbl.grid(row=1, column=3, columnspan=10)
        
        self.dart_count = tk.Label(self.window, text='Dart Count:')
        self.dart_count.grid(row=2, column=2, sticky='e')

        self.choose_size = tk.Scale(root, from_ = 10, to = 1000, orient = 'horizontal')
        self.choose_size.grid(row=2, column=2, columnspan=2, pady=10, padx=10)

        self.miss_lbl = tk.Label(self.window, text='Misses:')
        self.dotcolor_miss = ttk.Combobox(self.window, textvariable = self.dot_color_miss, state=['readonly'],values=['darkseagreen', 'cornflowerblue'])
        self.miss_lbl.grid(row=3, column=2, sticky='e')
        self.dotcolor_miss.grid(row=3, column=3)
            
        self.hit_lbl = tk.Label(self.window, text='Hits:')
        self.dotcolor_hit = ttk.Combobox(self.window, textvariable = self.dot_color_hit, state=['readonly'], values=['darkseagreen', 'cornflowerblue'])
        self.hit_lbl.grid(row=4, column=2, sticky='e')
        self.dotcolor_hit.grid(row=4, column=3)

        self.run_sim = ttk.Button(self.window, text='Run Simulator', command=self.CreatePoints)
        self.run_sim.grid(row=5, column=2, columnspan=2)

        self.clear_sim = ttk.Button(self.window,text='Clear Simulator', command= self.ClearCanvas)
        self.clear_sim.grid(row=6, column=2, columnspan=2)

        self.calc_pi = tk.Entry(self.window)
        self.calc_pi.grid(row=7,column=3, columnspan=3)
        self.calc_pi_lbl = tk.Label(self.window, text='Calculated Pi:')
        self.calc_pi_lbl.grid(row=7, column=1, columnspan=3)
        
        num_points = int(self.choose_size.get())
        hits = 0
        pi_estimate = 4 * (hits / num_points)
        self.calc_pi.delete(0, tk.END)  # Clear the Entry widget
        self.calc_pi.insert(0, f'{pi_estimate:.6f}')  # Display Pi
    
    #Creates the points
    def CreatePoints(self):
        num_points = int(self.choose_size.get())
        self.hits = 0  # Reset hits to zero

        def isInCircle(x, y, radius):
            distance = math.sqrt(x**2 + y**2)
            if distance >= radius:
                return self.dot_color_miss.get()
            else:
                return self.dot_color_hit.get()

        def animate_darts(count):
            if count < num_points:
                x = random.uniform(-1, 1)
                y = random.uniform(-1, 1)

                color = isInCircle(x, y, 1)

                canvas_x = int((x) * self.circle_radius + self.circle_origin_x)/1
                canvas_y = int((-y) * self.circle_radius + self.circle_origin_y)/1


                self.drawing_canvas.create_oval(
                    canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2,
                    outline=color,
                    fill=color
                )
                if color == self.dot_color_hit.get():
                    self.hits += 1

                # Update Pi estimate
                pi_estimate = 4 * (self.hits / (count + 1))
                self.calc_pi.delete(0, tk.END)
                self.calc_pi.insert(0, f'{pi_estimate:.6f}')

                # Update the canvas and continue animating
                self.window.update()
                self.window.after(10, animate_darts, count + 1)

        # Start the animation
        animate_darts(0)
        
    #Clears canvas
    def ClearCanvas(self):
        self.drawing_canvas.delete("all")
        self.drawing_canvas.create_oval(
            self.circle_origin_x - self.circle_radius,
            self.circle_origin_y - self.circle_radius,
            self.circle_origin_x + self.circle_radius,
            self.circle_origin_y + self.circle_radius,
            outline="black"
        )
        self.drawing_canvas.create_line(self.circle_origin_x, 0, self.circle_origin_x, 300, fill="black")
        self.drawing_canvas.create_line(0, self.circle_origin_y, 300, self.circle_origin_y, fill="black")
        
window = tk.Tk()
app = MonteCarloSIM(window)
window.mainloop()