import random
import matplotlib.pyplot as plt

while True:
  # Print the start menu
  print("1. Input for simulation")
  print("2. Guide")
  print("3. Quit")

  # Get the user's choice
  choice = input("Enter your choice: ")

  # Handle the user's choice
  if choice == "1":
    # Run the simulation
    # Define population size
    while True:
        try:
            POPULATION_SIZE = int(input("Enter population size: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.".center(160))

    # Define initial number of infected people
    while True:
        try:
            INITIAL_INFECTED_COUNT = int(input("Enter initial infected count: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Define transmission probability
    while True:
        try:
            TRANSMISSION_PROB = float(input("Enter transmission rate ( 0-1 only ): "))
            if TRANSMISSION_PROB > 1 or TRANSMISSION_PROB < 0:
                print("Invalid input. Please enter a value between 0 and 1.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Define recovery probability
    while True:
        try:
            RECOVERY_PROB = float(input("Enter recovery rate ( 0-1 only ): "))
            if RECOVERY_PROB > 1 or RECOVERY_PROB < 0:
                print("Invalid input. Please enter a value between 0 and 1.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Define mortality probability
    while True:
        try:
            MORTALITY_PROB = float(input("Enter mortality rate ( 0-1 only ): "))
            if MORTALITY_PROB > 1 or MORTALITY_PROB < 0:
                print("Invalid input. Please enter a value between 0 and 1.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Initialize variables
    susceptible_count = POPULATION_SIZE - INITIAL_INFECTED_COUNT
    infected_count = INITIAL_INFECTED_COUNT
    recovered_count = 0
    dead_count = 0

    days = 0

    # Initialize lists to store data
    susceptible_data = []
    infected_data = []
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
            if random.random() < TRANSMISSION_PROB:
                new_infections += 1
            if random.random() < RECOVERY_PROB:
                recoveries += 1
            if random.random() < MORTALITY_PROB:
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

        # Store data
        susceptible_data.append(susceptible_count)
        infected_data.append(infected_count)
        recovered_data.append(recovered_count)
        dead_data.append(dead_count)

        # Print current status
        print(
            f"Day {days}: Susceptible: {susceptible_count}, Infected: {infected_count}, Recovered: {recovered_count}, Dead: {dead_count}")
    # Print final status
    print("Disease spread complete. ")
    print("Final results: ")
    print(
        f"It took {days} days to have {susceptible_count} unaffected, {infected_count} infected, {recovered_count} recovered, and {dead_count} dead.")

    # Plot the final results
    # Ask the user if they want to see the plot
    plot_choice = input("Do you want to see the plot? (y/n) ".center(160))
    if plot_choice == "y":
        plt.plot(susceptible_data, label="Susceptible")
        plt.plot(infected_data, label="Infected")
        plt.plot(recovered_data, label="Recovered")
        plt.plot(dead_data, label="Dead")
        plt.xlabel('Number of Days')
        plt.ylabel('Population Size')
        plt.legend()
        plt.show()
    pass
  elif choice == "2":
    # Display the guide
    print("Eto guide.")
    pass
  elif choice == "3":
    # Quit the program
    break
  else:
    # Print an error message if the user's choice is invalid
    print("Invalid choice. Please try again.")

