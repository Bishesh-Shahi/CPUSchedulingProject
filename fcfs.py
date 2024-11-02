class FCFS:
    def __init__(self):
        self.current_time = 0
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
    
    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"
        
        processes.sort(key=lambda x: x.arrival_time)
        
        scheduling_output = f"{'Process ID':^12}{'Arrival Time':^15}{'Burst Time':^12}{'Waiting Time':^15}{'Turnaround Time':^17}\n"
        scheduling_output += "-" * 71 + "\n"
        
        for process in processes:
            
            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
            
            waiting_time = self.current_time - process.arrival_time
            self.total_waiting_time += waiting_time
            
            turnaround_time = waiting_time + process.burst_time
            self.total_turnaround_time += turnaround_time
            
            scheduling_output += f"{process.name:^12}{process.arrival_time:^15}{process.burst_time:^12}{waiting_time:^15}{turnaround_time:^17}\n"
            
            self.current_time += process.burst_time
        
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)
        
        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        
        return scheduling_output