import tkinter
from tkinter import ttk
from tkinter import messagebox
from weather_forecast import WeatherForecast
import datetime

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def enter_data():
    date = date_entry.get()
    selected_variables = []

    if max_temp_var.get():
        selected_variables.append("max_temp")
    if min_temp_var.get():
        selected_variables.append("min_temp")
    if mean_temp_var.get():
        selected_variables.append("mean_temp")

    if date and selected_variables:
        if is_valid_date(date):
            weather = WeatherForecast('london_weather.csv')
            weather_info_box.delete(1.0, tkinter.END)  # Clear previous weather information
            weather_info_box.config(state=tkinter.NORMAL)  # Enable the weather information box
            weather_info_box.insert(tkinter.END, "Weather forecast for " + str(date) + "\n")
            for variable in selected_variables:
                weather_data = weather.get_weather_data(date, variable)
                weather_info_box.insert(tkinter.END, variable + ": " + str(weather_data[variable]) + "\n")
            weather_info_box.insert(tkinter.END, "------------------------------------------\n")
            weather_info_box.config(state=tkinter.DISABLED)  # Disable the weather information box
        else:
            tkinter.messagebox.showwarning(title="Error", message="Invalid date format. Please enter a date in the format YYYY-MM-DD.")
    else:
        tkinter.messagebox.showwarning(title="Error", message="Please enter a date and select at least one weather variable.")


def toggle_weather_info():
    if weather_day_var.get():
        for widget in weather_info_frame.winfo_children():
            widget.config(state=tkinter.NORMAL)
    else:
        for widget in weather_info_frame.winfo_children():
            if widget != date_label:
                widget.config(state=tkinter.DISABLED)

window = tkinter.Tk()
window.title('Tra cứu và dự báo thời tiết')
window.iconbitmap('Images/weather-news.ico')

frame = tkinter.Frame(window)
frame.pack()

# Options
options_frame = tkinter.LabelFrame(frame, text="Options")
options_frame.grid(row=0, column=0, padx=20, pady=10)


weather_day_var = tkinter.BooleanVar()
weather_day_check = tkinter.Checkbutton(options_frame, text="Tra cứu thời tiết theo ngày", variable=weather_day_var, command=toggle_weather_info)
weather_day_check.grid(row=0, column=0, sticky="w")

blank_check = tkinter.Checkbutton(options_frame, text="Dự báo thời tiết")
blank_check.grid(row=1, column=0, sticky="w")

for widget in options_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Weather Info
weather_info_frame = tkinter.LabelFrame(frame, text="Weather Information")
weather_info_frame.grid(row=1, column=0, padx=20, pady=10)

date_label = tkinter.Label(weather_info_frame, text="Date (YYYY-MM-DD)")
date_entry = tkinter.Entry(weather_info_frame)
date_label.grid(row=0, column=0)
date_entry.grid(row=1, column=0)

max_temp_var = tkinter.BooleanVar()
min_temp_var = tkinter.BooleanVar()
mean_temp_var = tkinter.BooleanVar()

max_temp_check = tkinter.Checkbutton(weather_info_frame, text="Max Temp", variable=max_temp_var)
min_temp_check = tkinter.Checkbutton(weather_info_frame, text="Min Temp", variable=min_temp_var)
mean_temp_check = tkinter.Checkbutton(weather_info_frame, text="Mean Temp", variable=mean_temp_var)

max_temp_check.grid(row=2, column=0, sticky="w")
min_temp_check.grid(row=2, column=1, sticky="w")
mean_temp_check.grid(row=2, column=2, sticky="w")

for widget in weather_info_frame.winfo_children():
    if widget != date_label:
        widget.grid_configure(padx=10, pady=5)

# Weather Info Box
weather_info_box = tkinter.Text(frame, width=50, height=10, state=tkinter.DISABLED)
weather_info_box.grid(row=2, column=0, padx=20, pady=10)

# Submit button
enter_data_button = tkinter.Button(frame, text="Enter", command=enter_data)
enter_data_button.grid(row=3, column=0, padx=20, pady=10)

# Disable weather info widgets initially
toggle_weather_info()

window.mainloop()