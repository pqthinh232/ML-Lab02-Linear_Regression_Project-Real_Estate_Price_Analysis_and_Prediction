# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import matplotlib.pyplot as plt
# import seaborn as sns

# # --- 1. LOAD ASSETS & DATA ---
# @st.cache_data
# def load_raw_data():
#     # Nhớ kiểm tra lại đường dẫn file csv của bạn
#     df = pd.read_csv('../data/preprocessed/data_final.csv')
#     return df

# @st.cache_resource
# def load_assets():
#     model = joblib.load('model_bat_dong_san.pkl')
#     model_columns = joblib.load('model_columns.pkl')
#     return model, model_columns

# df_raw = load_raw_data()
# model, model_columns = load_assets()

# # --- 2. GIAO DIỆN ---
# st.set_page_config(page_title="Dự báo BĐS", layout="wide")
# st.title("🏠 Hệ thống Dự báo Giá Nhà")

# col1, col2 = st.columns([1, 1.2])

# with col1:
#     st.subheader("📋 Nhập thông số thực tế")
#     area_input = st.number_input("Diện tích thực tế (m²):", min_value=1.0, value=50.0)
#     bath_input = st.number_input("Số phòng tắm:", min_value=0, value=1)
#     floor_input = st.number_input("Số tầng:", min_value=0, value=1)
    
#     list_quan = sorted([
#         c.replace('quan_', '') 
#         for c in model_columns 
#         if c.startswith('quan_') and 'inter' not in c
#     ])
#     quan_selected = st.selectbox("Chọn Quận/Huyện:", list_quan)
#     phap_ly_selected = st.selectbox("Tình trạng pháp lý:", ["Có sổ", "Giấy tờ không xác định"])

# # --- 3. LOGIC DỰ BÁO ---
# def predict_price(area, bath, floor, dist, legal):
#     dt_log = np.log1p(area)
    
#     # Khởi tạo DataFrame với tất cả cột bằng 0
#     df_input = pd.DataFrame(0, index=[0], columns=model_columns)
    
#     # --- SỬA LẠI THEO ĐÚNG TÊN BẠN XÁC NHẬN ---
#     # Log thì là dien_tich_log
#     if 'dien_tich_log' in model_columns:
#         df_input.at[0, 'dien_tich_log'] = dt_log
    
#     if 'dien_tich_poly2' in model_columns:
#         df_input.at[0, 'dien_tich_poly2'] = dt_log**2
        
#     # Các biến số khác
#     df_input.at[0, 'phong_tam'] = bath
#     df_input.at[0, 'so_tang'] = floor
            
#     # Gán Quận
#     target_quan_col = f"quan_{dist}"
#     if target_quan_col in model_columns:
#         df_input.at[0, target_quan_col] = 1
        
#     # Gán Pháp lý
#     target_legal_col = f"phap_ly_{legal}"
#     if target_legal_col in model_columns:
#         df_input.at[0, target_legal_col] = 1

#     # Tính biến tương tác
#     # Lưu ý: Nếu model_columns hiện tên khác, hãy sửa target_inter_col cho khớp
#     target_inter_col = f"inter_area_quan_{dist}"
#     if target_inter_col in model_columns:
#         df_input.at[0, target_inter_col] = dt_log
    
#     # Dự báo
#     pred_log = model.predict(df_input)
#     return np.expm1(pred_log)[0]

# # --- 4. OUTPUT & VISUALIZATION ---
# with col2:
#     st.subheader("🚀 Kết quả dự báo")
#     res = predict_price(area_input, bath_input, floor_input, quan_selected, phap_ly_selected)
    
#     c1, c2 = st.columns(2)
#     c1.metric("Giá dự báo", f"{res:,.2f} Tỷ VNĐ")
#     c2.metric("Độ tin cậy (R²)", "0.75")
    
