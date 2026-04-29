import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# 1. تنظیمات هسته و استایل صنعتی (SCADA Theme)
st.set_page_config(page_title="Wadi Steel | Command Center", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1.5rem;}
    
    /* استایل کارت‌های متریک */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #0f172a, #1e293b);
        border-left: 4px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    </style>
""", unsafe_allow_html=True)

# 2. آدرس وب‌هوک میک.کام (لینک خودت را اینجا بگذار)
MAKE_API_URL = "لینک_وب‌هوک_خودت_را_اینجا_پیست_کن"

# 3. موتور دریافت داده با کش هوشمند
@st.cache_data(ttl=30) # رفرش هر 30 ثانیه
def fetch_telemetry_data():
    try:
        response = requests.get(MAKE_API_URL, timeout=10)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            # تبدیل ستون‌های عددی به فرمت قابل محاسبه
            numeric_cols = ['CV', 'SV', 'EEF', 'SPI_Real', 'Weightage', 'Actual_Total_H']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            return df
        return None
    except Exception as e:
        return None

# 4. هدر اصلی مرکز فرماندهی
st.markdown("""
    <div style='background-color: #020617; padding: 20px; border-radius: 10px; border-bottom: 2px solid #3b82f6; margin-bottom: 25px;'>
        <h1 style='text-align: center; color: #f8fafc; font-family: sans-serif; letter-spacing: 2px; margin:0;'>🛡️ WADI STEEL STRATEGIC COMMAND</h1>
        <p style='text-align: center; color: #94a3b8; font-size: 14px; margin:0; margin-top: 5px;'>REAL-TIME CRISIS ANALYSIS & PROJECT CONTROL</p>
    </div>
""", unsafe_allow_html=True)

df = fetch_telemetry_data()

if df is not None and not df.empty:
    
    # 5. سایدبار حرفه‌ای برای فیلترینگ
    with st.sidebar:
        st.markdown("<h2 style='color:#60a5fa;'>⚙️ پنل کنترل مانیتورینگ</h2>", unsafe_allow_html=True)
        st.markdown("---")
        search_term = st.text_input("🔍 جستجوی شناسه یا نام فعالیت:")
        
        # فیلترهای پویا بر اساس دیتای موجود
        if 'Department' in df.columns:
            selected_depts = st.multiselect("🏢 فیلتر دپارتمان:", df['Department'].dropna().unique())
        if 'Status' in df.columns:
            selected_status = st.multiselect("🚦 وضعیت فعالیت:", df['Status'].dropna().unique())

    # اعمال فیلترها روی دیتافریم
    filtered_df = df.copy()
    if search_term and 'Task_Name' in df.columns:
        filtered_df = filtered_df[filtered_df['Task_Name'].str.contains(search_term, na=False)]
    if 'selected_depts' in locals() and selected_depts:
        filtered_df = filtered_df[filtered_df['Department'].isin(selected_depts)]
    if 'selected_status' in locals() and selected_status:
        filtered_df = filtered_df[filtered_df['Status'].isin(selected_status)]

    # 6. محاسبه شاخص‌های کلیدی (KPIs)
    total_cv = filtered_df['CV'].sum()
    avg_spi = filtered_df['SPI_Real'].mean()
    total_hours = filtered_df['Actual_Total_H'].sum()

    col1, col2, col3, col4 = st.columns(4)
    
    # لاجیک رنگ‌بندی داینامیک برای بحران
    cv_color = "normal" if total_cv >= 0 else "inverse"
    spi_color = "normal" if avg_spi >= 1 else "inverse"

    col1.metric("مجموع انحراف هزینه (CV)", f"{total_cv:,.1f} H", delta="بحرانی" if total_cv < 0 else "پایدار", delta_color=cv_color)
    col2.metric("شاخص عملکرد زمان (SPI)", f"{avg_spi:.2f}", delta="تاخیر فاز" if avg_spi < 1 else "جلوتر از برنامه", delta_color=spi_color)
    col3.metric("مجموع ساعات کارکرد (Actual)", f"{total_hours:,.1f} H")
    col4.metric("فعالیت‌های در حال پایش", f"{len(filtered_df)} تسک")

    st.markdown("<br>", unsafe_allow_html=True)

    # 7. داشبورد تحلیلی تصویری (Plotly)
    chart_col1, chart_col2 = st.columns([1, 2])

    with chart_col1:
        st.markdown("<h4 style='color:#cbd5e1;'>وضعیت سلامت کلی (SPI Pulse)</h4>", unsafe_allow_html=True)
        # نمودار گیج (عقربه‌ای) برای SPI
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_spi,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 2], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#3b82f6"},
                'bgcolor': "#0f172a",
                'borderwidth': 2,
                'bordercolor': "#1e293b",
                'steps': [
                    {'range': [0, 0.8], 'color': "rgba(239, 68, 68, 0.4)"},  # قرمز
                    {'range': [0.8, 1.0], 'color': "rgba(245, 158, 11, 0.4)"}, # زرد
                    {'range': [1.0, 2.0], 'color': "rgba(16, 185, 129, 0.4)"}], # سبز
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 1}
            }))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#f8fafc"}, height=300, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with chart_col2:
        st.markdown("<h4 style='color:#cbd5e1;'>توزیع انحراف هزینه (CV) به تفکیک دپارتمان</h4>", unsafe_allow_html=True)
        if 'Department' in filtered_df.columns and 'CV' in filtered_df.columns:
            dept_cv = filtered_df.groupby('Department')['CV'].sum().reset_index()
            fig_bar = px.bar(dept_cv, x='CV', y='Department', orientation='h', 
                             color='CV', color_continuous_scale='RdYlGn')
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "#f8fafc"}, height=300, margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor='#1e293b'), yaxis={'title': ''}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # 8. دیتاگرید پیشرفته (Interactive Table)
    st.markdown("---")
    st.markdown("<h3 style='color:#60a5fa;'>📋 لاگ عملیاتی و ریزتراکنش‌های پروژه</h3>", unsafe_allow_html=True)
    
    # استفاده از data_editor برای نمایش زیباتر و قابلیت مرتب‌سازی حرفه‌ای
    st.dataframe(
        filtered_df,
        column_config={
            "Weightage": st.column_config.ProgressColumn("وزن فیزیکی (%)", format="%d%%", min_value=0, max_value=100),
            "CV": st.column_config.NumberColumn("انحراف هزینه (CV)", format="%.2f H"),
            "SPI_Real": st.column_config.NumberColumn("SPI", format="%.2f"),
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

else:
    # صفحه لودینگ حرفه‌ای
    st.info("📡 در حال برقراری ارتباط امن با سرورهای مرکزی (Make API) و همگام‌سازی داده‌ها... لطفاً شکیبا باشید.")
    st.caption("در صورت طولانی شدن، از اتصال صحیح Webhook و وجود داده در دیتابیس اطمینان حاصل کنید.")
