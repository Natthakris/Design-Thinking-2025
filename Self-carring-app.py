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
        # เพิ่ม Search Bar
        search_query = st.text_input("🔍 ค้นหาหัวข้อ", placeholder="พิมพ์คำค้นหา...")
        st.markdown("---")
        
        # กรองข้อมูลตามการค้นหา
        if search_query:
            filtered_df = df[
                df["Title"].str.contains(search_query, case=False, na=False) |
                df["Description"].str.contains(search_query, case=False, na=False)
            ]
        else:
            filtered_df = df
        
        # แสดงจำนวนผลการค้นหา
        if search_query:
            st.info(f"พบ {len(filtered_df)} รายการ")
        
        # แสดงข้อมูลแต่ละรายการ
        if filtered_df.empty and search_query:
            st.warning("ไม่พบหัวข้อที่ตรงกับการค้นหา 😢")
        else:
            for idx, row in filtered_df.iterrows():
                # สร้าง clickable title ที่เป็น link
                title = row["Title"]
                description = row["Description"]
                link = row["Link"]
                
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