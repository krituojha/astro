# app.py
import datetime
import streamlit as st
from horoscope import get_daily_horoscope
from tithi import get_today_tithi

st.set_page_config(page_title="🪐 Astro Assistant", layout="centered")

st.title("🪐 SK Pandey Astrology Assistant ")
st.markdown("Ask about today's **horoscope**, **tithi**, or **gemstone**.")

query_type = st.radio("Choose your query:", ["Today's Horoscope", "Aaj ki Tithi", "Gemstone Suggestion"])

if query_type == "Today's Horoscope":
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign = st.selectbox("🔯 Select your zodiac sign", signs)
    if st.button("Get Horoscope"):
        result = get_daily_horoscope(sign.lower())
        st.success(result)

elif query_type == "Aaj ki Tithi":
    if st.button("🔎 Fetch Today’s Tithi"):
        result = get_today_tithi()
        st.info(result)
elif query_type == "Gemstone Suggestion":
    name = st.text_input("Name")
    
    # Updated date input to support 1930-now
    min_date = datetime.date(1930, 1, 1)
    max_date = datetime.date.today()
    dob = st.date_input(
        "Date of Birth",
        min_value=min_date,
        max_value=max_date,
        value=datetime.date(1990, 1, 1)  # Default value
    )
    
    tob = st.time_input("Time of Birth")
    pob = st.text_input("Place of Birth", "Delhi")  # Default to Delhi
    weight = st.number_input("Weight (in kg)", min_value=1.0, value=60.0)  # Default weight

    if st.button("Suggest Gemstone"):
        from gemstone import gemstone_recommendation
        try:
            # Convert date to YYYY-MM-DD format
            dob_str = dob.strftime("%Y-%m-%d")
            tob_str = tob.strftime("%H:%M")
            
            result = gemstone_recommendation(dob_str, tob_str, pob, weight)

            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Moon Sign: {result['moon_sign']} | Lagna: {result['lagna_sign']}")
                st.markdown(f"""
                - 💎 Gemstone (Moon): **{result['moon_gem']}** ({result['moon_planet']})
                - 💠 Ratti: {result['ratti']}
                - 🧿 Wear on **{result['wear_day']}** in **{result['wear_finger']}** using **{result['wear_metal']}** Mantra **{result['mantra']}**
                - 🔄 Mahadasha Planet: **{result['dasha_planet']}** → Consider: **{result['dasha_gem']}**
                """)

                st.markdown("#### 🛒 Purchase Options")
                for site in result["purchase_links"]:
                    st.markdown(f"- [{site['name']}]({site['url']})")

                if st.button("📄 Download PDF"):
                    from generate_pdf import create_gemstone_pdf
                    path = create_gemstone_pdf(name, result)
                    with open(path, "rb") as file:
                        st.download_button("Download PDF", file, file_name="Gemstone_Advice.pdf")
                        
        except Exception as e:
            st.error(f"Error calculating gemstone recommendation: {str(e)}")

# elif query_type == "Gemstone Suggestion":
#     st.warning("💎 Feature coming soon: Provide DOB, TOB, POB for your Vedic gemstone suggestion.")
#     name = st.text_input("Name")
#     dob = st.date_input("Date of Birth")
#     tob = st.time_input("Time of Birth")
#     pob = st.text_input("Place of Birth")
#     if st.button("Suggest Gemstone"):
#         st.info("🪬 Based on your birth chart, gemstone suggestion feature is in progress.")
