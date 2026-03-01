import streamlit as st
import pandas as pd
import requests

# ตั้งค่าหน้า
st.set_page_config(
    page_title="Self-Caring App",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ชื่อเรื่อง
st.title("🌿 Self-Caring App")
st.markdown("---")

# Sidebar สำหรับเมนูหลัก
st.sidebar.title("📋 เมนู")
page = st.sidebar.radio(
    "เลือกหมวดหมู่:",
    ["🏠 หน้าแรก", "🏥 สาระสุขภาพ", "📞 ติดต่อ"]
)

# ============================================
# หน้าแรก
# ============================================
if page == "🏠 หน้าแรก":
    # ดึงข้อมูลอากาศ
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast?"
            "latitude=19.1767&longitude=99.8844&"     # พะเยา
            "current=temperature_2m,weather_code&timezone=Asia/Bangkok"
        )
        weather_data = response.json()
        current_temp = weather_data["current"]["temperature_2m"]
        weather_code = weather_data["current"]["weather_code"]

        # แปลง weather code เป็น emoji
        weather_emoji = {
            0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
            45: "🌫️", 48: "🌫️", 51: "🌦️", 53: "🌦️",
            55: "🌧️", 61: "🌧️", 63: "⛈️", 65: "⛈️",
            71: "🌨️", 73: "🌨️", 75: "🌨️", 77: "🌨️",
            80: "🌧️", 81: "⛈️", 82: "⛈️", 85: "🌨️",
            86: "🌨️", 95: "⛈️", 96: "⛈️", 99: "⛈️"
        }
        weather_desc = {
            0: "ท้องฟ้าแจ่มใส",        1: "มีแดดออก",        2: "แดดครึ้ม",
            3: "เมฆมาก",              45: "มีหมอก",          48: "มีหมอก",
            51: "เมฆฟ้าครึ้มมีฝนเล็กน้อย", 53: "เมฆฟ้าครึ้มมีฝน", 55: "ฝนตก",
            61: "ฝนตกเบา",            63: "ฝนตกปานกลาง",    65: "ฝนตกหนัก",
            71: "หิมะตกเล็กน้อย",     73: "หิมะตก",          75: "หิมะตกหนัก",
            77: "เม็ดน้ำแข็ง",         80: "ฝนตกเป็นช่วง",    81: "ฝนตกหนักเป็นช่วง",
            82: "พายุฝนฟ้าคะนอง",    85: "หิมะตกปานกลาง",  86: "หิมะตกหนัก",
            95: "พายุฝนฟ้าคะนอง",    96: "พายุฝนฟ้าคะนองกับลูกเห็บ",
            99: "พายุฝนฟ้าคะนองกับลูกเห็บ"
        }
        emoji = weather_emoji.get(weather_code, "🌤️")
        desc = weather_desc.get(weather_code, "มีแดดบางส่วน")
        weather_symbol = f"{emoji} {desc}"

        # ตรวจว่ามีฝนตก (รหัสในกลุ่มฝน/พายุ)
        rainy_codes = {51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99}
        is_raining = weather_code in rainy_codes
    except Exception:
        current_temp = "--"
        weather_symbol = "🌤️"
        is_raining = False

    # แสดงสภาพอากาศกับอุณหภูมิคนละคอลัมน์
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="สภาพอากาศ", value=weather_symbol)
    with col2:
        st.metric(label="อุณหภูมิ", value=f"{current_temp}°C", delta="พะเยา")

    # แจ้งเตือนเมื่อฝนตก
    if is_raining:
        st.warning("☔️ ฝนกำลังตก อย่าลืมพกร่ม/เสื้อกันฝนและระวังถนนลื่น")

    st.markdown("---")

    st.subheader("📌 เคล็ดลับการดูแลตนเอง")
    tips = [
        "🥗 ทานอาหารที่มีสารอาหารครบถ้วน",
        "💤 นอนให้พอเพียง 7-8 ชั่วโมงต่อวัน",
        "🚶 เดินหรือออกกำลังกายอย่างน้อย 30 นาทีต่อวัน",
        "🧘 ทำสมาธิหรือผ่อนคลายใจ 10 นาทีต่อวัน",
        "📱 ลดการใช้โทรศัพท์ก่อนนอน"
    ]
    for tip in tips:
        st.write(tip)

