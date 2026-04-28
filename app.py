import streamlit as st
import pandas as pd

# تنظیمات ظاهری داشبورد کنترل پروژه
st.set_page_config(page_title="Wadi Steel Project Control", layout="wide")

# استایل اختصاصی برای پرستیژ کاری
st.markdown("""
    <style>
    .main { background-color: #0b0d10; }
    .stMetric { background-color: #1c2128; border-left: 5px solid #00ffcc; border-radius: 5px; padding: 15px; }
    h1 { color: #00ffcc; font-family: 'Tahoma'; }
    </style>
    """, unsafe_allow_html=True)

# عنوان اصلی داشبورد
st.title("📊 سیستم جامع کنترل پروژه وادی استیل")
st.subheader("واحد برنامه‌ریزی و کنترل پروژه - تحلیل انحرافات استراتژیک")
st.write("---")

# منوی کناری
st.sidebar.header("پنل کنترلی")
view_mode = st.sidebar.selectbox("انتخاب لایه گزارش:", ["داشبورد مدیریتی", "تحلیل شاخص‌های زمانی و هزینه‌ای"])

if view_mode == "داشبورد مدیریتی":
    st.write("### 🚨 شاخص‌های کلیدی عملکرد (KPIs)")
    
    col1, col2, col3 = st.columns(3)
    # نمایش CV و EEF با برچسب‌های استاندارد کنترل پروژه
    col1.metric("انحراف هزینه (CV)", "-518.32 h", "بحرانی")
    col2.metric("شاخص بهره‌وری (EEF)", "0.25", "-75%")
    col3.metric("تأخیر تخمینی (FDE)", "14 روز", "نیاز به اقدام")

    st.error("وضعیت پروژه: خارج از محدوده راندمان تعریف شده. نیاز به بازبینی منابع.")

else:
    st.write("### 📉 تحلیل روند انحرافات (Variance Analysis)")
    st.info("این نمودار نشان‌دهنده افت راندمان تیم نسبت به خط مبنا (Baseline) است.")
    # نمودار خطی برای نشان دادن روند
    st.line_chart([0.95, 0.80, 0.55, 0.25])
    st.write("**تحلیل کارشناس کنترل پروژه:** روند نزولی راندمان از هفته سوم شدت گرفته است.")