#     # --- BIỂU ĐỒ 1: THỰC TẾ VS DỰ BÁO ---
#     st.divider()
#     st.write(f"📈 **Mối quan hệ Diện tích - Giá tại {quan_selected}**")
    
#     df_district = df_raw[df_raw['quan'] == quan_selected].copy()
    
#     # KIỂM TRA: Nếu file CSV tên là 'dien_tich_dat' thì giữ nguyên, nếu là 'dien_tich' thì sửa lại
#     col_x = 'dien_tich_dat' if 'dien_tich_dat' in df_district.columns else 'dien_tich'
    
#     fig1, ax1 = plt.subplots(figsize=(10, 5))
#     sns.scatterplot(data=df_district, x=col_x, y='gia', alpha=0.4, label='Dữ liệu thực tế', ax=ax1)
    
#     max_area = int(df_district[col_x].max()) if not df_district.empty else 500
#     test_areas = np.linspace(10, max_area, 50)
#     test_prices = [predict_price(a, bath_input, floor_input, quan_selected, phap_ly_selected) for a in test_areas]
#     ax1.plot(test_areas, test_prices, color='red', lw=2, label='Đường dự báo của mô hình')
    
#     ax1.scatter([area_input], [res], color='black', s=150, marker='*', label='Căn nhà bạn nhập', zorder=5)
#     ax1.set_xlabel("Diện tích (m²)")
#     ax1.set_ylabel("Giá (Tỷ VNĐ)")
#     ax1.legend()
#     st.pyplot(fig1)

#     # --- BIỂU ĐỒ 2: PHÂN BỔ GIÁ ---
#     # Giữ nguyên như cũ vì nó đã khá ổn
#     st.divider()
#     st.write(f"📊 **Vị trí giá dự báo so với mặt bằng chung tại {quan_selected}**")
#     fig2, ax2 = plt.subplots(figsize=(10, 4))
#     sns.kdeplot(df_district['gia'], fill=True, color="green", ax=ax2, label='Phân bổ giá thực tế')
#     ax2.axvline(res, color='red', linestyle='--', lw=2, label=f'Giá dự báo ({res:.1f} tỷ)')
#     ax2.legend()
#     st.pyplot(fig2)




import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --- LOAD ---
@st.cache_data
def load_raw_data():
    return pd.read_csv('../data/preprocessed/data_final_total.csv')

@st.cache_resource
def load_assets():
    model = joblib.load('model_bat_dong_san.pkl')
    model_columns = joblib.load('model_columns.pkl')
    return model, model_columns

df_raw = load_raw_data()
model, model_columns = load_assets()

# Màu biểu đồ — palette #503156 #6ea4bf #a31621 #bcd8c1 #fcf7f8 (+ biến thể hài hòa)
CHART = {
    "plum": "#503156",
    "sky": "#6ea4bf",
    "sky_dark": "#4a7f9c",
    "crimson": "#a31621",
    "crimson_soft": "#c43d48",
    "mint": "#bcd8c1",
    "mint_light": "#d8ebe0",
    "mist": "#fcf7f8",
    "spine": "#c4b3c8",
    "grid": "#bcd8c1",
}
# Biểu đồ full width (xếp dọc): kích thước hiển thị do CỘT Streamlit quyết định — không dùng figsize quá lớn (sẽ bị thu nhỏ, trông nhỏ hơn).
CHART_FS = {"title": 18, "axis": 15, "tick": 14, "legend": 13}
CHART_FIGSIZE = (8.8, 5.2)
CHART_DPI = 110


# --- CONFIG ---
st.set_page_config(page_title="Du bao BDS", layout="wide")

# --- DASHBOARD STYLES (palette: #503156 #6ea4bf #a31621 #bcd8c1 #fcf7f8) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

:root {
    --plum: #503156;
    --sky: #6ea4bf;
    --crimson: #a31621;
    --mint: #bcd8c1;
    --mist: #fcf7f8;
}

