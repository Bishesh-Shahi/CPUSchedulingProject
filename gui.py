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
        algorithm = self.selected_algorithm.get()
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)  # Clear the text widget
        
        # Create the appropriate scheduler instance
        if algorithm == "FCFS":
            scheduler = FCFS()
        elif algorithm == "RR":
            quantum = self.quantum_time.get()  # Get the quantum time from the entry
            scheduler = RR(quantum)  # Pass the quantum to the RR scheduler
        elif algorithm == "Priority":
            scheduler = Priority()
        else:
            self.output_text.insert(tk.END, "Selected algorithm is not implemented.")
            self.output_text.configure(state="disabled")
            return
        
        # Get the scheduling output
        scheduling_output = scheduler.schedule(self.processes)
        self.output_text.insert(tk.END, scheduling_output)
        self.output_text.configure(state="disabled")

        # Plot the Gantt chart after scheduling, passing the scheduler instance
        self.plot_gantt_chart(scheduler)

    def plot_gantt_chart(self, scheduler):
        for widget in self.gantt_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(12, 6))
        
        if isinstance(scheduler, RR):
            # Get execution sequence for Round Robin
            execution_sequence = self.get_rr_execution_sequence(scheduler)
            
            # Create unique process list while preserving order
            unique_processes = []
            process_indices = {}  # Maps process name to y-axis position
            
            for entry in execution_sequence:
                process_name = entry['process'].name
                if process_name not in process_indices:
                    process_indices[process_name] = len(unique_processes)
                    unique_processes.append(entry['process'])

            # Create color map
            cmap = plt.get_cmap('tab10')
            colors = {process.name: cmap(i % 10) for i, process in enumerate(unique_processes)}
            
            # Plot execution blocks
            for i, entry in enumerate(execution_sequence):
                process = entry['process']
                start_time = entry['start_time']
                end_time = entry['end_time']
                y_pos = process_indices[process.name]
                
                # Plot the execution block
                ax.barh(y_pos, 
                       end_time - start_time, 
                       left=start_time, 
                       color=colors[process.name], 
                       edgecolor='black',
                       alpha=0.7)
                
                # Add time markers
                if i == 0 or execution_sequence[i-1]['end_time'] != start_time:
                    ax.axvline(x=start_time, color='gray', linestyle='--', alpha=0.5)
                ax.text(start_time, -0.5, f'{start_time}', 
                       rotation=45, ha='right', va='top')
            
            # Add final time marker
            last_end_time = execution_sequence[-1]['end_time']
            ax.axvline(x=last_end_time, color='gray', linestyle='--', alpha=0.5)
            ax.text(last_end_time, -0.5, f'{last_end_time}', 
                   rotation=45, ha='right', va='top')
            
            # Customize the chart
            ax.set_xlabel('Time')
            ax.set_ylabel('Processes')
            ax.set_title('Round Robin Gantt Chart')
            ax.set_yticks(range(len(unique_processes)))
            ax.set_yticklabels([f'Process {p.name}' for p in unique_processes])
            ax.grid(True, axis='x', alpha=0.3)
            
            # Add legend
            handles = [plt.Rectangle((0,0),1,1, color=colors[p.name]) for p in unique_processes]
            ax.legend(handles, [f'Process {p.name}' for p in unique_processes], 
                     loc='upper right', bbox_to_anchor=(1.15, 1))
            
        else:
            # Original implementation for other algorithms
            processes = self.processes
            cmap = plt.get_cmap('tab10')
            colors = cmap(np.linspace(0, 1, len(processes)))
            
            for i, process in enumerate(processes):
                start_time = process.arrival_time
                end_time = process.arrival_time + process.burst_time
                ax.barh(i, end_time - start_time, left=start_time, 
                       color=colors[i], label=f'Process {process.name}')
            
            ax.set_xlabel('Time')
            ax.set_ylabel('Processes')
            ax.set_title('Gantt Chart')
            ax.set_yticks(np.arange(len(processes)))
            ax.set_yticklabels([f'Process {p.name}' for p in processes])
            ax.legend(loc='upper right')
            ax.grid(True)

        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.gantt_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def get_rr_execution_sequence(self, scheduler):
        """
        Simulate Round Robin scheduling to get the execution sequence.
        Returns a list of dictionaries containing process and its execution time slots.
        """
        if not self.processes:
            return []
            
        execution_sequence = []
        current_time = 0
        ready_queue = []
        processes = [Process(p.name, p.arrival_time, p.burst_time, p.priority) 
                    for p in self.processes]  # Create a deep copy
        remaining_burst_times = {p.name: p.burst_time for p in processes}
        
        while True:
            # Add newly arrived processes to ready queue
            for process in processes:
                if (process.arrival_time <= current_time and 
                    remaining_burst_times[process.name] > 0 and 
                    process not in ready_queue):
                    ready_queue.append(process)
            
            if not ready_queue:
                if all(remaining_burst_times[p.name] == 0 for p in processes):
                    break
                current_time += 1
                continue
            
            # Get next process from ready queue
            current_process = ready_queue.pop(0)
            
            # Calculate execution time for this quantum
            execution_time = min(scheduler.time_quantum, 
                               remaining_burst_times[current_process.name])
            
            # Record execution block
            execution_sequence.append({
                'process': current_process,
                'start_time': current_time,
                'end_time': current_time + execution_time
            })
            
            # Update time and remaining burst time
            current_time += execution_time
            remaining_burst_times[current_process.name] -= execution_time
            
            # Re-add process to ready queue if it's not finished
            if remaining_burst_times[current_process.name] > 0:
                ready_queue.append(current_process)
            
            # Add newly arrived processes that came during this execution
            for process in processes:
                if (process.arrival_time <= current_time and 
                    remaining_burst_times[process.name] > 0 and 
                    process not in ready_queue and 
                    process != current_process):
                    ready_queue.append(process)
        
        return execution_sequence
def main():
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
