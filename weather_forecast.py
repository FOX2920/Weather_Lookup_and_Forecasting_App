import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta

class WeatherForecast:
    """Lớp WeatherForecast để tra cứu và dự báo thời tiết."""

    def __init__(self, data_file):
        """
                Khởi tạo đối tượng WeatherForecast.

                Tham số:
                - data_file (str): Đường dẫn đến tệp dữ liệu thời tiết.
        """
        self.data_file = data_file
        self.data = pd.read_csv(self.data_file)
        self.preprocess_data()


    def preprocess_data(self):
        """
                Tiền xử lý dữ liệu thời tiết.

                Loại bỏ các hàng chứa giá trị null,
                chuyển đổi cột 'date' thành kiểu datetime,
                đặt cột 'date' làm chỉ mục của DataFrame,
                lựa chọn các cột dữ liệu cần sử dụng,
                chọn dữ liệu từ năm 2000 đến 2021.
        """
        # Xử lý dữ liệu
        # Loại bỏ các hàng chứa giá trị null
        self.data = self.data.dropna()

        # Chuyển đổi cột 'date' thành kiểu datetime
        self.data['date'] = pd.to_datetime(self.data['date'], format='%Y%m%d')

        # Đặt cột 'date' làm chỉ mục của DataFrame
        self.data = self.data.set_index('date')

        # Lựa chọn các cột dữ liệu cần sử dụng
        self.data = self.data[['max_temp', 'mean_temp', 'min_temp']]

        # Chọn dữ liệu từ năm 2000 đến 2021
        self.data = self.data['2000':'2021']

    def build_linear_regression_model(self, target_variable):
        """
        Xây dựng mô hình hồi quy tuyến tính.

        Tham số:
        - target_variable (str): Tên của biến mục tiêu.

        Trả về:
        - model (LinearRegression): Mô hình hồi quy tuyến tính đã huấn luyện.
        """
        if target_variable not in self.data.columns:
            raise Exception("Thuộc tính không tồn tại trong file CSV!")

        # Lựa chọn dữ liệu từ năm 2019 đến 2020
        data_subset = self.data['2019':'2020']

        # Tách dữ liệu thành features (X) và target (y)
        X = data_subset.drop(target_variable, axis=1)
        y = data_subset[target_variable]

        # Xây dựng mô hình hồi quy tuyến tính
        model = LinearRegression()

        # Huấn luyện mô hình
        model.fit(X, y)

        return model

    def get_weather_data(self, date, selected_variable):
        """
                        Lấy dữ liệu thời tiết cho một ngày cụ thể.

                        Tham số:
                        - date (datetime): Ngày cần lấy dữ liệu.
                        - selected_variable (str): Tên của biến thời tiết cần lấy.

                        Trả về:
                        - weather_data (dict): Dữ liệu thời tiết cho ngày và biến thời tiết đã chọn.
        """
        # Lấy dữ liệu thời tiết cho một ngày cụ thể
        try:
            weather_data = self.data.loc[date]
        except KeyError:
            # Lấy dữ liệu dự đoán từ mô hình hồi quy tuyến tính nếu ngày không tồn tại trong file CSV
            model = self.build_linear_regression_model(selected_variable)
            predicted_value = model.predict([[date.day, date.month]])
            return {
                'date': date,
                selected_variable: round(predicted_value[0], 2)
            }

        if selected_variable not in self.data.columns:
            raise Exception("Thuộc tính không tồn tại trong file CSV!")

        value = weather_data[selected_variable]
        return {
            'date': date,
            selected_variable: value
        }

    def get_weather_data_details(self, n):
        """
        Lấy dữ liệu chi tiết (max_temp, min_temp, mean_temp) của thời tiết cho n ngày sau ngày hiện tại.

        Tham số:
        - n (int): Số ngày cần lấy dữ liệu (n > 0).

        Trả về:
        - weather_data_details (list): Danh sách chứa dữ liệu chi tiết của thời tiết cho từng ngày.
        """
        if n <= 0:
            raise ValueError("Số ngày phải lớn hơn 0.")

        current_date = pd.Timestamp.now().floor('D')  # Lấy ngày hiện tại (loại bỏ giờ, phút, giây)

        weather_data_details = []
        for i in range(1, n + 1):
            date = current_date + timedelta(days=i)
            weather_data = self.get_weather_data(date, 'max_temp')
            weather_data['min_temp'] = self.get_weather_data(date, 'min_temp')['min_temp']
            weather_data['mean_temp'] = self.get_weather_data(date, 'mean_temp')['mean_temp']
            weather_data_details.append(weather_data)

        return weather_data_details