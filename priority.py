class Priority:
    def __init__(self):
        self.current_time = 0
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.execution_sequence = []  # Store the execution sequence for Gantt chart

    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"

        remaining_processes = processes.copy()
        completed_processes = []
        execution_timeline = []  # Store when each process executes
        self.current_time = min(p.arrival_time for p in processes)

        while remaining_processes:
            # Get available processes at current time
            available_processes = [p for p in remaining_processes 
                                if p.arrival_time <= self.current_time]
            
            if not available_processes:
                # No process available, move time to next arrival
                next_arrival = min(p.arrival_time for p in remaining_processes)
                execution_timeline.append(("Idle", self.current_time, next_arrival))
                self.current_time = next_arrival
                continue

            # Select process with highest priority (lowest priority number)
            selected_process = min(available_processes, 
                                key=lambda p: (p.priority, p.arrival_time))
            
            # Record execution start time
            start_time = self.current_time
            
            # Execute the process
            self.current_time += selected_process.burst_time
            
            # Calculate times
            waiting_time = start_time - selected_process.arrival_time
            turnaround_time = self.current_time - selected_process.arrival_time
            
            # Update totals
            self.total_waiting_time += waiting_time
            self.total_turnaround_time += turnaround_time
            
            # Store execution info
            execution_timeline.append((selected_process.name, start_time, self.current_time))
            
            # Update process info
            selected_process.waiting_time = waiting_time
            selected_process.turnaround_time = turnaround_time
            
            # Move process to completed
            remaining_processes.remove(selected_process)
            completed_processes.append(selected_process)

        # Store execution sequence for Gantt chart
        self.execution_sequence = execution_timeline
        
        # Generate output string
        scheduling_output = "Process ID\tArrival Time\tPriority\tBurst Time\tWaiting Time\tTurnaround Time\n"
        for process in completed_processes:
            scheduling_output += f"{process.name}\t\t{process.arrival_time}\t\t{process.priority}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}\n"
        
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)
        
        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        
        return scheduling_output