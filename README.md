#  Lab 02: Linear Regression - Phân tích và dự đoán giá bất động sản bằng mô hình hồi quy tuyến tính

Dự án này thực hiện quy trình toàn diện từ thu thập dữ liệu (Web Scraping), Tiền xử lý (Preprocessing), Phân tích khám phá (EDA) đến xây dựng mô hình Hồi quy Tuyến tính để dự đoán giá trị bất động sản tại thị trường Việt Nam (Hà Nội & TP.HCM).

## 📂 Cấu trúc dự án (Project Structure)

```text
ML-LAB02-LINEAR_REGRESSION/
├── data/
│   ├── raw/                # Dữ liệu gốc vừa thu thập (csv)
│   ├── interim/            # Dữ liệu trung gian sau khi chuẩn hóa sơ bộ
│   └── preprocessed/       # Dữ liệu sạch hoàn chỉnh, tập Train/Test cho Model
├── docs/                   # Chứa báo cáo dự án (PDF)
├── interface/              # Ứng dụng giao diện người dùng
│   ├── app.py              # File chạy ứng dụng dự báo
│   ├── model_bat_dong_san.pkl # Model đã huấn luyện
│   └── model_columns.pkl   # Danh sách các cột đặc trưng của model
├── interim preprocess/     # Xử lý sơ bộ riêng biệt cho từng nguồn dữ liệu cào được
├── modeling/               # Các thử nghiệm mô hình của 5 thành viên
│   ├── baseline.ipynb      # Mô hình baseline đơn giản nhất
│   ├── model_1(QThinh).ipynb 
│   ├── model_2(TLoi).ipynb
│   ├── model_3(THieu).ipynb
│   ├── model_4(KLinh).ipynb
│   └── model_5(Thien).ipynb
├── preprocessing and eda/  # Notebook tổng hợp xử lý và phân tích chuyên sâu
├── scraping/               # Các công cụ thu thập dữ liệu tự động
├── scripts/                # Script gộp dữ liệu thành viên
└── requirements.txt        # Danh sách thư viện cần cài đặt
```

## Quy trình thực hiện (Project Pipeline)

1. Data Collection: Sử dụng kỹ thuật Scraping thu thập hơn 10.000 tin đăng từ các sàn giao dịch bất động sản lớn.
2. Integration: Gộp dữ liệu từ các nguồn và khử trùng lặp dữ liệu (Scripts).
3. Preprocessing & EDA: 
    * Xử lý lỗi định dạng số, thời gian, xử lý dấu thập phân.
    * Lọc Outliers bằng phương pháp Percentile và khoảng cách Cook.
    * Biến đổi Log-Log để đưa dữ liệu về phân phối chuẩn.
    * Feature Engineering: Trích xuất Quận/Huyện, Thành phố, xử lý biến phân loại hiếm.
4. Modeling: Xây dựng 5 mô hình khác nhau để so sánh hiệu suất (Baseline, Multi-variable, Polynomial, Spatial Interaction).
5. Deployment: Đóng gói mô hình tốt nhất vào giao diện dự báo tại thư mục /interface.

## 🛠 Cài đặt và Sử dụng (Installation)

Yêu cầu: Python 3.10 trở lên.

1. Cài đặt các thư viện cần thiết:
   pip install -r requirements.txt

2. Chạy giao diện dự báo:
```text
   cd interface
   streamlit run app.py
```

## 📊 Kết quả mô hình tối ưu do nhóm đánh giá (Mô hình 1)

* R-squared (R2): 0.7502
* Mean Absolute Error (MAE): 2.61 Tỷ VNĐ
* Root Mean Squared Error (RMSE): 4.87 Tỷ VNĐ
* Mean Squared Error (MSE): 23.7 Tỷ^2