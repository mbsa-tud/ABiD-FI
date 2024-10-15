import tkinter as tk
from tkinter import ttk, filedialog
import json


class ConfigEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Config Editor")
        self.geometry("600x600")
        self.config_data = config_data

        # Main container frame
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Title label
        title_label = ttk.Label(container, text="Edit External Faults Config", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Notebook (tabs) for Faults
        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)

        # General settings frame
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General Settings")
        self.create_general_settings_frame(general_frame)

        # Faults frame
        faults_frame = ttk.Frame(notebook)
        notebook.add(faults_frame, text="Faults")
        self.create_faults_frame(faults_frame)

        # Save and load buttons
        save_button = ttk.Button(self, text="Save Config", command=self.save_config)
        save_button.pack(pady=10)

    def create_general_settings_frame(self, frame):
        """Creates general settings fields in the 'General Settings' tab"""
        settings = self.config_data["ExternalFaults"]
        row = 0

        # Add general fields like selected, compare_all, etc.
        for key in ["selected", "compare_all", "all_severities", "mixed", "keep_originals"]:
            label = ttk.Label(frame, text=f"{key.replace('_', ' ').title()}:")
            label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(frame)
            entry.insert(0, str(settings[key]))
            entry.grid(row=row, column=1, padx=5, pady=5)

            # Save reference for later
            setattr(self, f"{key}_entry", entry)
            row += 1

        # Image Directory
        label = ttk.Label(frame, text="Image Directory:")
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.image_dir_entry = ttk.Entry(frame)
        self.image_dir_entry.insert(0, settings["image_dir"])
        self.image_dir_entry.grid(row=row, column=1, padx=5, pady=5)

        # Add a button to browse directory
        browse_button = ttk.Button(frame, text="Browse", command=self.browse_image_dir)
        browse_button.grid(row=row, column=2, padx=5, pady=5)

    def create_faults_frame(self, frame):
        """Creates fault settings fields in the 'Faults' tab"""
        faults = self.config_data["ExternalFaults"]["Faults"]

        for fault_name, fault_data in faults.items():
            # Create a collapsible section for each fault
            fault_frame = ttk.LabelFrame(frame, text=fault_name.replace('_', ' ').title())
            fault_frame.pack(fill="both", padx=10, pady=5)

            # Initialize a row counter for placing widgets correctly
            row = 0

            # Add fields for 'category', 'active', 'probability', 'severity'
            for key, value in fault_data.items():
                label = ttk.Label(fault_frame, text=f"{key.title()}:")
                label.grid(row=row, column=0, padx=5, pady=2, sticky="w")

                entry = ttk.Entry(fault_frame)
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, padx=5, pady=2)

                # Save the reference to the entry widget
                setattr(self, f"{fault_name}_{key}_entry", entry)

                # Increment the row counter for each new label-entry pair
                row += 1

    def browse_image_dir(self):
        """Browse for image directory"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.image_dir_entry.delete(0, tk.END)
            self.image_dir_entry.insert(0, folder_selected)

    def save_config(self):
        """Saves the current configuration into the JSON file"""
        # Update general settings
        settings = self.config_data["ExternalFaults"]
        for key in ["selected", "compare_all", "all_severities", "mixed", "keep_originals"]:
            settings[key] = int(getattr(self, f"{key}_entry").get())
        settings["image_dir"] = self.image_dir_entry.get()

        # Update faults
        faults = settings["Faults"]
        for fault_name in faults.keys():
            for key in faults[fault_name].keys():
                entry_value = getattr(self, f"{fault_name}_{key}_entry").get()
                faults[fault_name][key] = int(entry_value)

        # Save to file (or you can use the json dump to save into file)
        with open("config.json", "w") as file:
            json.dump(self.config_data, file, indent=4)
        print("Config saved to config.json")


if __name__ == "__main__":
    # Sample config data to initialize the GUI
    config_data = {
        "ExternalFaults": {
            "selected": 1,
            "compare_all": 1,
            "all_severities": 1,
            "mixed": 0,
            "keep_originals": 0,
            "image_dir": "Test_Images",
            "Faults": {
                "gaussian_noise": {
                    "category": "noise",
                    "active": 1,
                    "probability": 1,
                    "severity": 5
                },
                "shot_noise": {
                    "category": "noise",
                    "active": 0,
                    "probability": 1,
                    "severity": 3
                },
                "impulse_noise": {
                    "category": "noise",
                    "active": 0,
                    "probability": 1,
                    "severity": 3
                },
                "defocus_blur": {
                    "category": "blur",
                    "active": 0,
                    "probability": 1,
                    "severity": 3
                },
                "motion_blur": {
                    "category": "blur",
                    "active": 0,
                    "probability": 1,
                    "severity": 3
                },
                # Add more faults here as needed...
            }
        }
    }

    # Create and run the application
    app = ConfigEditorApp()
    app.mainloop()