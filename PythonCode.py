import tkinter as tk

# Function to start the application
def start_app():
    try:
        print("Welcome to the BBC Ev Charging App.")
        print("Would you like to choose your car from our car library?")
        input1 = input("Type 'L' for library or 'B' to scan for a car: ")
        print(input1)
        # Checking library.
        if input1 == "L":
            print("Here is the car library:")
            print("Tesla")
            print("BMW")
            print("Mercedes")
            print("Other")
            input4 = input("Type the car you would like to choose: ")
            # Everything Tesla.
            if input4 == "Tesla":
                print("1. Tesla Model 3")
                print("2. Tesla Model S")
                print("3. Tesla Model X")
                print("4. Tesla Model Y")
                print("5. Tesla Model 3 Plus")
                print("6. Tesla Model S Plus")
                print("7. Tesla Model X Plus")
                print("8. Tesla Model Y Plus")
                print("9. Tesla Model 3 Plus Hybrid")
                print("10. Tesla Model S Plus Hybrid")
                print("11. Tesla Model X Plus Hybrid")
                print("12. Tesla Model Y Plus Hybrid")
                print("13. Tesla Model 3 Electric")
                print("14. Tesla Model S Electric")
                print("15. Tesla Model X Electric")
                print("16. Tesla Model Y Electric")
                print("Other")
                input2 = input("Type the number of the car you would like to choose: ")
                print(input2)
                if input2 == "1":
                    print("You have chosen the Tesla Model 3")
                # Add more conditions for other options...
            # Add similar sections for BMW, Mercedes, and Other options...
        else:
            print("Error, wrong value. Please restart the program.")
        # Checking Bluetooth
        if input1 == "B":
            print("Scanning for Car...")
            print("Found Car.")
            print("Would you like to connect to the device?")
            input2 = input("Type 'Y' for yes or 'N' for no: ")
            print(input2)
            if input2 == "Y":
                print("Connecting to the device...")
                print("Connected to the device.")
                print("Would you like to use the device?")
                input3 = input("Type 'Y' for yes or 'N' for no: ")
                print(input3)
                if input3 == "Y":
                    print("Using the device...")
                    print("Device is now used.")
                if input3 == "N":
                    print("Device is now not used.")
    except KeyboardInterrupt:
        print("Exiting the application...")
    except Exception as e:
        print("An error occurred:", e)

# Create the main application window
window = tk.Tk()
window.title('BBC Ev Charging App')

# Create buttons
start_button = tk.Button(window, text='Start App', command=start_app)
exit_button = tk.Button(window, text='Exit', command=window.quit)

# Add buttons to the window
start_button.pack(pady=10)
exit_button.pack(pady=10)

# Run the application
window.mainloop()
