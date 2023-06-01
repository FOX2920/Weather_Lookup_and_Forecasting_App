import tkinter
from tkinter import ttk
from tkinter import messagebox
from weather_forecast import WeatherForecast
import datetime


def is_valid_date(date_str):
    """
    Kiểm tra xem một chuỗi ngày có đúng định dạng YYYY-MM-DD hay không.

    Tham số:
    - date_str (str): Chuỗi ngày cần kiểm tra.

    Trả về:
    - valid (bool): True nếu đúng định dạng, False nếu không.
    """
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def enter_data():
    """
    Xử lý sự kiện nhấn nút "Enter" để tra cứu và hiển thị thông tin thời tiết.

    Sử dụng các giá trị ngày và biến thời tiết được nhập từ giao diện người dùng.
    Hiển thị thông báo lỗi nếu ngày hoặc biến thời tiết không hợp lệ.
    """
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


def enter_forecast_data():
    """
    Xử lý sự kiện nhấn nút "Enter" để dự báo thời tiết cho một số ngày trong tương lai.

    Sử dụng giá trị số ngày cần dự báo từ giao diện người dùng.
    Hiển thị thông báo lỗi nếu số ngày không hợp lệ.
    """
    try:
        n = int(forecast_days_entry.get())
        if n > 0:
            weather = WeatherForecast('london_weather.csv')
            forecast_data = weather.get_weather_data_details(n)
            forecast_info_box.delete(1.0, tkinter.END)  # Clear previous forecast information
            forecast_info_box.config(state=tkinter.NORMAL)  # Enable the forecast information box
            forecast_info_box.insert(tkinter.END, "Weather forecast for the next " + str(n) + " days:\n")
            for data in forecast_data:
                forecast_info_box.insert(tkinter.END, "Date: " + str(data['date']) + "\n")
                forecast_info_box.insert(tkinter.END, "Temp: " + str(data['mean_temp']) + "\n")
                forecast_info_box.insert(tkinter.END, "----------------------------------------\n")
            forecast_info_box.config(state=tkinter.DISABLED)  # Disable the forecast information box
        else:
            tkinter.messagebox.showwarning(title="Error", message="Invalid number of days. Please enter a positive integer.")
    except ValueError:
        tkinter.messagebox.showwarning(title="Error", message="Invalid number of days. Please enter a positive integer.")


def toggle_forecast_info():
    """
    Hàm này được gọi khi người dùng bật hoặc tắt thông tin dự báo thời tiết.

    Nếu checkbox "Dự báo thời tiết" được chọn, các thành phần liên quan đến dự báo thời tiết sẽ được kích hoạt.
    Nếu checkbox không được chọn, các thành phần liên quan đến dự báo thời tiết sẽ bị vô hiệu hóa.

    Tham số:
        Không có tham số đầu vào.

    Trả về:
        Không có giá trị trả về.
    """
    if forecast_var.get() == 1:
        forecast_days_label.config(state=tkinter.NORMAL)
        forecast_days_entry.config(state=tkinter.NORMAL)
        forecast_enter_button.config(state=tkinter.NORMAL)
        forecast_info_box.config(state=tkinter.NORMAL)
    else:
        forecast_days_label.config(state=tkinter.DISABLED)
        forecast_days_entry.config(state=tkinter.DISABLED)
        forecast_enter_button.config(state=tkinter.DISABLED)
        forecast_info_box.config(state=tkinter.DISABLED)


def toggle_weather_info():
    """
    Hàm này được gọi khi người dùng bật hoặc tắt thông tin thời tiết.

    Nếu checkbox "Thông tin thời tiết" được chọn, các thành phần liên quan đến thông tin thời tiết sẽ được kích hoạt.
    Nếu checkbox không được chọn, các thành phần liên quan đến thông tin thời tiết sẽ bị vô hiệu hóa.

    Tham số:
        Không có tham số đầu vào.

    Trả về:
        Không có giá trị trả về.
    """
    if weather_day_var.get() == 1:
        date_label.config(state=tkinter.NORMAL)
        date_entry.config(state=tkinter.NORMAL)
        max_temp_check.config(state=tkinter.NORMAL)
        min_temp_check.config(state=tkinter.NORMAL)
        mean_temp_check.config(state=tkinter.NORMAL)
        enter_button.config(state=tkinter.NORMAL)
        weather_info_box.config(state=tkinter.NORMAL)
    else:
        date_label.config(state=tkinter.DISABLED)
        date_entry.config(state=tkinter.DISABLED)
        max_temp_check.config(state=tkinter.DISABLED)
        min_temp_check.config(state=tkinter.DISABLED)
        mean_temp_check.config(state=tkinter.DISABLED)
        enter_button.config(state=tkinter.DISABLED)
        weather_info_box.config(state=tkinter.DISABLED)