html, body {
    font-family: "Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif !important;
    background-color: var(--mist) !important;
    font-size: 25.5px;
    line-height: 1.55;
}

.stApp {
    font-family: "Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif !important;
    background-color: var(--mist) !important;
    color: var(--plum);
    font-size: 25.5px;
    line-height: 1.55;
    overflow-x: hidden;
}

.stApp .main .block-container {
    color: var(--plum);
}

/* Bỏ giới hạn 1280px — nội dung dùng hết chiều ngang layout “wide” */
.block-container {
    padding: 2.5rem clamp(0.85rem, 2.5vw, 1.5rem) 3.5rem;
    max-width: none !important;
    width: 100% !important;
}

/* Top accent bar */
.stApp::before {
    content: "";
    display: block;
    height: 5px;
    width: 100%;
    background: linear-gradient(90deg, var(--plum) 0%, var(--sky) 45%, var(--crimson) 100%);
}

/* Page title */
h1 {
    font-family: "Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif !important;
    font-size: clamp(1.85rem, 3.5vw, 2.45rem) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em;
    color: var(--plum) !important;
    margin: 0 0 0.35rem 0 !important;
    line-height: 1.2 !important;
}

h2, h3 {
    font-family: "Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif !important;
    font-weight: 600 !important;
    color: var(--plum) !important;
    font-size: 1.15rem !important;
    margin: 0 0 1.1rem 0 !important;
    letter-spacing: -0.02em;
}

.dashboard-lead {
    font-size: 1rem;
    color: rgba(80, 49, 86, 0.78);
    max-width: 42rem;
    margin: 0 0 2rem 0;
}

/* Column cards & rhythm */
div[data-testid="stHorizontalBlock"] {
    gap: 1.75rem !important;
    align-items: stretch !important;
}

div[data-testid="column"] > div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="column"] > div[data-testid="stVerticalBlock"] {
    height: 100%;
}

div[data-testid="column"] > div[data-testid="stVerticalBlockBorderWrapper"] > div,
div[data-testid="column"] > div[data-testid="stVerticalBlock"] {
    height: 100%;
}

div[data-testid="column"] > div[data-testid="stVerticalBlockBorderWrapper"] > div > .stVerticalBlock,
div[data-testid="column"] > div[data-testid="stVerticalBlock"] > .stVerticalBlock {
    background: #ffffff;
    border: 1px solid rgba(80, 49, 86, 0.1);
    border-radius: 18px;
    padding: 1.75rem 1.85rem !important;
    box-shadow: 0 8px 32px rgba(80, 49, 86, 0.07);
}

/* Nested rows (e.g. metrics): no second card inside the panel */
div[data-testid="column"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlockBorderWrapper"] > div > .stVerticalBlock,
div[data-testid="column"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"] > .stVerticalBlock {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
}

/* Extra breathing room between form controls */
.stVerticalBlock > div {
    gap: 0.65rem;
}

/* Labels */
label, span[data-testid="stWidgetLabel"] p {
    font-size: 0.98rem !important;
    font-weight: 600 !important;
    color: var(--plum) !important;
}

/* Larger inputs */
.stNumberInput > div {
    align-items: center;
}

.stNumberInput input {
    background-color: var(--mist) !important;
    border: 2px solid var(--mint) !important;
    border-radius: 12px !important;
    min-height: 3.35rem;
    padding: 0.65rem 1rem !important;
    font-size: 1.08rem !important;
    font-weight: 500 !important;
    color: var(--plum) !important;
}

.stNumberInput button {
    min-height: 2.5rem !important;
}

/* Select đã đóng: theme tối hay tô nền đen + chữ tím — ép nền sáng toàn bộ control */
.stSelectbox [data-baseweb="select"] {
    background-color: #fcf7f8 !important;
    background-image: none !important;
    border: 2px solid var(--mint) !important;
    border-radius: 12px !important;
    min-height: 3.35rem;
    font-size: 1.08rem !important;
    font-weight: 500 !important;
    color-scheme: light !important;
}

.stSelectbox [data-baseweb="select"] > div {
    min-height: 3.35rem !important;
    padding: 0.35rem 0.85rem !important;
    align-items: center;
    background-color: #fcf7f8 !important;
    background-image: none !important;
    color: #503156 !important;
}

/* Mọi lớp con trong ô chọn (trừ portal menu): chữ đậm, không nền đen */
.stSelectbox [data-baseweb="select"] * {
    color: #503156 !important;
    -webkit-text-fill-color: #503156 !important;
    background-color: transparent !important;
    background-image: none !important;
}

.stSelectbox [data-baseweb="select"] svg,
.stSelectbox [data-baseweb="select"] svg * {
    fill: #503156 !important;
    color: #503156 !important;
    -webkit-text-fill-color: #503156 !important;
}

/* Dropdown portal (BaseWeb): light surface — không dùng selector * trên select */

body [data-baseweb="popover"] [data-baseweb="menu"],
body [data-baseweb="popover"] ul[role="listbox"],
body [data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 1px solid rgba(80, 49, 86, 0.14) !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.14) !important;
}

