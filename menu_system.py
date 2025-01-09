# menu_system.py
import os
import numpy as np


class MenuSystem:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from CSV file."""
        try:
            # Load settings from CSV file
            settings = np.genfromtxt('settings.csv', delimiter=',', skip_header=1)

            # Check if settings are correctly loaded
            if settings.size == 0:
                raise ValueError("Settings file is empty or has an invalid format.")

            return {
                'marker_length': settings[0],  # First column
                'focal_length': settings[1],  # Second column
                'threshold': settings[2]  # Third column
            }
        except Exception as e:
            print(f"Error loading settings from file: {e}")
            # Default settings in case of error
            return {
                'marker_length': 10.0,
                'focal_length': 50.0,
                'threshold': 0.5
            }

    def save_settings(self):
        """Save settings to CSV file."""
        try:
            settings_array = np.array(
                [[self.settings['marker_length'], self.settings['focal_length'], self.settings['threshold']]])
            header = "marker_length,focal_length,threshold"
            np.savetxt('settings.csv', settings_array, delimiter=',', header=header, comments='', fmt='%f')
            print("Settings saved successfully.")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_main_menu(self):
        self.clear_screen()
        print("=== Object Measurement System ===")
        print("1. Start Measurement")
        print("2. Camera Calibration")
        print("3. Settings")
        print("4. Exit")
        return input("Enter your choice (1-4): ")

    def show_camera_menu(self):
        self.clear_screen()
        print("=== Camera Selection ===")
        print("1. Default Camera")
        print("2. IP Webcam")
        while True:
            choice = input("Enter choice (1 or 2): ")
            if choice in ['1', '2']:
                return choice
            print("Invalid choice. Please try again.")

    def show_settings_menu(self):
        self.clear_screen()
        print("=== Settings ===")
        print(f"1. Marker Length (current: {self.settings['marker_length']} cm)")
        print(f"2. Focal Length (current: {self.settings['focal_length']})")
        print(f"3. Threshold Value (current: {self.settings['threshold']})")
        print("4. Back to Main Menu")

        choice = input("Enter your choice (1-4): ")

        if choice == '4':
            return

        if choice in ['1', '2', '3']:
            setting_keys = ['marker_length', 'focal_length', 'threshold']
            key = setting_keys[int(choice) - 1]
            try:
                new_value = float(input(f"Enter new value for {key}: "))
                self.settings[key] = new_value
                self.save_settings()  # Save settings after modification
                print(f"{key} updated successfully!")
            except ValueError:
                print("Invalid input. Setting not updated.")

        input("Press Enter to continue...")