def exit_app():
    """
    Xử lý sự kiện nhấn nút "Exit" để thoát ứng dụng.
    """
    window.quit()


# Tạo cửa sổ giao diện
window = tkinter.Tk()
window.title('Tra cứu và dự báo thời tiết')
window.iconbitmap('Images/weather-news.ico')

# Tạo frame chính
frame = ttk.Frame(window, padding="30 15 30 15")
frame.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Tạo các biến và các đối tượng liên quan
date_var = tkinter.StringVar()
max_temp_var = tkinter.IntVar()
min_temp_var = tkinter.IntVar()
mean_temp_var = tkinter.IntVar()
sunshine_var = tkinter.IntVar()
weather_day_var = tkinter.IntVar()
forecast_var = tkinter.IntVar()

# Tạo LabelFrame "Option"
option_frame = tkinter.LabelFrame(frame, text="Option")
option_frame.grid(row=0, column=0, padx=20, pady=10)

# Tạo Checkbutton "Dự báo thời tiết"
weather_day_check = ttk.Checkbutton(option_frame, text="Tra cứu theo ngày", variable=weather_day_var,
                                    command=toggle_weather_info)
weather_day_check.grid(row=0, column=0, columnspan=2, sticky=tkinter.W)


# Tạo Checkbutton "Dự báo thời tiết"
forecast_check = ttk.Checkbutton(option_frame, text="Dự báo thời tiết", variable=forecast_var, command=toggle_forecast_info)
forecast_check.grid(row=1, column=0, columnspan=2, sticky=tkinter.W)


# Tạo LabelFrame "Weather Information"
weather_info_frame = tkinter.LabelFrame(frame, text="Weather Information")
weather_info_frame.grid(row=1, column=0, padx=20, pady=10)

# Tạo Label và Entry cho ngày
date_label = ttk.Label(weather_info_frame, text="Date (YYYY-MM-DD): ", state=tkinter.DISABLED)
date_label.grid(row=0, column=0, sticky=tkinter.W)
date_entry = ttk.Entry(weather_info_frame, width=12, textvariable=date_var)
date_entry.grid(row=0, column=1)

# Tạo Checkbutton cho biến thời tiết
max_temp_check = ttk.Checkbutton(weather_info_frame, text="Max Temp", variable=max_temp_var, state=tkinter.DISABLED)
max_temp_check.grid(row=1, column=0, sticky=tkinter.W)
min_temp_check = ttk.Checkbutton(weather_info_frame, text="Min Temp", variable=min_temp_var, state=tkinter.DISABLED)
min_temp_check.grid(row=2, column=0, sticky=tkinter.W)
mean_temp_check = ttk.Checkbutton(weather_info_frame, text="Mean Temp", variable=mean_temp_var, state=tkinter.DISABLED)
mean_temp_check.grid(row=3, column=0, sticky=tkinter.W)


# Tạo nút "Enter" để tra cứu thông tin thời tiết
enter_button = ttk.Button(weather_info_frame, text="Enter", command=enter_data, state=tkinter.DISABLED)
enter_button.grid(row=4, column=1, padx=10, pady=5)


# Tạo khung hiển thị thông tin thời tiết
weather_info_box = tkinter.Text(weather_info_frame, width=40, height=10, state=tkinter.DISABLED)
weather_info_box.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Tạo LabelFrame "Weather Forecast"
forecast_frame = tkinter.LabelFrame(frame, text="Weather Forecast")
forecast_frame.grid(row=1, column=1, padx=20, pady=10)

# Tạo Label và Entry cho số ngày dự báo
forecast_days_label = ttk.Label(forecast_frame, text="Số ngày dự báo: ", state=tkinter.DISABLED)
forecast_days_label.grid(row=1, column=0, sticky=tkinter.W)
forecast_days_entry = ttk.Entry(forecast_frame, width=12, state=tkinter.DISABLED)
forecast_days_entry.grid(row=1, column=1)

# Tạo nút "Enter" để dự báo thông tin thời tiết
forecast_enter_button = ttk.Button(forecast_frame, text="Enter", command=enter_forecast_data, state=tkinter.DISABLED)
forecast_enter_button.grid(row=2, column=1, padx=10, pady=5)

# Tạo khung hiển thị thông tin dự báo thời tiết
forecast_info_box = tkinter.Text(forecast_frame, width=40, height=10, state=tkinter.DISABLED)
forecast_info_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Tạo nút "Exit" để thoát ứng dụng
exit_button = ttk.Button(frame, text="Exit", command=exit_app)
exit_button.grid(row=2, column=0, pady=10)

# Hiển thị cửa sổ giao diện
window.mainloop()