import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. تنظیمات صفحه و مخفی کردن المان‌های مبتدیِ استریم‌لیت
st.set_page_config(page_title="Wadi Steel Command Center", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* مخفی کردن منو و واترمارک استریم‌لیت برای حفظ پرستیژ سازمانی */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تم تاریک و صنعتی (SCADA Style) */
    .main { background-color: #050914; color: #E2E8F0; }
    
    /* استایل کارت‌های اطلاعاتی (Glassmorphism) */
    div[data-testid="metric-container"] {
        background-color: #0F172A; 
        border: 1px solid #1E293B; 
        border-left: 4px solid #3B82F6; 
        border-radius: 10px; 
        padding: 20px; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    
    /* شخصی‌سازی فونت و رنگ تیترها */
    h1, h2, h3 { color: #60A5FA !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. هدر اصلی (Enterprise Command Center)
st.markdown("""
    <div style='background-color: #0F172A; padding: 25px; border-radius: 12px; border-bottom: 2px solid #3B82F6; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.6);'>
        <h1 style='text-align: center; margin:0; letter-spacing: 2px;'>🛡️ WADI STEEL | STRATEGIC COMMAND CENTER</h1>
        <p style='text-align: center; color: #9CA3AF; font-size: 15px; margin:0; letter-spacing: 1px; margin-top: 5px;'>PROJECT CONTROL & CRISIS ANALYSIS SYSTEM</p>
    </div>
""", unsafe_allow_html=True)

# 3. داشبورد مدیریتی (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("وضعیت یکپارچگی سیستم", "98.5%", "پایدار", delta_color="normal")
col2.metric("انحراف هزینه (CV)", "-518.3 h", "بحرانی - نیاز به اقدام", delta_color="inverse")
col3.metric("راندمان کلی (EEF)", "25%", "-75% افت نسبت به بیس‌لاین", delta_color="inverse")
col4.metric("تأخیر تخمینی", "14 روز", "اخطار فاز 2", delta_color="inverse")

st.markdown("<br><br>", unsafe_allow_html=True)

# 4. نمودارهای پیشرفته تعاملی (Plotly)
chart_col1, chart_col2 = st.columns([1, 2])

with chart_col1:
    st.markdown("<h3 style='text-align:center;'>🚨 مانیتورینگ بحران (Pulse)</h3>", unsafe_allow_html=True)
    # نمودار عقربه‌ای (Gauge) با استایل تاریک
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 0.25,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ضریب بهره‌وری (EEF)", 'font': {'color': '#9CA3AF'}},
        gauge = {
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#EF4444"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 1,
            'bordercolor': "#1E293B",
            'steps': [
                {'range': [0, 0.3], 'color': "rgba(239, 68, 68, 0.2)"},
                {'range': [0.3, 0.7], 'color': "rgba(245, 158, 11, 0.2)"},
                {'range': [0.7, 1.0], 'color': "rgba(16, 185, 129, 0.2)"}],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0.25}}))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=350, margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig_gauge, use_container_width=True)

with chart_col2:
    st.markdown("### 📊 تحلیل انحرافات به تفکیک دپارتمان")
    # نمودار میله‌ای افقی حرفه‌ای
    df = pd.DataFrame({
        "دپارتمان": ["اسکادا", "زیرساخت شبکه", "سخت‌افزار", "برنامه‌نویسی"],
        "ساعت انحراف": [-320, -100, -80, -18.3]
    })
    fig_bar = px.bar(df, x="ساعت انحراف", y="دپارتمان", orientation='h', color="ساعت انحراف", color_continuous_scale="Reds_r")
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#9CA3AF"},
        xaxis=dict(showgrid=True, gridcolor='#1E293B', title="انحراف (ساعت)"),
        yaxis=dict(showgrid=False, title=""),
        height=350,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 5. دیتاگرید (جدول تسک‌ها)
st.markdown("---")
st.markdown("### 📋 لاگ عملیاتی تسک‌های بحرانی")
tasks_df = pd.DataFrame({
    "کد فعالیت": ["WS-01", "WS-02", "WS-03"],
    "شرح فعالیت": ["نصب سنسورهای مانیتورینگ", "پیکربندی سرور محلی", "تست شبکه اسکادا"],
    "وضعیت فعلی": ["🔴 متوقف (بحران)", "🟡 در حال انجام (با تاخیر)", "🟢 مطابق برنامه"],
    "مدیر مسئول": ["تیم فنی", "واحد معماری سیستم", "واحد کنترل پروژه"]
})
st.dataframe(tasks_df, use_container_width=True, hide_index=True)
