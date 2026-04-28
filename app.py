import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# تنظیمات پیشرفته صفحه
st.set_page_config(page_title="Wadi Steel Crisis Center", layout="wide")

# اعمال تم اختصاصی و فونت حرفه‌ای
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1a1d23; border: 1px solid #30363d; border-radius: 15px; padding: 20px; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    </style>
    """, unsafe_allow_html=True)

# هدر اصلی با پرستیژ بالا
col_logo, col_title = st.columns([1, 4])
with col_title:
    st.title("🛡️ سامانه پایش استراتژیک وادی استیل")
    st.write("تحلیلگر ارشد بحران: **علی** | واحد کنترل پروژه")

# --- بخش شاخص‌های عقربه‌ای (بسیار حرفه‌ای) ---
st.write("### 🚨 تحلیل وضعیت راندمان و بحران (Crisis Gauge)")
col1, col2 = st.columns(2)

with col1:
    # نمودار عقربه‌ای برای EEF
    fig_eef = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 0.25,
        title = {'text': "شاخص بهره‌وری (EEF)"},
        gauge = {'axis': {'range': [0, 1]},
                 'bar': {'color': "red"},
                 'steps': [
                     {'range': [0, 0.4], 'color': "maroon"},
                     {'range': [0.4, 0.7], 'color': "orange"},
                     {'range': [0.7, 1], 'color': "green"}]}))
    st.plotly_chart(fig_eef, use_container_width=True)

with col2:
    # وضعیت انحراف هزینه
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.metric("انحراف هزینه (CV)", "-518.32 h", "-12% بحرانی", delta_color="inverse")
    st.error("تحلیل کارشناس: انحراف فعلی ناشی از تأخیر در تأمین تجهیزات بخش اسکادا است.")

# --- جدول جزئیات تسک‌ها ---
st.write("---")
with st.expander("🔍 مشاهده جزئیات انحراف فعالیت‌های پروژه"):
    data = {
        "فعالیت": ["نصب سنسورها", "شبکه‌سازی", "کانفیگ نرم‌افزار"],
        "انحراف (ساعت)": [-494.5, -23.8, 0],
        "وضعیت": ["🔥 بحرانی", "⚠️ اخطار", "✅ مطابق برنامه"]
    }
    st.table(pd.DataFrame(data))
