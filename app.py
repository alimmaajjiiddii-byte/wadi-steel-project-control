import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# 1. تنظیمات فوق حرفه‌ای صفحه
st.set_page_config(page_title="Wadi Steel | Watchdog Pro", layout="wide")

# تزریق CSS برای تغییر ظاهر سایت به سبک صنعتی
st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    * { font-family: 'Vazir', sans-serif; }
    .stApp { background-color: #f8fafc; }
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border-top: 5px solid #1e40af;
    }
    </style>
""", unsafe_allow_html=True)

MAKE_API_URL = "https://hook.eu1.make.com/r8ihcn7jgpdp73wljeviquvb8rgkqhib"

@st.cache_data(ttl=20)
def load_data():
    try:
        r = requests.get(MAKE_API_URL)
        return pd.DataFrame(r.json())
    except: return None

df = load_data()

if df is not None:
    # --- سایدبار مدیریتی ---
    with st.sidebar:
        st.image("https://www.wadisteel.com/images/logo.png", width=150) # لوگوی شرکت
        st.title("پنل مدیریت پروژه‌ها")
        selected_project = st.selectbox("انتخاب پروژه فعال:", df['Project_Name'].unique())
        st.divider()
        st.info("کاربر: علی مجیدی | نقش: تحلیل‌گر بحران")

    # فیلتر پروژه
    p_df = df[df['Project_Name'] == selected_project]

    # --- بخش هدر ---
    st.title(f"📊 گزارش وضعیت پروژه: {selected_project}")
    
    # --- شاخص‌های کلیدی (Metrics) با استایل جدید ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("پیشرفت فیزیکی", f"{p_df['Weightage'].iloc[0]}%", "2.5%+")
    m2.metric("شاخص SPI", f"{p_df['SPI(Real)'].mean():.2f}", "-0.12", delta_color="inverse")
    m3.metric("انحراف هزینه (CV)", f"{p_df['CV'].sum():,.0f} H")
    m4.metric("توقفات ثبت شده", f"{len(p_df)} مورد")

    # --- چیدمان داشبورد (نمودارهای پیشرفته) ---
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        # نمودار گیج (Gauge) مثل عکس Watchdog
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = p_df['SPI(Real)'].mean(),
            title = {'text': "سلامت زمانی پروژه"},
            gauge = {'axis': {'range': [0, 2]}, 'bar': {'color': "#1e40af"}}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_right:
        # نمودار درختی (Tree Map) دقیقاً مثل عکس 81 برای تحلیل انحرافات
        st.subheader("تحلیل وزنی انحرافات دپارتمان‌ها")
        fig_tree = px.treemap(p_df, path=['Department', 'Task_Name'], values='Weightage', color='CV',
                              color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_tree, use_container_width=True)

    # --- جدول حرفه‌ای ---
    st.subheader("📋 مانیتورینگ خطوط تولید و فعالیت‌ها")
    st.dataframe(p_df, use_container_width=True)

else:
    st.error("ارتباط با دیتاسنتر برقرار نشد.")
