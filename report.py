import webbrowser
import os
from fpdf import FPDF
import pandas as pd
import datetime
import time


class WeatherReport:
    """
    Tạo một báo cáo PDF chứa dữ liệu thời tiết cho London.
    """

    def __init__(self, filename, data_file):
        self.filename = filename
        self.data_file = data_file
        self.data = pd.read_csv(self.data_file)
        self.data['date'] = pd.to_datetime(self.data['date'], format='%Y%m%d')  # Chuyển cột 'date' thành dạng datetime

    def generate(self):
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Thêm biểu tượng
        pdf.image("Images/weather-news-2.png", w=30, h=30)

        # Thêm tiêu đề
        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt="London Weather Report", border=0, align="C", ln=1)

        # Thêm dữ liệu thời tiết
        pdf.set_font(family='Times', size=12)
        self.add_table(pdf, self.get_weather_data())

        # Thêm thông tin địa điểm và ngày tạo báo cáo
        pdf.set_font(family='Times', size=12, style='I')
        location = "Ho Chi Minh City"
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        info = f"Location: {location}, Report generated on: {current_date}"
        pdf.cell(w=0, h=20, txt=info, border=0, align="R", ln=1)

        # Thêm chữ ký
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=0, h=20, txt="Son", border=0, align="R", ln=0)
        pdf.cell(w=0, h=20, txt="Tran Thanh Son", border=0, align="R", ln=1)

        os.chdir("source")

        pdf.output(self.filename)

        webbrowser.open(self.filename)

    def add_table(self, pdf, data):
        col_width = pdf.w / 6
        row_height = pdf.font_size + 5
        table_width = pdf.w - 2 * pdf.l_margin

        pdf.set_font('Times', 'B', 12)
        pdf.ln(row_height)

        pdf.set_font('Times', '', 12)

        # Add table header
        header = ["Date", "Max Temp (°C)", "Mean Temp (°C)", "Min Temp (°C)", "Precipitation (mm)"]
        for item in header:
            pdf.cell(col_width, row_height, str(item), border=1, align='C')

        pdf.ln(row_height)

        # Add table data
        for row in data:
            for item in row:
                pdf.cell(col_width, row_height, str(item), border=1, align='C')
            pdf.ln(row_height)

    def get_weather_data(self):
        weather_data = []

        start_date = datetime.datetime(2010, 1, 1)
        end_date = datetime.datetime(2010, 1, 10)

        filtered_data = self.data[(self.data['date'] >= start_date) & (self.data['date'] <= end_date)]

        for _, row in filtered_data.iterrows():
            date = row['date'].strftime('%Y-%m-%d')  # Định dạng ngày thành chuỗi
            max_temp = row['max_temp']
            mean_temp = row['mean_temp']
            min_temp = row['min_temp']
            precipitation = row['precipitation']
            weather_data.append([date, max_temp, mean_temp, min_temp, precipitation])

        return weather_data


current_time = time.strftime('%Y%m%d-%H%M%S')
filepath = f"{current_time}.pdf"
# Ví dụ sử dụng
report = WeatherReport(filepath, "london_weather.csv")
report.generate()
