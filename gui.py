import serial
import time
import tkinter as tk

# ---------------- SERIAL ----------------
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# ---------------- COLORS ----------------
BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
ACCENT = "#14b8a6"
GREEN_ON = "#22c55e"
RED_OFF = "#ef4444"
TEXT_COLOR = "#f8fafc"

# ---------------- SEND COMMAND ----------------
def send_command(cmd):
    arduino.write((cmd + '\n').encode())

# ---------------- UPDATE DATA ----------------
def update_data():
    if arduino.in_waiting:
        line = arduino.readline().decode().strip()
        try:
            parts = line.split(',')
            data = {}
            for part in parts:
                key, value = part.split(':')
                data[key] = value

            ph_value.config(text=data["PH"])
            tds_value.config(text=data["TDS"])
            temp_value.config(text=data["TEMP"] + " °C")
            hum_value.config(text=data["HUM"] + " %")

            # GREEN = ON
            if data["PUMP"] == "1":
                pump_indicator.config(bg=GREEN_ON)
                pump_status.config(text="ON", fg=GREEN_ON)
            else:
                pump_indicator.config(bg=RED_OFF)
                pump_status.config(text="OFF", fg=RED_OFF)

            if data["FAN"] == "1":
                fan_indicator.config(bg=GREEN_ON)
                fan_status.config(text="ON", fg=GREEN_ON)
            else:
                fan_indicator.config(bg=RED_OFF)
                fan_status.config(text="OFF", fg=RED_OFF)

        except:
            pass

    root.after(1000, update_data)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Hydroponics Monitoring System")
root.configure(bg=BG_COLOR)
root.state("zoomed")   # Fullscreen for Windows
root.bind("<Escape>", lambda e: root.state("normal"))

# Title
title = tk.Label(root, text="HYDROPONICS CONTROL DASHBOARD",
                 font=("Segoe UI", 26, "bold"),
                 bg=BG_COLOR, fg=ACCENT)
title.pack(pady=20)

# Main container
container = tk.Frame(root, bg=BG_COLOR)
container.pack(expand=True, fill="both", padx=40, pady=20)

# Make responsive columns
container.columnconfigure(0, weight=3)
container.columnconfigure(1, weight=2)

# ---------------- SENSOR CARD ----------------
sensor_card = tk.Frame(container, bg=CARD_COLOR)
sensor_card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

tk.Label(sensor_card, text="Sensor Readings",
         font=("Segoe UI", 18, "bold"),
         bg=CARD_COLOR, fg=TEXT_COLOR).pack(pady=15)

def sensor_row(parent, label_text):
    row = tk.Frame(parent, bg=CARD_COLOR)
    row.pack(fill="x", pady=15, padx=40)

    tk.Label(row, text=label_text,
             font=("Segoe UI", 16),
             bg=CARD_COLOR, fg=TEXT_COLOR).pack(side="left")

    value = tk.Label(row, text="--",
                     font=("Segoe UI", 22, "bold"),
                     bg=CARD_COLOR, fg=ACCENT)
    value.pack(side="right")

    return value

ph_value = sensor_row(sensor_card, "pH Level")
tds_value = sensor_row(sensor_card, "EC / TDS")
temp_value = sensor_row(sensor_card, "Temperature")
hum_value = sensor_row(sensor_card, "Humidity")

# ---------------- CONTROL CARD ----------------
control_card = tk.Frame(container, bg=CARD_COLOR)
control_card.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

tk.Label(control_card, text="System Controls",
         font=("Segoe UI", 18, "bold"),
         bg=CARD_COLOR, fg=TEXT_COLOR).pack(pady=15)

# Pump Section
pump_section = tk.Frame(control_card, bg=CARD_COLOR)
pump_section.pack(pady=20)

tk.Label(pump_section, text="PUMP",
         font=("Segoe UI", 16, "bold"),
         bg=CARD_COLOR, fg=TEXT_COLOR).pack()

pump_indicator = tk.Label(pump_section, width=6, height=2, bg=RED_OFF)
pump_indicator.pack(pady=5)

pump_status = tk.Label(pump_section, text="OFF",
                       font=("Segoe UI", 14, "bold"),
                       bg=CARD_COLOR, fg=RED_OFF)
pump_status.pack()

tk.Button(pump_section, text="ON", width=12,
          command=lambda: send_command("PUMP_ON")).pack(pady=5)

tk.Button(pump_section, text="OFF", width=12,
          command=lambda: send_command("PUMP_OFF")).pack(pady=5)

# Fan Section
fan_section = tk.Frame(control_card, bg=CARD_COLOR)
fan_section.pack(pady=30)

tk.Label(fan_section, text="FAN",
         font=("Segoe UI", 16, "bold"),
         bg=CARD_COLOR, fg=TEXT_COLOR).pack()

fan_indicator = tk.Label(fan_section, width=6, height=2, bg=RED_OFF)
fan_indicator.pack(pady=5)

fan_status = tk.Label(fan_section, text="OFF",
                      font=("Segoe UI", 14, "bold"),
                      bg=CARD_COLOR, fg=RED_OFF)
fan_status.pack()

tk.Button(fan_section, text="ON", width=12,
          command=lambda: send_command("FAN_ON")).pack(pady=5)

tk.Button(fan_section, text="OFF", width=12,
          command=lambda: send_command("FAN_OFF")).pack(pady=5)

tk.Button(fan_section, text="AUTO", width=12,
          command=lambda: send_command("FAN_AUTO")).pack(pady=5)

update_data()
root.mainloop()
