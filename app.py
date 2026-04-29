import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. تنظیمات اولیه و استایل‌های پورتال
# ==========================================
st.set_page_config(page_title="Wadi Steel Enterprise Portal", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazirmatn');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* استایل دکمه‌های صفحه اصلی (شبیه کارت) */
    div.stButton > button {
        width: 100%;
        height: 80px;
        border-radius: 10px;
        border: 1px solid #0284c7;
        background-color: #f8fafc;
        color: #0f172a;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #0284c7;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(2, 132, 199, 0.4);
    }
    
    /* استایل کارت‌های داشبورد */
    div[data-testid="metric-container"] {
        background: white; border-top: 4px solid #0284c7; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. موتور دیتابیس (Webhook)
# ==========================================
MAKE_API_URL = "https://hook.eu1.make.com/r8ihcn7jgpdp73wljeviquvb8rgkqhib"

@st.cache_data(ttl=30)
def fetch_data():
    try:
        response = requests.get(MAKE_API_URL, timeout=15)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            # استانداردسازی ستون‌ها
            for col in ['CV', 'Weightage', 'SPI_Real', 'SPI(Real)', 'Actual_Total_H']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # پر کردن جاهای خالی برای جلوگیری از ارور
            if 'Project_Name' not in df.columns: df['Project_Name'] = 'پروژه پیش‌فرض'
            df['Project_Name'].fillna('پروژه نامشخص', inplace=True)
            return df
        return None
    except:
        return None

df = fetch_data()

# ==========================================
# 3. مدیریت صفحات (روتر پورتال)
# ==========================================
# اگر متغیرهای حافظه وجود ندارند، آن‌ها را بساز
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'home'
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None

# تابع برای تغییر صفحه
def go_to_project(project_name):
    st.session_state.selected_project = project_name
    st.session_state.current_view = 'dashboard'

def go_home():
    st.session_state.current_view = 'home'
    st.session_state.selected_project = None

# ==========================================
# 4. صفحه اصلی (Lobby / Landing Page)
# ==========================================
if st.session_state.current_view == 'home':
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>🏢 پورتال جامع مدیریت پروژه‌های وادی استیل</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>برای ورود به مرکز فرماندهی، پروژه مورد نظر را انتخاب کنید</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if df is not None and not df.empty:
        projects = df['Project_Name'].unique()
        
        # چیدن کارت پروژه‌ها در وسط صفحه
        cols = st.columns(len(projects) if len(projects) > 0 else 1)
        for i, proj in enumerate(projects):
            with cols[i % len(cols)]:
                # با کلیک روی هر دکمه، تابع تغییر صفحه اجرا می‌شود
                st.button(f"⚙️ ورود به پروژه: {proj}", key=f"btn_{proj}", on_click=go_to_project, args=(proj,))
    else:
        st.warning("در حال حاضر دیتایی از میک دریافت نشد. لطفاً از روشن بودن سناریو در Make.com اطمینان حاصل کنید.")

# ==========================================
# 5. صفحه داشبورد اختصاصی هر پروژه
# ==========================================
elif st.session_state.current_view == 'dashboard':
    
    proj_name = st.session_state.selected_project
    p_df = df[df['Project_Name'] == proj_name] # فیلتر کردن دیتابیس فقط برای این پروژه
    
    # --- سایدبار عمودی (فهرست) ---
    with st.sidebar:
        st.button("🏠 بازگشت به منوی اصلی", on_click=go_home, use_container_width=True)
        st.markdown("---")
        st.markdown(f"<h3 style='color:#0284c7; text-align:center;'>{proj_name}</h3>", unsafe_allow_html=True)
        
        # منوی ناوبری داخلی
        menu_selection = st.radio(
            "بخش‌های مدیریتی:",
            ["📊 راندمان کلی (داشبورد)", "⚙️ راندمان فعالیت‌ها", "🛑 توقفات و موانع", "💰 تحلیل هزینه (CV)"]
        )

    # --- محتوای اصلی داشبورد ---
    st.markdown(f"<h2>کنترل پروژه: <span style='color:#0284c7;'>{proj_name}</span> | <span style='font-size:18px; color:gray;'>بخش: {menu_selection}</span></h2>", unsafe_allow_html=True)
    st.markdown("---")

    # ----- بخش 1: راندمان کلی -----
    if menu_selection == "📊 راندمان کلی (داشبورد)":
        c1, c2, c3 = st.columns(3)
        c1.metric("تعداد کل فعالیت‌ها", len(p_df))
        c2.metric("مجموع انحراف هزینه (CV)", f"{p_df['CV'].sum():,.0f}" if 'CV' in p_df.columns else "N/A")
        
        spi_col = 'SPI(Real)' if 'SPI(Real)' in p_df.columns else ('SPI_Real' if 'SPI_Real' in p_df.columns else None)
        c3.metric("میانگین SPI", f"{p_df[spi_col].mean():.2f}" if spi_col else "N/A")
        
        st.info("این نمای کلی پروژه است. برای جزئیات، از منوی سمت راست بخش‌های دیگر را انتخاب کنید.")

    # ----- بخش 2: راندمان فعالیت‌ها -----
    elif menu_selection == "⚙️ راندمان فعالیت‌ها":
        st.write("در این بخش جدول هوشمند با قابلیت جستجو و فیلتر روی تک‌تک فعالیت‌ها قرار می‌گیرد.")
        search = st.text_input("جستجو در نام فعالیت...")
        temp_df = p_df[p_df['Task_Name'].str.contains(search, na=False)] if search and 'Task_Name' in p_df.columns else p_df
        st.dataframe(temp_df, use_container_width=True, hide_index=True)

    # ----- بخش 3: توقفات و موانع -----
    elif menu_selection == "🛑 توقفات و موانع":
        st.error("گزارش توقفات خطوط تولید")
        st.write("اینجا در آینده نمودارهای Tree Map قرمز رنگ (شبیه نرم‌افزار Watchdog) قرار می‌گیرد که نشان می‌دهد کدام دپارتمان بیشترین عامل توقف بوده است.")

    # ----- بخش 4: تحلیل هزینه -----
    elif menu_selection == "💰 تحلیل هزینه (CV)":
        st.success("تحلیل مالی و انحرافات")
        if 'Department' in p_df.columns and 'CV' in p_df.columns:
            fig = px.bar(p_df, x='Department', y='CV', color='CV', color_continuous_scale='RdYlGn', title="انحراف هزینه به تفکیک واحدها")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("ستون Department یا CV در دیتابیس یافت نشد.")
