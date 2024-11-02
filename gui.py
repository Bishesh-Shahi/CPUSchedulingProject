import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from process import Process
from fcfs import FCFS
from rr import RR
from priority import Priority

class SchedulerGUI:
    def __init__(self, master):
        """Initialize the Scheduler GUI application."""
        self.master = master
        self.master.title("Process Scheduler")
        self.master.geometry("800x900")
        
        # Initialize variables
        self.processes = []
        self.selected_algorithm = tk.StringVar(value="FCFS")
        self.quantum_time = tk.IntVar(value=2)
        
        # Create the main UI
        self.create_widgets()
        self.update_quantum_visibility()
        
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Process Management Frame
        self.process_frame = ttk.LabelFrame(self.master, text="Process Management")
        self.process_frame.pack(padx=10, pady=5, fill="x")
        
        # Process List
        self.process_listbox = tk.Listbox(self.process_frame, height=5)
        self.process_listbox.pack(padx=5, pady=5, fill="x")
        self.process_listbox.bind('<<ListboxSelect>>', self.on_process_selected)
        
        # Process Control Buttons
        btn_frame = ttk.Frame(self.process_frame)
        btn_frame.pack(fill="x", padx=5)
        
        ttk.Button(btn_frame, text="Remove Process", command=self.remove_process).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit Process", command=self.edit_process).pack(side="left", padx=5)
        
        # Process Input Frame
        input_frame = ttk.Frame(self.process_frame)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        # Labels and Entries
        labels = ["Process ID", "Arrival Time", "Burst Time", "Priority"]
        self.entries = {}
        
        for i, label in enumerate(labels):
            ttk.Label(input_frame, text=label).grid(row=0, column=i, padx=5)
            entry = ttk.Entry(input_frame, width=15, justify='center')
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.entries[label.lower().replace(" ", "_")] = entry
        
        ttk.Button(input_frame, text="Add Process", command=self.add_process).grid(row=1, column=len(labels), padx=5)
        
        # Algorithm Selection Frame
        self.algorithm_frame = ttk.LabelFrame(self.master, text="Algorithm Selection")
        self.algorithm_frame.pack(padx=10, pady=5, fill="x")
        
        # Algorithm Dropdown
        algo_frame = ttk.Frame(self.algorithm_frame)
        algo_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(algo_frame, text="Select Algorithm:").pack(side="left", padx=5)
        self.algorithm_combo = ttk.Combobox(algo_frame, values=["FCFS", "RR", "Priority"], 
                                          textvariable=self.selected_algorithm, state="readonly")
        self.algorithm_combo.pack(side="left", padx=5)
        self.algorithm_combo.bind("<<ComboboxSelected>>", self.on_algorithm_selected)
        
        # Quantum Time Entry
        self.quantum_frame = ttk.Frame(self.algorithm_frame)
        self.quantum_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(self.quantum_frame, text="Quantum Time:").pack(side="left", padx=5)
        self.quantum_entry = ttk.Entry(self.quantum_frame, textvariable=self.quantum_time, 
                                     width=10, justify='center')
        self.quantum_entry.pack(side="left", padx=5)
        
        # Schedule Button
        ttk.Button(self.master, text="Schedule Processes", 
                  command=self.schedule_processes).pack(pady=10)
        
        # Output Frame
        self.output_frame = ttk.LabelFrame(self.master, text="Scheduling Results")
        self.output_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Output Text
        self.output_text = tk.Text(self.output_frame, height=10)
        self.output_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Gantt Chart Frame
        self.gantt_frame = ttk.LabelFrame(self.master, text="Gantt Chart")
        self.gantt_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
    def add_process(self):
        """Add a new process to the list."""
        try:
            name = self.entries["process_id"].get()
            arrival_time = int(self.entries["arrival_time"].get())
            burst_time = int(self.entries["burst_time"].get())
            priority = int(self.entries["priority"].get())
            
            if not name or arrival_time < 0 or burst_time <= 0 or priority < 0:
                raise ValueError("Invalid input values")
                
            process = Process(name, arrival_time, burst_time, priority)
            self.processes.append(process)
            self.update_process_listbox()
            
            # Clear entries
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numeric values")
            
    def remove_process(self):
        """Remove the selected process from the list."""
        selected = self.process_listbox.curselection()
        if selected:
            del self.processes[selected[0]]
            self.update_process_listbox()
            
    def edit_process(self):
        """Edit the selected process."""
        selected = self.process_listbox.curselection()
        if not selected:
            return
            
        try:
            process = self.processes[selected[0]]
            name = self.entries["process_id"].get()
            arrival_time = int(self.entries["arrival_time"].get())
            burst_time = int(self.entries["burst_time"].get())
            priority = int(self.entries["priority"].get())
            
            if not name or arrival_time < 0 or burst_time <= 0 or priority < 0:
                raise ValueError("Invalid input values")
                
            process.name = name
            process.arrival_time = arrival_time
            process.burst_time = burst_time
            process.priority = priority
            
            self.update_process_listbox()
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values")
            
    def update_process_listbox(self):
        """Update the process listbox display."""
        self.process_listbox.delete(0, tk.END)
        for i, process in enumerate(self.processes, 1):
            self.process_listbox.insert(tk.END, 
                f"P{i}: {process.name} (Arrival: {process.arrival_time}, Burst: {process.burst_time}, Priority: {process.priority})")
            
    def on_process_selected(self, event):
        """Handle process selection from the listbox."""
        selected = self.process_listbox.curselection()
        if selected:
            process = self.processes[selected[0]]
            
            self.entries["process_id"].delete(0, tk.END)
            self.entries["process_id"].insert(0, process.name)
            
            self.entries["arrival_time"].delete(0, tk.END)
            self.entries["arrival_time"].insert(0, str(process.arrival_time))
            
            self.entries["burst_time"].delete(0, tk.END)
            self.entries["burst_time"].insert(0, str(process.burst_time))
            
            self.entries["priority"].delete(0, tk.END)
            self.entries["priority"].insert(0, str(process.priority))
            
    def on_algorithm_selected(self, event):
        """Handle algorithm selection."""
        self.update_quantum_visibility()
        
    def update_quantum_visibility(self):
        """Show/hide quantum time entry based on selected algorithm."""
        if self.selected_algorithm.get() == "RR":
            self.quantum_frame.pack(fill="x", padx=5, pady=5)
        else:
            self.quantum_frame.pack_forget()
            
    def schedule_processes(self):
        """Execute the selected scheduling algorithm."""
        if not self.processes:
            messagebox.showwarning("Warning", "Please add some processes first")
            return
            
        algorithm = self.selected_algorithm.get()
        
        try:
            if algorithm == "FCFS":
                scheduler = FCFS()
            elif algorithm == "RR":
                quantum = self.quantum_time.get()
                if quantum <= 0:
                    raise ValueError("Quantum time must be positive")
                scheduler = RR(quantum)
            elif algorithm == "Priority":
                scheduler = Priority()
                
            # Clear previous output
            self.output_text.delete(1.0, tk.END)
            
            # Run scheduling algorithm
            output = scheduler.schedule(self.processes.copy())
            self.output_text.insert(tk.END, output)
            
            # Update Gantt chart
            self.plot_gantt_chart()
            
        except Exception as e:
            messagebox.showerror("Error", f"Scheduling error: {str(e)}")
            
    def plot_gantt_chart(self):
        """Generate and display the Gantt chart."""
        # Clear previous chart
        for widget in self.gantt_frame.winfo_children():
            widget.destroy()
            
        if not self.processes:
            return
            
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Generate colors for processes
        colors = plt.cm.Set3(np.linspace(0, 1, len(self.processes)))
        
        # Plot each process
        for i, process in enumerate(self.processes):
            start = process.arrival_time
            duration = process.burst_time
            ax.barh(i, duration, left=start, color=colors[i], 
                   label=f'Process {process.name}')
            
            # Add process details
            ax.text(start + duration/2, i, f'P{process.name}',
                   ha='center', va='center')
            
        # Customize the chart
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_title('Process Scheduling Gantt Chart')
        ax.set_yticks(range(len(self.processes)))
        ax.set_yticklabels([f'P{p.name}' for p in self.processes])
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Embed the chart in the GUI
        canvas = FigureCanvasTkAgg(fig, master=self.gantt_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

def main():
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