# ============================================
# สาระสุขภาพ
# ============================================
elif page == "🏥 สาระสุขภาพ":
    st.subheader("🏥 สาระสุขภาพ")

    try:
        df = pd.read_csv("output.csv")

        if df.empty:
            st.warning("ไม่พบข้อมูลในไฟล์ CSV")
        else:
            # สร้างรายการตัวเลือกจากไตเติล
            all_titles = df["Title"].unique().tolist()
            all_titles.insert(0, "")

            # เพิ่ม Search Bar พร้อมตัวเลือก
            search_query = st.selectbox(
                "🔍 ค้นหาสาระสุขภาพ",
                options=all_titles,
                key="search_query"
            )
            st.markdown("---")

            # กรองข้อมูลตามการค้นหา
            if search_query == "":
                filtered_df = df
            else:
                filtered_df = df[
                    df["Title"].str.contains(search_query, case=False, na=False) |
                    df["Description"].str.contains(search_query, case=False, na=False)
                ]

            # แสดงจำนวนผลการค้นหา
            if search_query != "":
                st.info(f"พบ {len(filtered_df)} รายการ")

                # แสดงข้อมูลแต่ละรายการ
                if filtered_df.empty:
                    st.warning("ไม่พบหัวข้อที่ตรงกับการค้นหา 😢")
                else:
                    for idx, row in filtered_df.iterrows():
                        title = row["Title"]
                        description = row["Description"]
                        link = row["Link"]

                        # แสดงหัวข้อเป็น link
                        st.markdown(f"### 📌 [{title}]({link})")

                        # แสดง Description
                        st.markdown(f"{description}")

                        # เพิ่มเส้นแบ่งระหว่างรายการ
                        st.markdown("---")
            else:
                # แสดงทั้งหมดเมื่อเลือก "แสดงทั้งหมด"
                for idx, row in df.iterrows():
                    title = row["Title"]
                    description = row["Description"]
                    link = row["Link"]

                    st.markdown(f"### 📌 [{title}]({link})")
                    st.markdown(f"{description}")
                    st.markdown("---")

    except FileNotFoundError:
        st.error("❌ ไม่พบไฟล์ output.csv กรุณาตรวจสอบให้แน่ใจว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")

    st.markdown("---")
    st.write("💚 ดูแลตัวเอง คือการลงทุนที่ดีที่สุด")

# ============================================
# ติดต่อโรงพยาบาล / เว็บไซต์
# ============================================
elif page == "📞 ติดต่อ":
    st.subheader("📞 ติดต่อโรงพยาบาลและเว็บไซต์")
    st.write("🏥 **โรงพยาบาลมหาวิทยาลัยพะเยา**")
    st.write("ที่อยู่: 99 หมู่ 3 ตำบลแม่กา อำเภอเมือง จังหวัดพะเยา 56000")
    st.write("โทร: 054‑466‑666 ต่อ 7000")
    st.write("ห้องฉุกเฉิน: 054-466-758")
    st.write("เว็บไซต์: [www.up.ac.th](https://www.up.ac.th)")
    st.markdown("---")
    st.write("🌐 เว็บไซต์สุขภาพที่น่าสนใจ")
    st.write("- [กระทรวงสาธารณสุข](https://www.moph.go.th)")
    st.write("- [ศูนย์ควบคุมและป้องกันโรค (CDC)](https://www.cdc.gov)")
    st.write("- [สำนักงานสาธารณสุขจังหวัด](https://www.spso.moph.go.th)")