body [data-baseweb="popover"] [role="option"],
body [data-baseweb="popover"] li,
body [data-baseweb="menu"] li {
    color: #503156 !important;
    background-color: #ffffff !important;
}

body [data-baseweb="popover"] [role="option"]:hover,
body [data-baseweb="popover"] li:hover,
body [data-baseweb="menu"] li:hover {
    background-color: #bcd8c1 !important;
    color: #2a1830 !important;
}

body [data-baseweb="popover"] [aria-selected="true"] {
    background-color: rgba(188, 216, 193, 0.65) !important;
}

/* Primary action */
.stButton > button {
    width: 100%;
    margin-top: 0.5rem;
    background: linear-gradient(135deg, var(--crimson) 0%, #7d1220 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.95rem 1.25rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
    box-shadow: 0 6px 20px rgba(163, 22, 33, 0.28);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--sky) 0%, #4d87a8 100%) !important;
    box-shadow: 0 8px 24px rgba(110, 164, 191, 0.35);
}

/* Metrics: nền trắng + chữ đậm (override gradient/text-fill theme tối → chữ “mất”) */
[data-testid="stAppViewContainer"] > .main {
    background-color: var(--mist) !important;
}

[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 2px solid rgba(80, 49, 86, 0.18) !important;
    padding: 1.35rem 1rem !important;
    border-radius: 14px !important;
    text-align: center !important;
    box-shadow: 0 2px 12px rgba(80, 49, 86, 0.06);
    color: #241829 !important;
    /* Một số bản Streamlit dùng biến theme cho màu số metric */
    --text-color: #0f0814 !important;
    --primary-text-color: #0f0814 !important;
}

[data-testid="metric-container"] label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    opacity: 1 !important;
    color: #503156 !important;
}

[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] label,
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #503156 !important;
    opacity: 1 !important;
}

/* Số metric: Streamlit theme tối hay để chữ trong suốt / gradient — ép đen tuyệt đối */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="metric-container"] [data-testid="stMarkdownContainer"],
[data-testid="metric-container"] [data-testid="stMarkdownContainer"] * {
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    fill: #000000 !important;
    caret-color: #000000 !important;
    background: transparent !important;
    background-image: none !important;
    background-clip: border-box !important;
    -webkit-background-clip: border-box !important;
    opacity: 1 !important;
    visibility: visible !important;
    mix-blend-mode: normal !important;
}

[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    color: #503156 !important;
    -webkit-text-fill-color: #503156 !important;
}

