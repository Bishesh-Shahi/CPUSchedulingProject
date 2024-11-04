# CPU-Scheduling
 CS405 Team Project
# CPU Process Scheduler

The CPU Process Scheduler is a graphical user interface (GUI) application that simulates the scheduling of processes on a computer's CPU. It allows users to input a set of processes with their respective arrival times, burst times, and priorities, and then visualizes the scheduling of these processes using three different algorithms: First-Come, First-Served (FCFS), Round-Robin (RR), and Priority Scheduling.

## Features

- **Process Input**: Users can input the details of each process, including its ID, arrival time, burst time, and priority.
- **Scheduling Algorithms**: The application implements the FCFS, RR, and Priority scheduling algorithms to determine the order and timing of process execution.
- **Gantt Chart Visualization**: The application displays a Gantt chart visualization of the scheduling results, showing the start and end times of each process, as well as any idle periods in the CPU.
- **Performance Metrics**: The application calculates and displays the average waiting time and average turnaround time for each scheduling algorithm, providing insights into their performance.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies (Tkinter, Matplotlib, and Numpy).
3. Run the `gui.py` file to launch the application.
4. Input the details of the processes you want to schedule.
5. Select the scheduling algorithm you want to use.
6. Click the "Schedule" button to see the scheduling results and Gantt chart visualization.

## Project Structure

The project consists of the following files:

- `gui.py`: The main entry point of the application, which contains the code for the graphical user interface.
- `rr.py`: Implements the Round-Robin scheduling algorithm.
- `fcfs.py`: Implements the First-Come, First-Served scheduling algorithm.
- `priority.py`: Implements the Priority scheduling algorithm.
- `process.py`: Defines the `Process` class, which represents a single process with its attributes.

## Dependencies

- Python 3.x
- Tkinter (built-in)
- Matplotlib
- Numpy

## Contributing

If you find any issues or have suggestions for improvements, feel free to open a new issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
