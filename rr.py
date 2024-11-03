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
        gantt_chart = []  # To store the execution order for the Gantt chart
        finished_processes = 0  # Count of finished processes

        scheduling_output = f"{'Process ID':^12}{'Arrival Time':^15}{'Burst Time':^12}{'Waiting Time':^15}{'Turnaround Time':^17}\n"
        scheduling_output += "-" * 71 + "\n"
        while finished_processes < len(processes):
            process_found = False
            for i, process in enumerate(processes):
                # Check if the process has arrived and still has burst time left
                if remaining_burst_time[i] > 0 and process.arrival_time <= self.current_time:
                    process_found = True  # At least one process is ready to execute
                    if remaining_burst_time[i] > self.time_quantum:
                        gantt_chart.append(process.name)  # Record execution for Gantt chart
                        self.current_time += self.time_quantum
                        remaining_burst_time[i] -= self.time_quantum
                    else:
                        gantt_chart.append(process.name)  # Record execution for Gantt chart
                        self.current_time += remaining_burst_time[i]
                        process_turnaround_time = self.current_time - process.arrival_time
                        self.total_turnaround_time += process_turnaround_time
                        
                        waiting_times[i] = process_turnaround_time - process.burst_time
                        self.total_waiting_time += waiting_times[i]
                        
                        scheduling_output += f"{process.name}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t{waiting_times[i]}\t\t{process_turnaround_time}\n"
                        remaining_burst_time[i] = 0  # Process finished
                        finished_processes += 1  # Increment finished process count

            # If no process was found, increment current time to the next arriving process
            if not process_found:
                next_process_arrival = min(
                    process.arrival_time for process in processes if process.arrival_time > self.current_time
                )
                self.current_time = next_process_arrival  # Jump to next arrival time

        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)

        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"

        return scheduling_output, gantt_chart  # Return gantt_chart as well