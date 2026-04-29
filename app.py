import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. تنظیمات هسته و استایل صنعتی پیشرفته
st.set_page_config(page_title="Wadi Steel | Watchdog Hub", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* فونت فارسی حرفه‌ای */
    @import url('https://v1.fontapi.ir/css/Vazirmatn');
    html, body, [class*="css"]  {
        font-family: 'Vazirmatn', sans-serif;
    }
    
    /* مخفی کردن المان‌های اضافی استریم‌لیت */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* استایل کارت‌های شاخص (KPIs) - شبیه Watchdog */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #ffffff, #f1f5f9);
        border: 1px solid #e2e8f0;
        border-right: 5px solid #0284c7; /* نوار آبی رنگ صنعتی */
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* رنگ لیبل شاخص‌ها */
    [data-testid="stMetricLabel"] {
        font-size: 16px;
        color: #475569;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        font-size: 32px;
        color: #0f172a;
    }
    </style>
""", unsafe_allow_html=True)

# 2. اتصال به دیتاسنتر (Webhook میک)
MAKE_API_URL = "https://hook.eu1.make.com/r8ihcn7jgpdp73wljeviquvb8rgkqhib"

@st.cache_data(ttl=30)
def fetch_telemetry_data():
    try:
        response = requests.get(MAKE_API_URL, timeout=15)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            
            # پاک‌سازی و آماده‌سازی داده‌های مهندسی
            numeric_cols = ['CV', 'SV', 'EEF', 'SPI_Real', 'SPI(Real)', 'Weightage', 'Actual_Total_H']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # پر کردن مقادیر خالی برای جلوگیری از ارور
            if 'Department' in df.columns: df['Department'].fillna('نامشخص', inplace=True)
            if 'Project_Name' in df.columns: df['Project_Name'].fillna('پروژه عمومی', inplace=True)
            
            return df
        return None
    except:
        return None

# --- شروع ساختار صفحه ---
df = fetch_telemetry_data()

if df is not None and not df.empty:
    
    # 3. سایدبار مدیریت چند پروژه‌ای (Multi-Project)
    with st.sidebar:
        st.markdown("<h2 style='color:#0284c7; text-align:center;'>⚙️ WADI WATCHDOG</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # انتخابگر پروژه (قلب تپنده‌ی سیستم چند پروژه‌ای)
        project_list = df['Project_Name'].unique().tolist()
        selected_project = st.selectbox("📂 انتخاب پروژه فعال:", project_list)
        
        st.markdown("---")
        st.markdown("<p style='font-size:14px; color:#64748b;'>فیلترهای تخصصی</p>", unsafe_allow_html=True)
        
        # فیلتر کردن دیتابیس بر اساس پروژه انتخاب شده
        p_df = df[df['Project_Name'] == selected_project]
        
        # فیلتر دپارتمان به صورت پویا
        selected_depts = []
        if 'Department' in p_df.columns:
            selected_depts = st.multiselect("🏢 دپارتمان / واحد:", p_df['Department'].unique())
            if selected_depts:
                p_df = p_df[p_df['Department'].isin(selected_depts)]
                
        search_term = st.text_input("🔍 جستجوی فعالیت...")
        if search_term and 'Task_Name' in p_df.columns:
            p_df = p_df[p_df['Task_Name'].str.contains(search_term, na=False)]
            
        st.markdown("<br><br><p style='text-align:center; color:#94a3b8; font-size:12px;'>Core Architecture by Zarovin</p>", unsafe_allow_html=True)

    # 4. هدر اصلی داشبورد
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"<h2 style='color:#1e293b; margin-bottom:0;'>داشبورد پایش استراتژیک: <span style='color:#0284c7;'>{selected_project}</span></h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#64748b; margin-top:0;'>نمای لحظه‌ای انحرافات و پیشرفت فیزیکی خطوط | آپدیت: {datetime.now().strftime('%H:%M')}</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. شاخص‌های کلیدی عملکرد (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    
    cv_sum = p_df['CV'].sum() if 'CV' in p_df.columns else 0
    spi_col = 'SPI(Real)' if 'SPI(Real)' in p_df.columns else ('SPI_Real' if 'SPI_Real' in p_df.columns else None)
    spi_avg = p_df[spi_col].mean() if spi_col else 0
    total_hours = p_df['Actual_Total_H'].sum() if 'Actual_Total_H' in p_df.columns else 0
    
    col1.metric("مجموع انحراف هزینه (CV)", f"{cv_sum:,.0f} H", delta="وضعیت بحرانی" if cv_sum < 0 else "نرمال", delta_color="inverse")
    col2.metric("شاخص سلامت زمان (SPI)", f"{spi_avg:.2f}", delta="تاخیر فاز" if spi_avg < 1 else "جلوتر از برنامه", delta_color="inverse")
    col3.metric("مجموع ساعات کارکرد", f"{total_hours:,.1f} H")
    col4.metric("فعالیت‌های درگیر", f"{len(p_df)} رکورد")

    st.markdown("<br>", unsafe_allow_html=True)

    # 6. پنل نمودارهای تحلیلی (مانند سیستم Watchdog)
    chart_col1, chart_col2 = st.columns([1, 2])

    with chart_col1:
        st.markdown("<h4 style='color:#334155;'>گیج عملکرد زمانی (SPI)</h4>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = spi_avg,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 2], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#0284c7"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#e2e8f0",
                'steps': [
                    {'range': [0, 0.85], 'color': "rgba(239, 68, 68, 0.2)"},   # قرمز (خطر)
                    {'range': [0.85, 1.0], 'color': "rgba(245, 158, 11, 0.2)"}, # زرد (هشدار)
                    {'range': [1.0, 2.0], 'color': "rgba(16, 185, 129, 0.2)"}], # سبز (ایده‌آل)
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 1}
            }))
        fig_gauge.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, use_container_width=True)

    with chart_col2:
        st.markdown("<h4 style='color:#334155;'>درخت انحرافات (Treemap) به تفکیک دپارتمان</h4>", unsafe_allow_html=True)
        if 'Department' in p_df.columns and 'Task_Name' in p_df.columns and 'CV' in p_df.columns:
            # ساخت نمودار درختی دقیقاً مشابه سیستم‌های SCADA
            # از Absolute CV برای سایز باکس‌ها استفاده می‌کنیم تا منفی‌ها هم کشیده شوند
            p_df['Abs_CV'] = p_df['CV'].abs() 
            fig_tree = px.treemap(
                p_df, 
                path=[px.Constant("کل پروژه"), 'Department', 'Task_Name'], 
                values='Abs_CV',
                color='CV', 
                color_continuous_scale='RdYlGn',
                color_continuous_midpoint=0,
                custom_data=['CV', 'Weightage']
            )
            fig_tree.update_traces(hovertemplate='<b>%{label}</b><br>انحراف هزینه: %{customdata[0]:.2f}<br>وزن فیزیکی: %{customdata[1]}%<extra></extra>')
            fig_tree.update_layout(height=320, margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_tree, use_container_width=True)
        else:
            st.warning("داده‌های کافی برای رسم نمودار درختی (ستون‌های دپارتمان، نام تسک، CV) یافت نشد.")

    # 7. دیتاگرید تعاملی و پیشرفته
    st.markdown("---")
    st.markdown("<h4 style='color:#334155;'>📋 ریزتراکنش‌های عملیاتی و توقفات</h4>", unsafe_allow_html=True)
    
    # تنظیمات ستون‌ها برای نمایش حرفه‌ای (Progress bar و فرمت اعداد)
    cols_config = {}
    if 'Weightage' in p_df.columns:
        cols_config["Weightage"] = st.column_config.ProgressColumn("پیشرفت (%)", format="%d%%", min_value=0, max_value=100)
    if 'CV' in p_df.columns:
        cols_config["CV"] = st.column_config.NumberColumn("CV (H)", format="%.1f")
    if spi_col:
        cols_config[spi_col] = st.column_config.NumberColumn("SPI", format="%.2f")

    st.dataframe(
        p_df,
        column_config=cols_config,
        hide_index=True,
        use_container_width=True,
        height=400
    )

else:
    # صفحه لودینگ با استایل صنعتی
    st.info("📡 در حال همگام‌سازی با سرورهای وادی استیل... (لطفاً از اتصال وب‌هوک و وجود داده در نوشن اطمینان حاصل کنید)")
    with st.spinner("Processing Telemetry Data..."):
        pass
