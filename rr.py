

class RR:
    def __init__(self, quantum_time):
        self.current_time = 0
        self.time_quantum = quantum_time  
        self.total_waiting_time = 0
        self.total_turnaround_time = 0

    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"
        
        remaining_burst_time = [process.burst_time for process in processes]
        waiting_times = [0] * len(processes)
        first_response_time = [-1] * len(processes)

        # Header with centered columns
        scheduling_output = f"{'Process ID':^12}{'Arrival Time':^15}{'Burst Time':^12}{'Waiting Time':^15}{'Turnaround Time':^17}\n"
        scheduling_output += "-" * 71 + "\n"
        
        completed_processes = set()  # Track which processes have been output
        
        while True:
            done = True
            for i, process in enumerate(processes):
                if remaining_burst_time[i] > 0:
                    done = False

                    if first_response_time[i] == -1:
                        first_response_time[i] = self.current_time

                    if remaining_burst_time[i] > self.time_quantum:
                        self.current_time += self.time_quantum
                        remaining_burst_time[i] -= self.time_quantum
                    else:
                        self.current_time += remaining_burst_time[i]
                        remaining_burst_time[i] = 0
                        
                        process_turnaround_time = self.current_time - process.arrival_time
                        self.total_turnaround_time += process_turnaround_time
                        
                        waiting_times[i] = process_turnaround_time - process.burst_time
                        self.total_waiting_time += waiting_times[i]
                        
                        # Only output process information once when it completes
                        if i not in completed_processes:
                            scheduling_output += f"{process.name:^12}{process.arrival_time:^15}{process.burst_time:^12}{waiting_times[i]:^15}{process_turnaround_time:^17}\n"
                            completed_processes.add(i)

            if done:
                break
        
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)
        
        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"

        return scheduling_output