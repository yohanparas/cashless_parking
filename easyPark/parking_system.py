# parking_system.py
import tkinter as tk
import hashlib
from datetime import datetime
from tkinter import ttk, messagebox
from database import Database
from vehicle import Vehicle
from parking_spot import ParkingLot

class ParkingSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EasyPark")
        self.geometry("800x600")
        self.parking_lot = ParkingLot(10)
        self.rates = {"car": 5, "motorcycle": 3}
        self.db = Database()
        self.current_user = None
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.login_frame = ttk.Frame(self.notebook)
        self.signup_frame = ttk.Frame(self.notebook)
        self.parking_frame = ttk.Frame(self.notebook)
        self.watch_frame = ttk.Frame(self.notebook)
        self.exit_frame = ttk.Frame(self.notebook)
        self.account_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.signup_frame, text="Sign Up")
        self.notebook.add(self.parking_frame, text="Park Vehicle")
        self.notebook.add(self.watch_frame, text="Watch Spots")
        self.notebook.add(self.exit_frame, text="Exit Parking")
        self.notebook.add(self.account_frame, text="Account")

        self.create_login_widgets()
        self.create_signup_widgets()
        self.create_parking_widgets()
        self.create_watch_widgets()
        self.create_exit_widgets()
        self.create_account_widgets()

    def create_login_widgets(self): #login tab
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.login_username_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.login_username_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.login_password_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.login_password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def create_signup_widgets(self): #signup tab
        ttk.Label(self.signup_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.signup_username_var = tk.StringVar()
        ttk.Entry(self.signup_frame, textvariable=self.signup_username_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.signup_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.signup_password_var = tk.StringVar()
        ttk.Entry(self.signup_frame, textvariable=self.signup_password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.signup_frame, text="Sign Up", command=self.signup).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def create_parking_widgets(self): #show available spots
        ttk.Label(self.parking_frame, text="Available Spots:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.available_spots_var = tk.StringVar()
        self.available_spots_dropdown = ttk.Combobox(self.parking_frame, textvariable=self.available_spots_var)
        self.available_spots_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.update_available_spots()

        ttk.Label(self.parking_frame, text="Vehicle Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.vehicle_type_var = tk.StringVar(value="car")
        ttk.Radiobutton(self.parking_frame, text="Car", variable=self.vehicle_type_var, value="car").grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.parking_frame, text="Motorcycle", variable=self.vehicle_type_var, value="motorcycle").grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(self.parking_frame, text="License Plate:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.license_plate_var = tk.StringVar()
        ttk.Entry(self.parking_frame, textvariable=self.license_plate_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.parking_frame, text="Duration (hours):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.duration_var = tk.StringVar(value="1")
        ttk.Spinbox(self.parking_frame, from_=1, to=24, textvariable=self.duration_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.parking_frame, text="Calculate Cost", command=self.calculate_cost).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.cost_var = tk.StringVar()
        ttk.Label(self.parking_frame, textvariable=self.cost_var).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(self.parking_frame, text="Park Vehicle", command=self.park_vehicle).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def create_watch_widgets(self):
        self.watch_tree = ttk.Treeview(self.watch_frame, columns=("Spot", "Status"), show="headings")
        self.watch_tree.heading("Spot", text="Spot")
        self.watch_tree.heading("Status", text="Status")
        self.watch_tree.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(self.watch_frame, text="Refresh", command=self.update_watch_list).grid(row=2, column=0, padx=5, pady=5)

        self.update_watch_list()

    def create_exit_widgets(self):
        ttk.Label(self.exit_frame, text="Occupied Spots:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.exit_spots_var = tk.StringVar()
        self.exit_spots_dropdown = ttk.Combobox(self.exit_frame, textvariable=self.exit_spots_var)
        self.exit_spots_dropdown.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.exit_frame, text="Calculate Fee", command=self.calculate_exit_fee).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.exit_fee_var = tk.StringVar()
        ttk.Label(self.exit_frame, textvariable=self.exit_fee_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(self.exit_frame, text="Pay and Exit", command=self.pay_and_exit).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.update_exit_spots()

    def create_account_widgets(self): #account
        self.balance_var = tk.StringVar()
        ttk.Label(self.account_frame, text="Cash Balance:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.account_frame, textvariable=self.balance_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.account_frame, text="Add Funds:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.add_funds_var = tk.StringVar()
        ttk.Entry(self.account_frame, textvariable=self.add_funds_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.account_frame, text="Add Funds (GCash)", command=self.add_funds_gcash).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.account_frame, text="Add Funds (Card)", command=self.add_funds_card).grid(row=2, column=1, padx=5, pady=5)

        # Logout
        ttk.Button(self.account_frame, text="Logout", command=self.logout).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        username = self.login_username_var.get()
        password = self.login_password_var.get()
        user = self.db.get_user(username)
        if user and user.password_hash == self.hash_password(password):
            self.current_user = user
            self.update_balance_display()
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.notebook.select(2)  # Switch to parking tab
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup(self):
        username = self.signup_username_var.get()
        password = self.signup_password_var.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        if self.db.get_user(username):
            messagebox.showerror("Error", "Username already exists")
            return
        password_hash = self.hash_password(password)
        self.db.add_user(username, password_hash)
        messagebox.showinfo("Success", "Account created successfully")
        self.notebook.select(0)  # Switch to login tab

    def logout(self):
        self.current_user = None  # Clear the logged-in user
        messagebox.showinfo("Logout", "You have been logged out successfully.")
        self.notebook.select(0)  # Switch back to the login tab

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def update_balance_display(self):
        if self.current_user:
            self.balance_var.set(f"${self.current_user.balance:.2f}")

    def add_funds_gcash(self):
        self.add_funds("GCash")

    def add_funds_card(self):
        self.add_funds("Card")

    def add_funds(self, method):
        if not self.current_user:
            messagebox.showerror("Error", "Please log in first")
            return
        try:
            amount = float(self.add_funds_var.get())
            if amount <= 0:
                raise ValueError
            self.current_user.balance += amount
            self.db.update_balance(self.current_user.username, self.current_user.balance)
            self.update_balance_display()
            messagebox.showinfo("Success", f"${amount:.2f} added to your account via {method}")
            self.add_funds_var.set("")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def update_available_spots(self):
        available_spots = self.parking_lot.get_available_spots()
        self.available_spots_dropdown['values'] = [spot.id for spot in available_spots]
        if available_spots:
            self.available_spots_dropdown.set(available_spots[0].id)
        else:
            self.available_spots_dropdown.set('')

    def calculate_cost(self):
        try:
            duration = int(self.duration_var.get())
            vehicle_type = self.vehicle_type_var.get()
            cost = self.rates[vehicle_type] * duration
            self.cost_var.set(f"Estimated Cost: ${cost:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration.")

    def park_vehicle(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please log in first")
            return
        spot_id = self.available_spots_var.get()
        vehicle_type = self.vehicle_type_var.get()
        license_plate = self.license_plate_var.get()
        try:
            duration = int(self.duration_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration.")
            return

        if not spot_id or not license_plate:
            messagebox.showerror("Error", "Please select a spot and enter a license plate.")
            return

        cost = self.rates[vehicle_type] * duration
        if self.current_user.balance < cost:
            messagebox.showerror("Error", "Insufficient balance. Please add funds to your account.")
            return

        vehicle = Vehicle(vehicle_type, license_plate)
        self.parking_lot.occupy_spot(spot_id, vehicle, duration, self.current_user)
        messagebox.showinfo("Success", f"Vehicle parked in spot {spot_id}.")
        self.update_available_spots()
        self.update_watch_list()
        self.update_exit_spots()

    def update_watch_list(self):
        for item in self.watch_tree.get_children():
            self.watch_tree.delete(item)

        for spot in self.parking_lot.spots:
            status = "Occupied" if spot.is_occupied else "Available"
            self.watch_tree.insert("", "end", values=(spot.id, status))

    def update_exit_spots(self):
        occupied_spots = [spot.id for spot in self.parking_lot.spots if spot.is_occupied]
        self.exit_spots_dropdown['values'] = occupied_spots
        if occupied_spots:
            self.exit_spots_dropdown.set(occupied_spots[0])
        else:
            self.exit_spots_dropdown.set('')

    def calculate_exit_fee(self):
        spot_id = self.exit_spots_var.get()
        if not spot_id:
            messagebox.showerror("Error", "Please select an occupied spot.")
            return

        spot = next((spot for spot in self.parking_lot.spots if spot.id == spot_id), None)
        if spot and spot.is_occupied:
            elapsed_time = datetime.now() - spot.start_time
            hours_parked = elapsed_time.total_seconds() / 3600
            fee = self.rates[spot.vehicle.type] * hours_parked
            self.exit_fee_var.set(f"Parking Fee: ${fee:.2f}")
        else:
            messagebox.showerror("Error", "Invalid spot selection.")

    def pay_and_exit(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please log in first")
            return
        spot_id = self.exit_spots_var.get()
        if not spot_id:
            messagebox.showerror("Error", "Please select an occupied spot.")
            return

        spot = next((spot for spot in self.parking_lot.spots if spot.id == spot_id), None)
        if spot and spot.is_occupied and spot.user == self.current_user:
            elapsed_time = datetime.now() - spot.start_time
            hours_parked = elapsed_time.total_seconds() / 3600
            fee = self.rates[spot.vehicle.type] * hours_parked

            if self.current_user.balance < fee:
                messagebox.showerror("Error", "Insufficient balance. Please add funds to your account.")
                return

            self.current_user.balance -= fee
            self.db.update_balance(self.current_user.username, self.current_user.balance)
            self.update_balance_display()
            self.parking_lot.vacate_spot(spot_id)
            messagebox.showinfo("Success", f"Vehicle has exited from spot {spot_id}. ${fee:.2f} deducted from your account.")
            self.update_available_spots()
            self.update_watch_list()
            self.update_exit_spots()
            self.exit_fee_var.set("")
        else:
            messagebox.showerror("Error", "Invalid spot selection or you don't have permission to exit this vehicle.")
