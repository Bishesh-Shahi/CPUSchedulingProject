

class Priority:
    def __init__(self):
        self.current_time = 0
        self.total_waiting_time = 0
        self.total_turnaround_time = 0

    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"

        # Sort processes by arrival time and priority
        processes.sort(key=lambda x: (x.arrival_time, x.priority))
        
        # Create formatted header
        scheduling_output = f"{'Process ID':^12}{'Arrival Time':^15}{'Priority':^12}{'Burst Time':^12}{'Waiting Time':^15}{'Turnaround Time':^17}\n"
        scheduling_output += "-" * 83 + "\n"  # Separator line
        
        # Process each process
        for process in processes:
            # Update current time if there's a gap
            if process.arrival_time > self.current_time:
                self.current_time = process.arrival_time
            
            # Calculate times
            waiting_time = self.current_time - process.arrival_time
            self.total_waiting_time += waiting_time
            
            turnaround_time = waiting_time + process.burst_time
            self.total_turnaround_time += turnaround_time
            
            # Update current time
            self.current_time += process.burst_time
            
            # Add formatted process data
            scheduling_output += f"{process.name:^12}{process.arrival_time:^15}{process.priority:^12}{process.burst_time:^12}{waiting_time:^15}{turnaround_time:^17}\n"
        
        # Calculate and add averages
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)
        
        # Add separator and averages to output
        scheduling_output += "-" * 83 + "\n"
        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}"
        scheduling_output += f"\nAverage Turnaround Time: {avg_turnaround_time:.2f}"
        
        return scheduling_output