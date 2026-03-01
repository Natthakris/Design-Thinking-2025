import streamlit as st
import pandas as pd

# กำหนดค่า page configuration
st.set_page_config(page_title="Self-Caring App", layout="wide")

# หัวข้อแอปพลิเคชัน
st.title("🌿 Self-Caring App")
st.markdown("---")

# อ่านข้อมูลจากไฟล์ CSV
try:
    df = pd.read_csv("output.csv")
    
    if df.empty:
        st.warning("ไม่พบข้อมูลในไฟล์ CSV")
    else:
        # แสดงข้อมูลแต่ละรายการ
        for idx, row in df.iterrows():
            # สร้าง clickable title ที่เป็น link
            title = row["Title"]
            description = row["Description"]
            link = row["link"]
            
            # แสดงหัวข้อเป็น link
            st.markdown(f"### [{title}]({link})")
            
            # แสดง Description
            st.markdown(f"**{description}**")
            
            # เพิ่มเส้นแบ่งระหว่างรายการ
            st.markdown("---")
            
except FileNotFoundError:
    st.error("❌ ไม่พบไฟล์ output.csv กรุณาตรวจสอบให้แน่ใจว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาด: {e}")