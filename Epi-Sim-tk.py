# Group 5
# Epidemic Simulator

import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import seaborn as sns
import customtkinter

# main window / start menu
window = tk.Tk()
window.title("Epidemic Simulator")
window.configure(bg="#1C2C54")
window.geometry("800x500")
label = tk.Label(window, text="EPIDEMIC SIMULATOR", font=('Gotham Black', 30), bg="#1C2C54", fg="white")
label.pack(side="top", expand=True, anchor="s")
label = tk.Label(window, text="Made by Group 5 (BSCS 2-2)", font=('Gotham', 10), bg="#1C2C54", fg="white")
label.pack(side="top", expand=True, anchor="n")

# Define a function that handles the choice of user
def handle_choice(choice):
    if choice == "1":
        # Window if Select a preset is chosen.
        preset_window = tk.Toplevel(window)
        preset_window.title("Select Preset")
        preset_window.configure(bg="#4BC3B5")
        preset_window.geometry("300x100")

        def selected():
            # If Ebola is chosen
            if clicked.get() == 'Ebola':
                # Window of input if Ebola is chosen
                simulation_window = tk.Toplevel(window)
                simulation_window.title("Simulation")
                simulation_window.configure(bg="#4BC3B5")
                simulation_window.geometry("400x300")
                simulation_label = tk.Label(simulation_window, text="Ebola", font=('Gotham Black', 16),
                                            bg="#4BC3B5", fg="#454545")
                simulation_label.pack(padx=10, pady=10)

                Label1 = tk.Label(simulation_window, text="Enter population size: ", font=('Arial', 9),
                                  bg="#4BC3B5", fg="black")
                Label1.pack()
                POPULATION_SIZE = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
                POPULATION_SIZE.pack(padx=5, pady=5)

                Label2 = tk.Label(simulation_window, text="Enter initial infected count: ", font=('Arial', 9),
                                  bg="#4BC3B5", fg="black")
                Label2.pack()
                INITIAL_INFECTED_COUNT = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
                INITIAL_INFECTED_COUNT.pack(padx=5, pady=5)

                TRANSMISSION_PROB = 0.4
                RECOVERY_PROB = 0.2
                MORTALITY_PROB = 0.4

                button_simulation = customtkinter.CTkButton(master=simulation_window, command=lambda: on_button_click(),
                                                            text='Confirm',
                                                            fg_color=("dodger blue", "dodger blue"))
                button_simulation.pack(padx=40, pady=20)

                # Run the simulation
                def on_button_click():

                    results_window = tk.Toplevel(window)
                    results_window.title("Results")
                    results_window.configure(bg="#010402")
                    results_window.geometry("600x600")

                    scrollbar = ttk.Scrollbar(results_window, orient="vertical")
                    scrollbar.pack(side="right", fill="y")

                    canvas = tk.Canvas(results_window, bg="#010402", yscrollcommand=scrollbar.set)
                    canvas.pack(side="left", fill="both", expand=True)

                    frame = tk.Frame(canvas, bg="#010402")
                    canvas.create_window((0, 0), window=frame, anchor="n")

                    scrollbar.configure(command=canvas.yview)

                    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                    susceptible_count = int(POPULATION_SIZE.get()) - int(INITIAL_INFECTED_COUNT.get())
                    infected_count = int(INITIAL_INFECTED_COUNT.get())
                    recovered_count = 0
                    dead_count = 0

                    days = 0

                    # Initialize lists to store data
                    susceptible_data = []
                    infected_data = []

                    # Recovered data
                    recovered_data = []
                    dead_data = []

                    # Simulate disease spreading
                    while infected_count > 0:

                        # Increment days by 1
                        days += 1

                        # Calculate number of new infections and recoveries
                        new_infections = 0
                        recoveries = 0
                        deaths = 0
                        for i in range(infected_count):
                            if random.random() < float(TRANSMISSION_PROB):
                                new_infections += 1
                            if random.random() < float(RECOVERY_PROB):
                                recoveries += 1
                            if random.random() < float(MORTALITY_PROB):
                                deaths += 1

                        # This is to prevent new_infections variable from making susceptible_count negative
                        if new_infections > susceptible_count:
                            new_infections = susceptible_count

                        # This is to prevent new_infections variable from making infected_count negative
                        if new_infections > recoveries + deaths:
                            new_infections = recoveries + deaths

                        # Update data
                        susceptible_count -= new_infections
                        infected_count += new_infections - recoveries - deaths
                        recovered_count += min(recoveries, infected_count)
                        dead_count += min(deaths, infected_count)

                        # Store data for this day
                        susceptible_data.append(susceptible_count)
                        infected_data.append(infected_count)
                        recovered_data.append(recovered_count)
                        dead_data.append(dead_count)

                        data = [susceptible_data, infected_data, recovered_data, dead_data]
                        data = list(map(list, zip(*data)))

                        results = tk.Label(frame,
                                           text=f"Day {days}: Susceptible: {susceptible_count}, Infected: {infected_count}, Recovered: {recovered_count}, Dead: {dead_count}",
                                           font=('Arial', 10), bg="#010402", fg="#4BC3B5")
                        results.pack()

                    text_finish = tk.Label(frame, text="Disease spread complete. ", font=('Gotham Black', 12),
                                           bg="#010402", fg="#4BC3B5")
                    text_finish.pack()

                    text_finalres = tk.Label(frame, text="Final results: ", font=('Gotham Black', 10),
                                             bg="#010402", fg="#4BC3B5")
                    text_finalres.pack()

                    final_results = tk.Label(frame,
                                             text=f"It took {days} days to have {susceptible_count} unaffected, {infected_count} infected, {recovered_count} recovered, and {dead_count} dead.",
                                             font=('Gotham Black', 10),
                                             bg="#010402", fg="#4BC3B5")
                    final_results.pack()

                    Label6 = tk.Label(frame, text="Do you want to see the graph?", font=('Gotham Black', 10),
                                      bg="#010402", fg="white")
                    Label6.pack(padx=20, pady=20)

                    button_plot = customtkinter.CTkButton(master=frame, command=lambda: plot_data(), text='View Graph',
                                                          fg_color=("dodger blue", "dodger blue"))
                    button_plot.pack(padx=10, pady=10)

                    button_hm = customtkinter.CTkButton(master=frame, command=lambda: heatmap(), text='View Heatmap',
                                                        fg_color=("dodger blue", "dodger blue"))
                    button_hm.pack(padx=10, pady=10)

                    button_exit = customtkinter.CTkButton(master=frame, command=lambda: results_window.destroy(),
                                                          text='Exit',
                                                          fg_color=("dodger blue", "dodger blue"))
                    button_exit.pack(padx=10, pady=10)

                    def plot_data():
                        plt.plot(susceptible_data, label="Susceptible")
                        plt.plot(infected_data, label="Infected")
                        plt.plot(recovered_data, label="Recovered")
                        plt.plot(dead_data, label="Dead")
                        plt.xlabel('Number of Days')
                        plt.ylabel('Population Size')
                        plt.legend()
                        plt.show()

                    def heatmap():
                        sns.heatmap(data, cmap="YlGnBu", xticklabels=["Susceptible", "Infected", "Recovered", "Dead"],
                                    yticklabels=False)
                        plt.title("Simulation Results")
                        plt.xlabel("Categories")
                        plt.ylabel("Days")
                        plt.show()

            # If Covid-19 is chosen
            elif clicked.get() == 'Covid-19':
                # Window of input if Covid-19 is chosen
                simulation_window = tk.Toplevel(window)
                simulation_window.title("Simulation")
                simulation_window.configure(bg="#4BC3B5")
                simulation_window.geometry("400x300")
                simulation_label = tk.Label(simulation_window, text="Covid-19", font=('Gotham Black', 16),
                                            bg="#4BC3B5", fg="#454545")
                simulation_label.pack(padx=10, pady=10)

                Label1 = tk.Label(simulation_window, text="Enter population size: ", font=('Arial', 9),
                                  bg="#4BC3B5", fg="black")
                Label1.pack()
                POPULATION_SIZE = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
                POPULATION_SIZE.pack(padx=5, pady=5)

                Label2 = tk.Label(simulation_window, text="Enter initial infected count: ", font=('Arial', 9),
                                  bg="#4BC3B5", fg="black")
                Label2.pack()
                INITIAL_INFECTED_COUNT = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
                INITIAL_INFECTED_COUNT.pack(padx=5, pady=5)

                TRANSMISSION_PROB = 0.6
                RECOVERY_PROB = 0.4
                MORTALITY_PROB = 0.2

                button_simulation = customtkinter.CTkButton(master=simulation_window, command=lambda: on_button_click(),
                                                            text='Confirm',
                                                            fg_color=("dodger blue", "dodger blue"))
                button_simulation.pack(padx=40, pady=20)

                # Run the simulation
                def on_button_click():

                    results_window = tk.Toplevel(window)
                    results_window.title("Results")
                    results_window.configure(bg="#010402")
                    results_window.geometry("600x600")

                    scrollbar = ttk.Scrollbar(results_window, orient="vertical")
                    scrollbar.pack(side="right", fill="y")

                    canvas = tk.Canvas(results_window, bg="#010402", yscrollcommand=scrollbar.set)
                    canvas.pack(side="left", fill="both", expand=True)

                    frame = tk.Frame(canvas, bg="#010402")
                    canvas.create_window((0, 0), window=frame, anchor="n")

                    scrollbar.configure(command=canvas.yview)

                    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                    susceptible_count = int(POPULATION_SIZE.get()) - int(INITIAL_INFECTED_COUNT.get())
                    infected_count = int(INITIAL_INFECTED_COUNT.get())
                    recovered_count = 0
                    dead_count = 0

                    days = 0

                    # Initialize lists to store data
                    susceptible_data = []
                    infected_data = []

                    # Recovered data
                    recovered_data = []
                    dead_data = []

                    # Simulate disease spreading
                    while infected_count > 0:

                        # Increment days by 1
                        days += 1

                        # Calculate number of new infections and recoveries
                        new_infections = 0
                        recoveries = 0
                        deaths = 0
                        for i in range(infected_count):
                            if random.random() < float(TRANSMISSION_PROB):
                                new_infections += 1
                            if random.random() < float(RECOVERY_PROB):
                                recoveries += 1
                            if random.random() < float(MORTALITY_PROB):
                                deaths += 1

                        # This is to prevent new_infections variable from making susceptible_count negative
                        if new_infections > susceptible_count:
                            new_infections = susceptible_count

                        # This is to prevent new_infections variable from making infected_count negative
                        if new_infections > recoveries + deaths:
                            new_infections = recoveries + deaths

                        # Update data
                        susceptible_count -= new_infections
                        infected_count += new_infections - recoveries - deaths
                        recovered_count += min(recoveries, infected_count)
                        dead_count += min(deaths, infected_count)

                        # Store data for this day
                        susceptible_data.append(susceptible_count)
                        infected_data.append(infected_count)
                        recovered_data.append(recovered_count)
                        dead_data.append(dead_count)

                        data = [susceptible_data, infected_data, recovered_data, dead_data]
                        data = list(map(list, zip(*data)))

                        results = tk.Label(frame,
                                           text=f"Day {days}: Susceptible: {susceptible_count}, Infected: {infected_count}, Recovered: {recovered_count}, Dead: {dead_count}",
                                           font=('Arial', 10), bg="#010402", fg="#4BC3B5")
                        results.pack()

                    text_finish = tk.Label(frame, text="Disease spread complete. ", font=('Gotham Black', 12),
                                           bg="#010402", fg="#4BC3B5")
                    text_finish.pack()

                    text_finalres = tk.Label(frame, text="Final results: ", font=('Gotham Black', 10),
                                             bg="#010402", fg="#4BC3B5")
                    text_finalres.pack()

                    final_results = tk.Label(frame,
                                             text=f"It took {days} days to have {susceptible_count} unaffected, {infected_count} infected, {recovered_count} recovered, and {dead_count} dead.",
                                             font=('Gotham Black', 10),
                                             bg="#010402", fg="#4BC3B5")
                    final_results.pack()

                    Label6 = tk.Label(frame, text="Do you want to see the graph?", font=('Gotham Black', 10),
                                      bg="#010402", fg="white")
                    Label6.pack(padx=20, pady=20)

                    button_plot = customtkinter.CTkButton(master=frame, command=lambda: plot_data(), text='View Graph',
                                                          fg_color=("dodger blue", "dodger blue"))
                    button_plot.pack(padx=10, pady=10)

                    button_hm = customtkinter.CTkButton(master=frame, command=lambda: heatmap(), text='View Heatmap',
                                                        fg_color=("dodger blue", "dodger blue"))
                    button_hm.pack(padx=10, pady=10)

                    button_exit = customtkinter.CTkButton(master=frame, command=lambda: results_window.destroy(),
                                                          text='Exit',
                                                          fg_color=("dodger blue", "dodger blue"))
                    button_exit.pack(padx=10, pady=10)

                    def plot_data():
                        plt.plot(susceptible_data, label="Susceptible")
                        plt.plot(infected_data, label="Infected")
                        plt.plot(recovered_data, label="Recovered")
                        plt.plot(dead_data, label="Dead")
                        plt.xlabel('Number of Days')
                        plt.ylabel('Population Size')
                        plt.legend()
                        plt.show()

                    def heatmap():
                        sns.heatmap(data, cmap="YlGnBu", xticklabels=["Susceptible", "Infected", "Recovered", "Dead"],
                                    yticklabels=False)
                        plt.title("Simulation Results")
                        plt.xlabel("Categories")
                        plt.ylabel("Days")
                        plt.show()

            # If Common Cold is chosen
            elif clicked.get() == 'Common Cold':
                # Window of input if Common Cold is chosen
                simulation_window = tk.Toplevel(window)
                simulation_window.title("Simulation")
                simulation_window.configure(bg="#4BC3B5")
                simulation_window.geometry("400x300")
                simulation_label = tk.Label(simulation_window, text="Common Cold", font=('Gotham Black', 16),
                                            bg="#4BC3B5", fg="#454545")
                simulation_label.pack(padx=10, pady=10)

                Label1 = tk.Label(simulation_window, text="Enter population size: ", font=('Arial', 9),
                                  bg="#4BC3B5", fg="black")
                Label1.pack()
                POPULATION_SIZE = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
                POPULATION_SIZE.pack(padx=5, pady=5)

                Label2 = tk.Label(simulation_window, text="Enter initial infected count: ", font=('Arial', 9),
                                  bg="#4BC3B5", fg="black")
                Label2.pack()
                INITIAL_INFECTED_COUNT = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
                INITIAL_INFECTED_COUNT.pack(padx=5, pady=5)

                TRANSMISSION_PROB = 0.4
                RECOVERY_PROB = 0.9
                MORTALITY_PROB = 0.05

                button_simulation = customtkinter.CTkButton(master=simulation_window, command=lambda: on_button_click(),
                                                            text='Confirm',
                                                            fg_color=("dodger blue", "dodger blue"))
                button_simulation.pack(padx=40, pady=20)

                # Run the simulation
                def on_button_click():

                    results_window = tk.Toplevel(window)
                    results_window.title("Results")
                    results_window.configure(bg="#010402")
                    results_window.geometry("600x600")

                    scrollbar = ttk.Scrollbar(results_window, orient="vertical")
                    scrollbar.pack(side="right", fill="y")

                    canvas = tk.Canvas(results_window, bg="#010402", yscrollcommand=scrollbar.set)
                    canvas.pack(side="left", fill="both", expand=True)

                    frame = tk.Frame(canvas, bg="#010402")
                    canvas.create_window((0, 0), window=frame, anchor="n")

                    scrollbar.configure(command=canvas.yview)

                    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                    susceptible_count = int(POPULATION_SIZE.get()) - int(INITIAL_INFECTED_COUNT.get())
                    infected_count = int(INITIAL_INFECTED_COUNT.get())
                    recovered_count = 0
                    dead_count = 0

                    days = 0

                    # Initialize lists to store data
                    susceptible_data = []
                    infected_data = []

                    # Recovered data
                    recovered_data = []
                    dead_data = []

                    # Simulate disease spreading
                    while infected_count > 0:

                        # Increment days by 1
                        days += 1

                        # Calculate number of new infections and recoveries
                        new_infections = 0
                        recoveries = 0
                        deaths = 0
                        for i in range(infected_count):
                            if random.random() < float(TRANSMISSION_PROB):
                                new_infections += 1
                            if random.random() < float(RECOVERY_PROB):
                                recoveries += 1
                            if random.random() < float(MORTALITY_PROB):
                                deaths += 1

                        # This is to prevent new_infections variable from making susceptible_count negative
                        if new_infections > susceptible_count:
                            new_infections = susceptible_count

                        # This is to prevent new_infections variable from making infected_count negative
                        if new_infections > recoveries + deaths:
                            new_infections = recoveries + deaths

                        # Update data
                        susceptible_count -= new_infections
                        infected_count += new_infections - recoveries - deaths
                        recovered_count += min(recoveries, infected_count)
                        dead_count += min(deaths, infected_count)

                        # Store data for this day
                        susceptible_data.append(susceptible_count)
                        infected_data.append(infected_count)
                        recovered_data.append(recovered_count)
                        dead_data.append(dead_count)

                        data = [susceptible_data, infected_data, recovered_data, dead_data]
                        data = list(map(list, zip(*data)))

                        results = tk.Label(frame,
                                           text=f"Day {days}: Susceptible: {susceptible_count}, Infected: {infected_count}, Recovered: {recovered_count}, Dead: {dead_count}",
                                           font=('Arial', 10), bg="#010402", fg="#4BC3B5")
                        results.pack()

                    text_finish = tk.Label(frame, text="Disease spread complete. ", font=('Gotham Black', 12),
                                           bg="#010402", fg="#4BC3B5")
                    text_finish.pack()

                    text_finalres = tk.Label(frame, text="Final results: ", font=('Gotham Black', 10),
                                             bg="#010402", fg="#4BC3B5")
                    text_finalres.pack()

                    final_results = tk.Label(frame,
                                             text=f"It took {days} days to have {susceptible_count} unaffected, {infected_count} infected, {recovered_count} recovered, and {dead_count} dead.",
                                             font=('Gotham Black', 10),
                                             bg="#010402", fg="#4BC3B5")
                    final_results.pack()

                    Label6 = tk.Label(frame, text="Do you want to see the graph?", font=('Gotham Black', 10),
                                      bg="#010402", fg="white")
                    Label6.pack(padx=20, pady=20)

                    button_plot = customtkinter.CTkButton(master=frame, command=lambda: plot_data(), text='View Graph',
                                                          fg_color=("dodger blue", "dodger blue"))
                    button_plot.pack(padx=10, pady=10)

                    button_hm = customtkinter.CTkButton(master=frame, command=lambda: heatmap(), text='View Heatmap',
                                                        fg_color=("dodger blue", "dodger blue"))
                    button_hm.pack(padx=10, pady=10)

                    button_exit = customtkinter.CTkButton(master=frame, command=lambda: results_window.destroy(),
                                                          text='Exit',
                                                          fg_color=("dodger blue", "dodger blue"))
                    button_exit.pack(padx=10, pady=10)

                    def plot_data():
                        plt.plot(susceptible_data, label="Susceptible")
                        plt.plot(infected_data, label="Infected")
                        plt.plot(recovered_data, label="Recovered")
                        plt.plot(dead_data, label="Dead")
                        plt.xlabel('Number of Days')
                        plt.ylabel('Population Size')
                        plt.legend()
                        plt.show()

                    def heatmap():
                        sns.heatmap(data, cmap="YlGnBu", xticklabels=["Susceptible", "Infected", "Recovered", "Dead"],
                                    yticklabels=False)
                        plt.title("Simulation Results")
                        plt.xlabel("Categories")
                        plt.ylabel("Days")
                        plt.show()

            # If Influenza is chosen
            elif clicked.get() == 'Influenza':
                # Window of input if Influenza is chosen
                simulation_window = tk.Toplevel(window)
                simulation_window.title("Simulation")
                simulation_window.configure(bg="#4BC3B5")
                simulation_window.geometry("400x300")
                simulation_label = tk.Label(simulation_window, text="Influenza", font=('Gotham Black', 16),
                                            bg="#4BC3B5", fg="#454545")
                simulation_label.pack(padx=10, pady=10)

                Label1 = tk.Label(simulation_window, text="Enter population size: ", font=('Arial', 9),
                                  bg="#4BC3B5", fg="black")
                Label1.pack()
                POPULATION_SIZE = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
                POPULATION_SIZE.pack(padx=5, pady=5)

                Label2 = tk.Label(simulation_window, text="Enter initial infected count: ", font=('Arial', 9),
                                  bg="#4BC3B5", fg="black")
                Label2.pack()
                INITIAL_INFECTED_COUNT = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
                INITIAL_INFECTED_COUNT.pack(padx=5, pady=5)

                TRANSMISSION_PROB = 0.5
                RECOVERY_PROB = 0.7
                MORTALITY_PROB = 0.1

                button_simulation = customtkinter.CTkButton(master=simulation_window, command=lambda: on_button_click(),
                                                            text='Confirm',
                                                            fg_color=("dodger blue", "dodger blue"))
                button_simulation.pack(padx=40, pady=20)

                # Run the simulation
                def on_button_click():

                    results_window = tk.Toplevel(window)
                    results_window.title("Results")
                    results_window.configure(bg="#010402")
                    results_window.geometry("600x600")

                    scrollbar = ttk.Scrollbar(results_window, orient="vertical")
                    scrollbar.pack(side="right", fill="y")

                    canvas = tk.Canvas(results_window, bg="#010402", yscrollcommand=scrollbar.set)
                    canvas.pack(side="left", fill="both", expand=True)

                    frame = tk.Frame(canvas, bg="#010402")
                    canvas.create_window((0, 0), window=frame, anchor="n")

                    scrollbar.configure(command=canvas.yview)

                    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                    susceptible_count = int(POPULATION_SIZE.get()) - int(INITIAL_INFECTED_COUNT.get())
                    infected_count = int(INITIAL_INFECTED_COUNT.get())
                    recovered_count = 0
                    dead_count = 0

                    days = 0

                    # Initialize lists to store data
                    susceptible_data = []
                    infected_data = []

                    # Recovered data
                    recovered_data = []
                    dead_data = []

                    # Simulate disease spreading
                    while infected_count > 0:

                        # Increment days by 1
                        days += 1

                        # Calculate number of new infections and recoveries
                        new_infections = 0
                        recoveries = 0
                        deaths = 0
                        for i in range(infected_count):
                            if random.random() < float(TRANSMISSION_PROB):
                                new_infections += 1
                            if random.random() < float(RECOVERY_PROB):
                                recoveries += 1
                            if random.random() < float(MORTALITY_PROB):
                                deaths += 1

                        # This is to prevent new_infections variable from making susceptible_count negative
                        if new_infections > susceptible_count:
                            new_infections = susceptible_count

                        # This is to prevent new_infections variable from making infected_count negative
                        if new_infections > recoveries + deaths:
                            new_infections = recoveries + deaths

                        # Update data
                        susceptible_count -= new_infections
                        infected_count += new_infections - recoveries - deaths
                        recovered_count += min(recoveries, infected_count)
                        dead_count += min(deaths, infected_count)

                        # Store data for this day
                        susceptible_data.append(susceptible_count)
                        infected_data.append(infected_count)
                        recovered_data.append(recovered_count)
                        dead_data.append(dead_count)

                        data = [susceptible_data, infected_data, recovered_data, dead_data]
                        data = list(map(list, zip(*data)))

                        results = tk.Label(frame,
                                           text=f"Day {days}: Susceptible: {susceptible_count}, Infected: {infected_count}, Recovered: {recovered_count}, Dead: {dead_count}",
                                           font=('Arial', 10), bg="#010402", fg="#4BC3B5")
                        results.pack()

                    text_finish = tk.Label(frame, text="Disease spread complete. ", font=('Gotham Black', 12),
                                           bg="#010402", fg="#4BC3B5")
                    text_finish.pack()

                    text_finalres = tk.Label(frame, text="Final results: ", font=('Gotham Black', 10),
                                             bg="#010402", fg="#4BC3B5")
                    text_finalres.pack()

                    final_results = tk.Label(frame,
                                             text=f"It took {days} days to have {susceptible_count} unaffected, {infected_count} infected, {recovered_count} recovered, and {dead_count} dead.",
                                             font=('Gotham Black', 10),
                                             bg="#010402", fg="#4BC3B5")
                    final_results.pack()

                    Label6 = tk.Label(frame, text="Do you want to see the graph?", font=('Gotham Black', 10),
                                      bg="#010402", fg="white")
                    Label6.pack(padx=20, pady=20)

                    button_plot = customtkinter.CTkButton(master=frame, command=lambda: plot_data(), text='View Graph',
                                                          fg_color=("dodger blue", "dodger blue"))
                    button_plot.pack(padx=10, pady=10)

                    button_hm = customtkinter.CTkButton(master=frame, command=lambda: heatmap(), text='View Heatmap',
                                                        fg_color=("dodger blue", "dodger blue"))
                    button_hm.pack(padx=10, pady=10)

                    button_exit = customtkinter.CTkButton(master=frame, command=lambda: results_window.destroy(),
                                                          text='Exit',
                                                          fg_color=("dodger blue", "dodger blue"))
                    button_exit.pack(padx=10, pady=10)

                    def plot_data():
                        plt.plot(susceptible_data, label="Susceptible")
                        plt.plot(infected_data, label="Infected")
                        plt.plot(recovered_data, label="Recovered")
                        plt.plot(dead_data, label="Dead")
                        plt.xlabel('Number of Days')
                        plt.ylabel('Population Size')
                        plt.legend()
                        plt.show()

                    def heatmap():
                        sns.heatmap(data, cmap="YlGnBu", xticklabels=["Susceptible", "Infected", "Recovered", "Dead"],
                                    yticklabels=False)
                        plt.title("Simulation Results")
                        plt.xlabel("Categories")
                        plt.ylabel("Days")
                        plt.show()

        # Define options for the combobox
        options = ["Ebola", "Covid-19", "Common Cold", "Influenza"]

        # Create a ttk Combobox widget
        clicked = tk.StringVar()
        combobox = ttk.Combobox(preset_window, textvariable=clicked, values=options)
        combobox.pack(padx=5, pady=10)

        # Set default value of the combobox
        clicked.set("Select Preset")

        button_drop = customtkinter.CTkButton(master=preset_window, command=lambda: [selected(), preset_window.destroy()], text='Confirm',
                                          fg_color=("dodger blue", "dodger blue"))
        button_drop.pack()

    elif choice == "2":
        # Run Simulation of create your own
        simulation_window = tk.Toplevel(window)
        simulation_window.title("Simulation")
        simulation_window.configure(bg="#4BC3B5")
        simulation_window.geometry("600x400")
        simulation_label = tk.Label(simulation_window, text="Customize your own", font=('Gotham Black', 16),
                                    bg="#4BC3B5", fg="#000000")
        simulation_label.pack(padx=10, pady=10)

        Label1 = tk.Label(simulation_window, text="Enter population size: ", font=('Arial', 9),
                          bg="#4BC3B5", fg="black")
        Label1.pack()
        POPULATION_SIZE = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
        POPULATION_SIZE.pack(padx=5, pady=5)

        Label2 = tk.Label(simulation_window, text="Enter initial infected count: ", font=('Arial', 9),
                          bg="#4BC3B5", fg="black")
        Label2.pack()
        INITIAL_INFECTED_COUNT = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
        INITIAL_INFECTED_COUNT.pack(padx=5, pady=5)

        Label3 = tk.Label(simulation_window, text="Enter transmission rate ( 0-1 only ): ", font=('Arial', 9),
                          bg="#4BC3B5", fg="black")
        Label3.pack()
        TRANSMISSION_PROB = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
        TRANSMISSION_PROB.pack(padx=5, pady=5)

        Label4 = tk.Label(simulation_window, text="Enter recovery rate ( 0-1 only ): ", font=('Arial', 9),
                          bg="#4BC3B5", fg="black")
        Label4.pack()
        RECOVERY_PROB = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
        RECOVERY_PROB.pack(padx=5, pady=5)

        Label5 = tk.Label(simulation_window, text="Enter mortality rate ( 0-1 only ): ", font=('Arial', 9),
                          bg="#4BC3B5", fg="black")
        Label5.pack()
        MORTALITY_PROB = tk.Entry(simulation_window, font=('Arial', 9), bg="#4BC3B5", fg="black")
        MORTALITY_PROB.pack(padx=5, pady=5)

        button_simulation = customtkinter.CTkButton(master=simulation_window, command=lambda: on_button_click(), text='Confirm',
                                              fg_color=("dodger blue", "dodger blue"))
        button_simulation.pack(padx=40, pady=20)

        # Run the algorithm
        def on_button_click():

            results_window = tk.Toplevel(window)
            results_window.title("Results")
            results_window.configure(bg="#010402")
            results_window.geometry("620x720")

            scrollbar = ttk.Scrollbar(results_window, orient="vertical")
            scrollbar.pack(side="right", fill="y")

            canvas = tk.Canvas(results_window, bg="#010402", yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)

            frame = tk.Frame(canvas, bg="#010402")
            canvas.create_window((0, 0), window=frame, anchor="n")

            scrollbar.configure(command=canvas.yview)

            canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            susceptible_count = int(POPULATION_SIZE.get()) - int(INITIAL_INFECTED_COUNT.get())
            infected_count = int(INITIAL_INFECTED_COUNT.get())
            recovered_count = 0
            dead_count = 0

            days = 0

            # Initialize lists to store data
            susceptible_data = []
            infected_data = []

            # Recovered data
            recovered_data = []
            dead_data = []

            # Simulate disease spreading
            while infected_count > 0:

                # Increment days by 1
                days += 1

                # Calculate number of new infections and recoveries
                new_infections = 0
                recoveries = 0
                deaths = 0
                for i in range(infected_count):
                    if random.random() < float(TRANSMISSION_PROB.get()):
                        new_infections += 1
                    if random.random() < float(RECOVERY_PROB.get()):
                        recoveries += 1
                    if random.random() < float(MORTALITY_PROB.get()):
                        deaths += 1

                # This is to prevent new_infections variable from making susceptible_count negative
                if new_infections > susceptible_count:
                    new_infections = susceptible_count

                # This is to prevent new_infections variable from making infected_count negative
                if new_infections > recoveries + deaths:
                    new_infections = recoveries + deaths

                # Update data
                susceptible_count -= new_infections
                infected_count += new_infections - recoveries - deaths
                recovered_count += min(recoveries, infected_count)
                dead_count += min(deaths, infected_count)

                # Store data for this day
                susceptible_data.append(susceptible_count)
                infected_data.append(infected_count)
                recovered_data.append(recovered_count)
                dead_data.append(dead_count)

                data = [susceptible_data, infected_data, recovered_data, dead_data]
                data = list(map(list, zip(*data)))

                results = tk.Label(frame,
                                   text=f"Day {days}: Susceptible: {susceptible_count}, Infected: {infected_count}, Recovered: {recovered_count}, Dead: {dead_count}",
                                   font=('Arial', 10), bg="#010402", fg="#4BC3B5")
                results.pack()

            text_finish = tk.Label(frame, text="Disease spread complete. ", font=('Gotham Black', 12), bg="#010402", fg="#4BC3B5")
            text_finish.pack()

            text_finalres = tk.Label(frame, text="Final results: ", font=('Gotham Black', 10),
                                   bg="#010402", fg="#4BC3B5")
            text_finalres.pack()

            final_results = tk.Label(frame,
                               text=f"It took {days} days to have {susceptible_count} unaffected, {infected_count} infected, {recovered_count} recovered, and {dead_count} dead.",
                                     font=('Gotham Black', 10),
                                     bg="#010402", fg="#4BC3B5")
            final_results.pack()

            button_plot = customtkinter.CTkButton(master=frame, command=lambda: plot_data(), text='View Graph',
                                              fg_color=("dodger blue", "dodger blue"))
            button_plot.pack(padx=10, pady=10)

            button_hm = customtkinter.CTkButton(master=frame, command=lambda: heatmap(), text='View Heatmap',
                                                  fg_color=("dodger blue", "dodger blue"))
            button_hm.pack(padx=10, pady=10)

            button_exit = customtkinter.CTkButton(master=frame, command=lambda: results_window.destroy(), text='Exit',
                                                  fg_color=("dodger blue", "dodger blue"))
            button_exit.pack(padx=10, pady=10)

            def plot_data():
                plt.plot(susceptible_data, label="Susceptible")
                plt.plot(infected_data, label="Infected")
                plt.plot(recovered_data, label="Recovered")
                plt.plot(dead_data, label="Dead")
                plt.xlabel('Number of Days')
                plt.ylabel('Population Size')
                plt.legend()
                plt.show()

            def heatmap():
                sns.heatmap(data, cmap="YlGnBu", xticklabels=["Susceptible", "Infected", "Recovered", "Dead"],
                            yticklabels=False)
                plt.title("Simulation Results")
                plt.xlabel("Categories")
                plt.ylabel("Days")
                plt.show()



    elif choice == "3":
        dis_window = tk.Toplevel(window)
        dis_window.title("Infectious Diseases")
        dis_window.configure(bg="#4BC3B5")
        dis_window.geometry("600x400")

        scrollbar1 = ttk.Scrollbar(dis_window, orient="vertical")
        scrollbar1.pack(side="right", fill="y")

        canvas1 = tk.Canvas(dis_window, bg="#4BC3B5", yscrollcommand=scrollbar1.set)
        canvas1.pack(side="left", fill="both", expand=True)

        frame1 = tk.Frame(canvas1, bg="#4BC3B5")
        canvas1.create_window((0, 0), window=frame1, anchor="n")

        scrollbar1.configure(command=canvas1.yview)

        canvas1.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))

        dis_label = tk.Label(frame1, text="Infectious Diseases",
                               font=('Gotham Black', 12),
                               bg="#4BC3B5", fg="#000000")
        dis_label.pack(padx=10, pady=10)

        dis_text1 = tk.Label(frame1, text="An epidemic occurs when a disease spreads quickly through a population, "
                                          "\naffecting a significant number of people in a limited amount of time.",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        dis_text1.configure(justify="left", anchor="center")
        dis_text1.pack(pady=10)

        dis_text2 = tk.Label(frame1, text="Ebola"
                                            "\n\nEbola virus disease (EVD), formerly known as Ebola haemorrhagic fever, "
                                          "\nis a rare but severe, often fatal illness in humans. It is introduced into the human population "
                                          "\nthrough close contact with the blood, secretions, organs or other bodily fluids "
                                          "\nof a person who is sick with or has died from Ebola."
                                          "\n\nEstimated Transmission Rate: 0.4"
                                          "\nEstimated Recovery Rate: 0.2"
                                          "\nEstimated Mortality Rate: 0.4",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        dis_text2.configure(justify="center")
        dis_text2.pack(padx=10, pady=20)

        dis_text3 = tk.Label(frame1, text="Covid-19"
                                            "\n\nCoronavirus disease (COVID-19) is an infectious disease caused by the SARS-CoV-2 virus."
                                          "\nMost people infected with the virus will experience mild to moderate respiratory illness "
                                          "\nand recover without requiring special treatment. However, some will become seriously ill "
                                          "\nand require medical attention."
                                          "\n\nEstimated Transmission Rate: 0.6"
                                          "\nEstimated Recovery Rate: 0.4"
                                          "\nEstimated Mortality Rate: 0.2",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        dis_text3.configure(justify="center")
        dis_text3.pack(padx=10, pady=10)

        dis_text4 = tk.Label(frame1, text="Common Cold"
                                            "\n\nSore throat and runny nose are usually the first signs of a cold, "
                                          "\nfollowed by coughing and sneezing. Most people recover in about 7-10 days. "
                                            "\n\nEstimated Transmission Rate: 0.4"
                                          "\nEstimated Recovery Rate: 0.9"
                                          "\nEstimated Mortality Rate: 0.05",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        dis_text4.configure(justify="center")
        dis_text4.pack(padx=10, pady=10)

        dis_text5 = tk.Label(frame1, text="Influenza"
                                            "\n\nSore throat and runny nose are usually the first signs of a cold, "
                                          "\nfollowed by coughing and sneezing. Most people recover in about 7-10 days. "
                                            "\n\nEstimated Transmission Rate: 0.5"
                                          "\nEstimated Recovery Rate: 0.7"
                                          "\nEstimated Mortality Rate: 0.1",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        dis_text5.configure(justify="center")
        dis_text5.pack(padx=10, pady=10)

    elif choice == "4":
        # Display the guide
        guide_window = tk.Toplevel(window)
        guide_window.title("Guide")
        guide_window.configure(bg="#4BC3B5")
        guide_window.geometry("600x400")

        scrollbar1 = ttk.Scrollbar(guide_window, orient="vertical")
        scrollbar1.pack(side="right", fill="y")

        canvas1 = tk.Canvas(guide_window, bg="#4BC3B5", yscrollcommand=scrollbar1.set)
        canvas1.pack(side="left", fill="both", expand=True)

        frame1 = tk.Frame(canvas1, bg="#4BC3B5")
        canvas1.create_window((0, 0), window=frame1, anchor="n")

        scrollbar1.configure(command=canvas1.yview)

        canvas1.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))

        guide_label = tk.Label(frame1, text="This is a quick guide in using Epidemic Simulator.",
                               font=('Gotham Black', 12),
                               bg="#4BC3B5", fg="black")
        guide_label.pack(padx=10, pady=10)

        guide_text1 = tk.Label(frame1, text="When starting the simulation, "
                                                  "you will be prompted to enter population size, "
                                                  "\ninitial infected count, transmission rate, "
                                                  "recovery rate, and moratlity rate.",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        guide_text1.configure(justify="left", anchor="center")
        guide_text1.pack(pady=10)

        guide_text2 = tk.Label(frame1, text="Population size"
                                                  "\n\nPopulation size refers to the total number of individuals in a particular population. "
                                                  "\nIn this section, an integer must be entered. "
                                                  "An integer is a whole number \nthat can be positive, negative, or zero. "
                                                  "Positive numbers are recommended \nas this represents the number of the population.",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        guide_text2.configure(justify="center")
        guide_text2.pack(padx=10, pady=20)

        guide_text3 = tk.Label(frame1, text="Initial infected count"
                                                  "\n\nInitial infected count refers to the number of people who are initially "
                                                  "\ninfected with a particular disease or virus. It is recommended to enter \na positive integer.",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        guide_text3.configure(justify="center")
        guide_text3.pack(padx=10, pady=10)

        guide_text4 = tk.Label(frame1, text="Transmission rate"
                                                  "\n\nTransmission rate is a measure of how easily a disease spreads from "
                                            "\none person to another. A high transmission rate indicates that a \ndisease is spreading quickly "
                                            "and is more likely to cause a large outbreak, \nwhile a low transmission rate indicates "
                                            "that the disease \nis not spreading as easily and may be more easily controlled. "
                                            "\nEnter numbers 0-1."
                                            "\n0.1=10%\n0.2=20%\n0.3=30%\n...",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        guide_text4.configure(justify="center")
        guide_text4.pack(padx=10, pady=10)

        guide_text5 = tk.Label(frame1, text="Recovery rate"
                                            "\n\nRecovery rate refers to the proportion of individuals who "
                                            "\nrecover from the spread of disease. This can be expressed as a percentage, "
                                            "\nwith a higher recovery rate indicating that a larger proportion of individuals "
                                            "\nare able to recover from the disease or condition."
                                            "\nEnter numbers 0-1."
                                            "\n0.1=10%\n0.2=20%\n0.3=30%\n...",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        guide_text5.configure(justify="center")
        guide_text5.pack(padx=10, pady=10)

        guide_text6 = tk.Label(frame1, text="Mortality rate"
                                            "\n\nMortality rate is a measure of the number of deaths "
                                            "\nin a particular population over a specific period of time. "
                                            "\nEnter numbers 0-1."
                                            "\n0.1=10%\n0.2=20%\n0.3=30%\n...",
                               font=('Arial', 10),
                               bg="#4BC3B5", fg="black")
        guide_text6.configure(justify="center")
        guide_text6.pack(padx=10, pady=10)

    elif choice == "5":
        # Quit the program
        window.quit()

customtkinter.set_appearance_mode("System")

# Create the buttons for each option in the menu
button1 = customtkinter.CTkButton(master=window, command=lambda: handle_choice("1"), text='Select a preset',
                                  fg_color=("dodger blue", "dodger blue"))
button2 = customtkinter.CTkButton(master=window, command=lambda: handle_choice("2"), text='Create your own',
                                  fg_color=("dodger blue", "dodger blue"))
button3 = customtkinter.CTkButton(master=window, command=lambda: handle_choice("3"), text='Infectious Diseases',
                                  fg_color=("dodger blue", "dodger blue"))
button4 = customtkinter.CTkButton(master=window, command=lambda: handle_choice("4"), text='Guide',
                                  fg_color=("dodger blue", "dodger blue"))
button5 = customtkinter.CTkButton(master=window, command=lambda: handle_choice("5"), text='Quit',
                                  fg_color=("#1C2C54", "#1C2C54"))

# Place the buttons in the window
button1.pack(padx=5, pady=10)
button2.pack(padx=5, pady=10)
button3.pack(padx=5, pady=10)
button4.pack(padx=5, pady=10)
button5.pack(padx=5, pady=60)

# Start the main event loop
window.mainloop()