/* Hai ô kết quả (chỉ dùng result_placeholder, không lặp st.metric) */
.result-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 0.9rem;
    margin: 0.35rem 0 0 0;
}
.result-card {
    flex: 1 1 200px;
    background: linear-gradient(165deg, #ffffff 0%, #f5faf6 100%) !important;
    border: 2px solid #6ea4bf !important;
    border-radius: 16px !important;
    padding: 1rem 1.15rem !important;
    box-shadow: 0 6px 22px rgba(80, 49, 86, 0.12), inset 0 1px 0 rgba(255,255,255,0.9) !important;
    text-align: center !important;
}
.result-card .result-lbl {
    display: block !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #503156 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 0.45rem !important;
}
.result-card .result-val {
    display: block !important;
    font-size: 1.45rem !important;
    font-weight: 800 !important;
    color: #a31621 !important;
    line-height: 1.2 !important;
}
.result-card.result-card-secondary .result-val {
    color: #503156 !important;
}

.stApp .main [data-testid="stMarkdownContainer"] p,
.stApp .main [data-testid="stMarkdownContainer"] span {
    color: #503156 !important;
}

/* Section divider (Streamlit) */
hr {
    margin: 2.25rem 0 1.75rem !important;
    border: none !important;
    border-top: 1px solid rgba(80, 49, 86, 0.12) !important;
}

/* Chart trong cột (2×2), không full-bleed viewport */
.stPyplot {
    background: #ffffff !important;
    padding: 0.65rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(80, 49, 86, 0.1) !important;
    box-shadow: 0 4px 16px rgba(80, 49, 86, 0.07) !important;
    width: 100% !important;
    max-width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    box-sizing: border-box !important;
}

.stPyplot img,
[data-testid="stImage"] img {
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    object-fit: contain !important;
}

</style>
""", unsafe_allow_html=True)

st.title("Hệ thống dự báo giá nhà ở thành phố Hồ Chí Minh và Hà Nội")
st.markdown(
    '<p class="dashboard-lead">Nhập thông tin bất động sản để ước tính giá và xem phân tích nhanh theo khu vực.</p>',
    unsafe_allow_html=True,
)

# ===== MAIN GRID (balanced columns) =====
left, right = st.columns([1, 1])

# --- LEFT: FORM ---
with left:
    st.subheader("Thông tin đầu vào")

    area_input = st.number_input("Diện tích (m²)", min_value=1.0, value=50.0)
    bath_input = st.number_input("Số phòng tắm", min_value=0, value=1)
    floor_input = st.number_input("Số tầng", min_value=0, value=1)

    list_quan = sorted([
        c.replace('quan_', '') 
        for c in model_columns 
        if c.startswith('quan_') and 'inter' not in c
    ])
    quan_selected = st.selectbox("Quận/Huyện", list_quan)
    phap_ly_selected = st.selectbox("Tình trạng pháp lý", ["Có sổ", "Giấy tờ không xác định"])

    predict_btn = st.button("Dự đoán")

# --- RIGHT: RESULT ---
with right:
    st.subheader("Kết quả")

    result_placeholder = st.empty()

# --- LOGIC GIỮ NGUYÊN ---
def predict_price(area, bath, floor, dist, legal):
    dt_log = np.log1p(area)
    df_input = pd.DataFrame(0, index=[0], columns=model_columns)

    if 'dien_tich_log' in model_columns:
        df_input.at[0, 'dien_tich_log'] = dt_log
    
    if 'dien_tich_poly2' in model_columns:
        df_input.at[0, 'dien_tich_poly2'] = dt_log**2
        
    df_input.at[0, 'phong_tam'] = bath
    df_input.at[0, 'so_tang'] = floor
            
    target_quan_col = f"quan_{dist}"
    if target_quan_col in model_columns:
        df_input.at[0, target_quan_col] = 1
        
    target_legal_col = f"phap_ly_{legal}"
    if target_legal_col in model_columns:
        df_input.at[0, target_legal_col] = 1

    target_inter_col = f"inter_area_quan_{dist}"
    if target_inter_col in model_columns:
        df_input.at[0, target_inter_col] = dt_log
    
    pred_log = model.predict(df_input)
    return np.expm1(pred_log)[0]

# --- ACTION ---
if predict_btn:
    res = predict_price(area_input, bath_input, floor_input, quan_selected, phap_ly_selected)

    result_placeholder.markdown(
        f'<div class="result-cards">'
        f'<div class="result-card"><span class="result-lbl">Giá dự báo</span>'
        f'<span class="result-val">{res:,.2f} tỷ VNĐ</span></div>'
        f'<div class="result-card result-card-secondary"><span class="result-lbl">Độ tin cậy (R²)</span>'
        f'<span class="result-val">0.75</span></div></div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("Phân tích dữ liệu")

    df_district = df_raw[df_raw['quan'] == quan_selected].copy()
    col_x = 'dien_tich_dat' if 'dien_tich_dat' in df_district.columns else 'dien_tich'

    row1_left, row1_right = st.columns(2)
    row2_left, row2_right = st.columns(2)

    # ---- Hàng 1: diện tích + KDE ----
    with row1_left:
        fig1, ax1 = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)
        fig1.patch.set_facecolor(CHART["mist"])
        ax1.set_facecolor(CHART["mist"])

        sns.scatterplot(
            data=df_district,
            x=col_x,
            y="gia",
            ax=ax1,
            facecolor=CHART["mint_light"],
            edgecolor=CHART["sky"],
            linewidths=0.55,
            s=88,
            alpha=0.82,
            label="Giao dịch thực tế",
        )

        max_area = int(df_district[col_x].max()) if not df_district.empty else 500
        test_areas = np.linspace(10, max_area, 50)
        test_prices = [
            predict_price(a, bath_input, floor_input, quan_selected, phap_ly_selected)
            for a in test_areas
        ]

        ax1.plot(
            test_areas,
            test_prices,
            color=CHART["sky"],
            linewidth=5,
            alpha=0.35,
            solid_capstyle="round",
            zorder=1,
        )
        ax1.plot(
            test_areas,
            test_prices,
            color=CHART["crimson"],
            linewidth=2.8,
            solid_capstyle="round",
            label="Đường xu hướng dự báo",
            zorder=2,
        )
        ax1.scatter(
            [area_input],
            [res],
            s=440,
            marker="*",
            facecolor=CHART["plum"],
            zorder=5,
            edgecolors=CHART["crimson_soft"],
            linewidths=1.35,
            label="Giá dự báo (đầu vào của bạn)",
        )

        ax1.set_title(
            f"Mối quan hệ diện tích – giá tại {quan_selected}",
            fontsize=CHART_FS["title"],
            fontweight="600",
            color=CHART["plum"],
            pad=14,
        )
        ax1.set_xlabel("Diện tích (m²)", fontsize=CHART_FS["axis"], color=CHART["plum"])
        ax1.set_ylabel("Giá (tỷ VNĐ)", fontsize=CHART_FS["axis"], color=CHART["plum"])
        for spine in ax1.spines.values():
            spine.set_color(CHART["spine"])
        ax1.tick_params(colors=CHART["plum"], labelsize=CHART_FS["tick"])
        ax1.grid(True, linestyle="--", alpha=0.38, color=CHART["grid"])
        ax1.set_axisbelow(True)
        ax1.legend(
            frameon=True,
            loc="best",
            fontsize=CHART_FS["legend"],
            framealpha=0.96,
            facecolor=CHART["mist"],
            edgecolor=CHART["mint"],
        )
        fig1.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    with row1_right:
        fig2, ax2 = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)
        fig2.patch.set_facecolor(CHART["mist"])
        ax2.set_facecolor(CHART["mist"])

        sns.kdeplot(
            df_district["gia"],
            fill=True,
            ax=ax2,
            color=CHART["sky"],
            alpha=0.4,
            linewidth=0,
            legend=False,
        )
        sns.kdeplot(
            df_district["gia"],
            fill=True,
            ax=ax2,
            color=CHART["mint"],
            alpha=0.62,
            linewidth=0,
            label="Phân bố giá thực tế (KDE)",
        )
        sns.kdeplot(
            df_district["gia"],
            fill=False,
            ax=ax2,
            color=CHART["plum"],
            linewidth=2.8,
            legend=False,
        )
        ax2.axvline(
            res,
            linestyle="--",
            linewidth=2.8,
            color=CHART["crimson"],
            label=f"Giá dự báo ({res:,.2f} tỷ VNĐ)",
        )

        ax2.set_title(
            f"Vị trí giá dự báo so với phân bố tại {quan_selected}",
            fontsize=CHART_FS["title"],
            fontweight="600",
            color=CHART["plum"],
            pad=14,
        )
        ax2.set_xlabel("Giá (tỷ VNĐ)", fontsize=CHART_FS["axis"], color=CHART["plum"])
        ax2.set_ylabel("Mật độ (KDE)", fontsize=CHART_FS["axis"], color=CHART["plum"])
        for spine in ax2.spines.values():
            spine.set_color(CHART["spine"])
        ax2.tick_params(colors=CHART["plum"], labelsize=CHART_FS["tick"])
        ax2.grid(True, linestyle="--", alpha=0.38, color=CHART["grid"])
        ax2.set_axisbelow(True)
        ax2.legend(
            frameon=True,
            loc="best",
            fontsize=CHART_FS["legend"],
            framealpha=0.96,
            facecolor=CHART["mist"],
            edgecolor=CHART["mint"],
        )
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # ---- Hàng 2: phòng tắm + pháp lý ----
    with row2_left:
        fig3, ax3 = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)
        fig3.patch.set_facecolor(CHART["mist"])
        ax3.set_facecolor(CHART["mist"])
        df_bath = df_district.dropna(subset=["phong_tam", "gia"]).copy()
        if df_bath.empty or df_bath["phong_tam"].nunique() < 1:
            ax3.text(
                0.5, 0.5, "Không đủ dữ liệu theo phòng tắm",
                ha="center", va="center", transform=ax3.transAxes, color=CHART["plum"],
            )
            ax3.set_axis_off()
        else:
            bath_order = sorted(df_bath["phong_tam"].unique())
            pal_bath = (
                [CHART["sky"], CHART["mint"], CHART["mint_light"]]
                * ((len(bath_order) // 3) + 1)
            )[: len(bath_order)]
            sns.boxplot(
                data=df_bath,
                x="phong_tam",
                y="gia",
                order=bath_order,
                ax=ax3,
                palette=pal_bath,
                saturation=0.72,
                medianprops={"color": CHART["crimson"], "linewidth": 2.2},
                whiskerprops={"color": CHART["sky_dark"], "linewidth": 1.2},
                capprops={"color": CHART["sky_dark"], "linewidth": 1.2},
                boxprops={"linewidth": 1.0, "edgecolor": CHART["plum"]},
                flierprops={
                    "marker": "o",
                    "markersize": 4,
                    "markerfacecolor": CHART["crimson_soft"],
                    "alpha": 0.45,
                },
            )
            sns.stripplot(
                data=df_bath,
                x="phong_tam",
                y="gia",
                order=bath_order,
                ax=ax3,
                color=CHART["plum"],
                alpha=0.32,
                size=3.2,
                jitter=0.22,
            )
            ax3.axhline(
                res,
                color=CHART["crimson"],
                linestyle="--",
                linewidth=2.4,
                label=f"Giá dự báo ({res:,.2f} tỷ)",
            )
            ax3.set_title(
                f"Giá theo số phòng tắm — {quan_selected}",
                fontsize=CHART_FS["title"],
                fontweight="600",
                color=CHART["plum"],
                pad=14,
            )
            ax3.set_xlabel("Số phòng tắm", fontsize=CHART_FS["axis"], color=CHART["plum"])
            ax3.set_ylabel("Giá (tỷ VNĐ)", fontsize=CHART_FS["axis"], color=CHART["plum"])
            for spine in ax3.spines.values():
                spine.set_color(CHART["spine"])
            ax3.tick_params(colors=CHART["plum"], labelsize=CHART_FS["tick"])
            ax3.grid(True, axis="y", linestyle="--", alpha=0.38, color=CHART["grid"])
            ax3.set_axisbelow(True)
            ax3.legend(
                frameon=True,
                loc="best",
                fontsize=CHART_FS["legend"],
                framealpha=0.96,
                facecolor=CHART["mist"],
                edgecolor=CHART["mint"],
            )
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

    with row2_right:
        fig4, ax4 = plt.subplots(figsize=CHART_FIGSIZE, dpi=CHART_DPI)
        fig4.patch.set_facecolor(CHART["mist"])
        ax4.set_facecolor(CHART["mist"])
        df_legal = df_district.dropna(subset=["phap_ly", "gia"]).copy()
        if df_legal.empty or df_legal["phap_ly"].nunique() < 1:
            ax4.text(
                0.5, 0.5, "Không đủ dữ liệu theo pháp lý",
                ha="center", va="center", transform=ax4.transAxes, color=CHART["plum"],
            )
            ax4.set_axis_off()
        else:
            leg_order = sorted(df_legal["phap_ly"].unique())
            pal_legal = (
                [CHART["mint"], CHART["sky"], CHART["mint_light"], CHART["sky"], CHART["mint"]]
                * ((len(leg_order) // 5) + 1)
            )[: len(leg_order)]
            sns.boxplot(
                data=df_legal,
                x="phap_ly",
                y="gia",
                order=leg_order,
                ax=ax4,
                palette=pal_legal,
                saturation=0.72,
                medianprops={"color": CHART["crimson"], "linewidth": 2.2},
                whiskerprops={"color": CHART["sky_dark"], "linewidth": 1.2},
                capprops={"color": CHART["sky_dark"], "linewidth": 1.2},
                boxprops={"linewidth": 1.0, "edgecolor": CHART["plum"]},
                flierprops={
                    "marker": "o",
                    "markersize": 4,
                    "markerfacecolor": CHART["crimson_soft"],
                    "alpha": 0.45,
                },
            )
            sns.stripplot(
                data=df_legal,
                x="phap_ly",
                y="gia",
                order=leg_order,
                ax=ax4,
                color=CHART["plum"],
                alpha=0.3,
                size=3.2,
                jitter=0.18,
            )
            ax4.axhline(
                res,
                color=CHART["crimson"],
                linestyle="--",
                linewidth=2.4,
                label=f"Giá dự báo ({res:,.2f} tỷ)",
            )
            ax4.set_title(
                f"Giá theo pháp lý — {quan_selected}",
                fontsize=CHART_FS["title"],
                fontweight="600",
                color=CHART["plum"],
                pad=14,
            )
            ax4.set_xlabel("Pháp lý", fontsize=CHART_FS["axis"], color=CHART["plum"])
            ax4.set_ylabel("Giá (tỷ VNĐ)", fontsize=CHART_FS["axis"], color=CHART["plum"])
            ax4.tick_params(axis="x", rotation=18, colors=CHART["plum"], labelsize=CHART_FS["tick"])
            ax4.tick_params(axis="y", colors=CHART["plum"], labelsize=CHART_FS["tick"])
            for spine in ax4.spines.values():
                spine.set_color(CHART["spine"])
            ax4.grid(True, axis="y", linestyle="--", alpha=0.38, color=CHART["grid"])
            ax4.set_axisbelow(True)
            ax4.legend(
                frameon=True,
                loc="best",
                fontsize=CHART_FS["legend"],
                framealpha=0.96,
                facecolor=CHART["mist"],
                edgecolor=CHART["mint"],
            )
        fig4.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)
else:
    result_placeholder.empty()