from datetime import datetime, timedelta
import swisseph as swe

# Initialize Swiss Ephemeris with extended ephemeris path if needed
swe.set_ephe_path()
# English Data
GEMSTONE_DATA_EN = {
    "mars":      ("Red Coral",     "Tuesday",  "Ring", "Copper or Silver", "Ring finger", "Om Mangalaya Namah"),
    "venus":     ("Diamond",       "Friday",   "Ring", "Silver or Platinum", "Middle finger", "Om Shukraya Namah"),
    "mercury":   ("Emerald",       "Wednesday","Ring", "Gold",              "Little finger", "Om Budhaya Namah"),
    "moon":      ("Pearl",         "Monday",   "Ring", "Silver",            "Little finger", "Om Somaya Namah"),
    "sun":       ("Ruby",          "Sunday",   "Ring", "Gold or Copper",    "Ring finger", "Om Suryaya Namah"),
    "jupiter":   ("Yellow Sapphire","Thursday","Ring", "Gold",              "Index finger", "Om Brihaspataye Namah"),
    "saturn":    ("Blue Sapphire", "Saturday", "Ring", "Iron or Silver",    "Middle finger", "Om Shanaischaraya Namah"),
    "rahu":      ("Hessonite",     "Saturday", "Ring", "Silver",            "Middle finger", "Om Rahave Namah"),
    "ketu":      ("Cat's Eye",     "Tuesday",  "Ring", "Silver",            "Little finger", "Om Ketave Namah"),
}

# Hindi Data
GEMSTONE_DATA_HI = {
    "mars":      ("मूंगा",          "मंगलवार",   "अंगूठी", "तांबा या चांदी", "अनामिका", "ॐ मंगलाय नमः"),
    "venus":     ("हीरा",           "शुक्रवार",  "अंगूठी", "चांदी या प्लैटिनम", "मध्यमा", "ॐ शुक्राय नमः"),
    "mercury":   ("पन्ना",          "बुधवार",    "अंगूठी", "सोना",            "कनिष्ठिका", "ॐ बुधाय नमः"),
    "moon":      ("मोती",           "सोमवार",    "अंगूठी", "चांदी",           "कनिष्ठिका", "ॐ सोमाय नमः"),
    "sun":       ("माणिक्य",         "रविवार",    "अंगूठी", "सोना या तांबा",   "अनामिका", "ॐ सूर्याय नमः"),
    "jupiter":   ("पुखराज",         "गुरुवार",   "अंगूठी", "सोना",            "तर्जनी", "ॐ बृहस्पतये नमः"),
    "saturn":    ("नीलम",           "शनिवार",    "अंगूठी", "लोहा या चांदी",   "मध्यमा", "ॐ शनैश्चराय नमः"),
    "rahu":      ("गोमेद",          "शनिवार",    "अंगूठी", "चांदी",           "मध्यमा", "ॐ राहवे नमः"),
    "ketu":      ("लहसुनिया",       "मंगलवार",   "अंगूठी", "चांदी",           "कनिष्ठिका", "ॐ केतवे नमः"),
}

ZODIAC_SIGNS_EN = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

ZODIAC_SIGNS_HI = [
    "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
    "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"
]

PLANET_NAMES_EN = {
    "sun": "Sun",
    "moon": "Moon",
    "mars": "Mars",
    "mercury": "Mercury",
    "jupiter": "Jupiter",
    "venus": "Venus",
    "saturn": "Saturn",
    "rahu": "Rahu",
    "ketu": "Ketu"
}

PLANET_NAMES_HI = {
    "sun": "सूर्य",
    "moon": "चंद्र",
    "mars": "मंगल",
    "mercury": "बुध",
    "jupiter": "गुरु",
    "venus": "शुक्र",
    "saturn": "शनि",
    "rahu": "राहु",
    "ketu": "केतु"
}

TRUSTED_SITES = [
    {"name": "GemPundit", "url": "https://www.gempundit.com"},
    {"name": "Gemstone Universe", "url": "https://www.gemstoneuniverse.com"},
    {"name": "Khanna Gems", "url": "https://www.khannagems.com"},
]


# Extended date range support (1970 to today)
def validate_date(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        min_date = datetime(1970, 1, 1)
        max_date = datetime.now()
        if not (min_date <= birth_date <= max_date):
            raise ValueError(f"Date must be between {min_date.year} and {max_date.year}")
        return True
    except ValueError as e:
        raise ValueError(f"Invalid date: {str(e)}")

def calculate_jd(dob, tob, offset_hrs):
    try:
        # Convert to datetime and adjust to UTC
        dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        dt_utc = dt - timedelta(hours=offset_hrs)
        print({dob})
        # Julian Day (UT)
        jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                       dt_utc.hour + dt_utc.minute / 60.0)
        return jd
    except Exception as e:
        raise ValueError(f"Invalid date/time format: {str(e)}")

def get_sign(jd, planet, language='en'):
    try:
        # Set the ayanamsa to Lahiri (most commonly used in Vedic astrology)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        ayanamsa = swe.get_ayanamsa(jd)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
        
        zodiac_signs = ZODIAC_SIGNS_HI if language == 'hi' else ZODIAC_SIGNS_EN
        
        # if planet is None:  # For ascendant calculation
        #     lat, lon = 28.6139, 77.2090  # Delhi coordinates
        #     # Use full house calculation with sidereal zodiac
        #     houses = swe.houses_ex(jd, lat, lon, b'P', flags)
        #     asc_deg = houses[0][0]  # No need to subtract ayanamsa
        #     sign_index = int(asc_deg // 30)
        #     return zodiac_signs[sign_index]
        
        # Calculate planet position in sidereal zodiac
        # planet_data = swe.calc_ut(jd, planet, flags)
        # planet_longitude = planet_data[0][0]  # Already sidereal
        # sign_index = int(planet_longitude // 30)
        # Get sidereal moon position (Lahiri)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        planet_longitude = swe.calc_ut(jd, swe.MOON, flags)[0][0]  # Only get longitude
        sign_index = int(planet_longitude // 30)
        print(zodiac_signs[sign_index])
        return zodiac_signs[sign_index]
    
    except Exception as e:
        raise ValueError(f"Error calculating sign: {str(e)}")

# Test function for specific date
def test_karak_rashi():
    dob = "1987-04-08"
    tob = "04:00"  # Noon time for testing
    jd = calculate_jd(dob, tob, 5.5)
    
    # Get Moon sign (Karak Rashi)
    moon_sign = get_sign(jd, swe.MOON)
    print(f"Moon Sign (Karak Rashi) for {dob} Delhi: {moon_sign}")
  
# Run test
test_karak_rashi()

def get_dasha_info(jd, language='en'):
    moon_longitude = swe.calc_ut(jd, swe.MOON)[0][0]
    moon_deg = moon_longitude % 30
    nak_index = int(moon_deg // (13 + 1/3))
    
    dasha_planets = ["ketu", "venus", "sun", "moon", "mars", "rahu", "jupiter", "saturn", "mercury"]
    dasha_planet = dasha_planets[nak_index % 9]
    
    dasha_balance = (1 - (moon_deg % (13 + 1/3)) / (13 + 1/3)) * 100
    
    planet_names = PLANET_NAMES_HI if language == 'hi' else PLANET_NAMES_EN
    return dasha_planet, round(dasha_balance, 2), planet_names[dasha_planet]
    
def moon_sign_to_planet_and_gem(sign, language='en'):
    if language == 'hi':
        mapping = {
            "मेष": ("मंगल", "मूंगा"),
            "वृषभ": ("शुक्र", "हीरा"),
            "मिथुन": ("बुध", "पन्ना"),
            "कर्क": ("चंद्र", "मोती"),
            "सिंह": ("सूर्य", "माणिक्य"),
            "कन्या": ("बुध", "पन्ना"),
            "तुला": ("शुक्र", "हीरा"),
            "वृश्चिक": ("मंगल", "मूंगा"),
            "धनु": ("गुरु", "पुखराज"),
            "मकर": ("शनि", "नीलम"),
            "कुंभ": ("शनि", "नीलम"),
            "मीन": ("गुरु", "पुखराज")
        }
    else:
        mapping = {
            "aries": ("Mars", "Red Coral"),
            "taurus": ("Venus", "Diamond"),
            "gemini": ("Mercury", "Emerald"),
            "cancer": ("Moon", "Pearl"),
            "leo": ("Sun", "Ruby"),
            "virgo": ("Mercury", "Emerald"),
            "libra": ("Venus", "Diamond"),
            "scorpio": ("Mars", "Red Coral"),
            "sagittarius": ("Jupiter", "Yellow Sapphire"),
            "capricorn": ("Saturn", "Blue Sapphire"),
            "aquarius": ("Saturn", "Blue Sapphire"),
            "pisces": ("Jupiter", "Yellow Sapphire")
        }
    return mapping[sign]


def gemstone_recommendation(dob, tob, pob="Delhi", weight_kg=None, language='en'):
    try:
        # Validate date range
        validate_date(dob)
        
        offset = 5.5  # IST
        jd = calculate_jd(dob, tob, offset)
        
        # Set location and topocentric position
        lat, lon = 28.6139, 77.2090  # Default to Delhi
        swe.set_topo(lon, lat, 0)
        
        # Get signs with more precise calculations
        moon_sign = get_sign(jd, swe.MOON, language)
        moon_planet, moon_gem = moon_sign_to_planet_and_gem(moon_sign, language)
        
        sun_sign = get_sign(jd, swe.SUN, language)
        lagna_sign = get_sign(jd, None, language)
        lagna_planet, lagna_gem = moon_sign_to_planet_and_gem(lagna_sign, language)

        # Dasha calculation
        dasha_planet, dasha_balance, dasha_planet_name = get_dasha_info(jd, language)
        gemstone_data = GEMSTONE_DATA_HI if language == 'hi' else GEMSTONE_DATA_EN
        dasha_instr = gemstone_data[dasha_planet.lower()]
        moon_instr = gemstone_data[moon_planet.lower()]

        # Weight/ratti calculation
        ratti = round(weight_kg * 2, 1) if weight_kg else None
        ratti_text = f"{ratti} {'रत्ती' if language == 'hi' else 'ratti'}" if ratti else "Not specified"

        return {
            "moon_sign": moon_sign,
            "sun_sign": sun_sign,
            "lagna_sign": lagna_sign,
            "moon_planet": moon_planet,
            "lagna_planet": lagna_planet,
            "moon_gem": moon_gem,
            "lagna_gem": lagna_gem,
            "dasha_planet": dasha_planet_name,
            "dasha_balance": dasha_balance,
            "dasha_gem": dasha_instr[0],
            "ratti": ratti_text,
            "wear_metal": moon_instr[3],  # Changed from 'metal' to 'wear_metal'
            "wear_finger": moon_instr[4],  # Changed from 'finger' to 'wear_finger'
            "wear_day": moon_instr[1],  # Changed from 'day' to 'wear_day'
            "mantra": moon_instr[5],
            "purchase_links": TRUSTED_SITES,
            "language": language
        }

    except Exception as e:
        return {"error": str(e), "language": language}
# from datetime import datetime, timedelta
# import swisseph as swe

# # English Data
# GEMSTONE_DATA_EN = {
#     "mars":      ("Red Coral",     "Tuesday",  "Ring", "Copper or Silver", "Ring finger", "Om Mangalaya Namah"),
#     "venus":     ("Diamond",       "Friday",   "Ring", "Silver or Platinum", "Middle finger", "Om Shukraya Namah"),
#     "mercury":   ("Emerald",       "Wednesday","Ring", "Gold",              "Little finger", "Om Budhaya Namah"),
#     "moon":      ("Pearl",         "Monday",   "Ring", "Silver",            "Little finger", "Om Somaya Namah"),
#     "sun":       ("Ruby",          "Sunday",   "Ring", "Gold or Copper",    "Ring finger", "Om Suryaya Namah"),
#     "jupiter":   ("Yellow Sapphire","Thursday","Ring", "Gold",              "Index finger", "Om Brihaspataye Namah"),
#     "saturn":    ("Blue Sapphire", "Saturday", "Ring", "Iron or Silver",    "Middle finger", "Om Shanaischaraya Namah"),
#     "rahu":      ("Hessonite",     "Saturday", "Ring", "Silver",            "Middle finger", "Om Rahave Namah"),
#     "ketu":      ("Cat's Eye",     "Tuesday",  "Ring", "Silver",            "Little finger", "Om Ketave Namah"),
# }

# # Hindi Data
# GEMSTONE_DATA_HI = {
#     "mars":      ("मूंगा",          "मंगलवार",   "अंगूठी", "तांबा या चांदी", "अनामिका", "ॐ मंगलाय नमः"),
#     "venus":     ("हीरा",           "शुक्रवार",  "अंगूठी", "चांदी या प्लैटिनम", "मध्यमा", "ॐ शुक्राय नमः"),
#     "mercury":   ("पन्ना",          "बुधवार",    "अंगूठी", "सोना",            "कनिष्ठिका", "ॐ बुधाय नमः"),
#     "moon":      ("मोती",           "सोमवार",    "अंगूठी", "चांदी",           "कनिष्ठिका", "ॐ सोमाय नमः"),
#     "sun":       ("माणिक्य",         "रविवार",    "अंगूठी", "सोना या तांबा",   "अनामिका", "ॐ सूर्याय नमः"),
#     "jupiter":   ("पुखराज",         "गुरुवार",   "अंगूठी", "सोना",            "तर्जनी", "ॐ बृहस्पतये नमः"),
#     "saturn":    ("नीलम",           "शनिवार",    "अंगूठी", "लोहा या चांदी",   "मध्यमा", "ॐ शनैश्चराय नमः"),
#     "rahu":      ("गोमेद",          "शनिवार",    "अंगूठी", "चांदी",           "मध्यमा", "ॐ राहवे नमः"),
#     "ketu":      ("लहसुनिया",       "मंगलवार",   "अंगूठी", "चांदी",           "कनिष्ठिका", "ॐ केतवे नमः"),
# }

# ZODIAC_SIGNS_EN = [
#     "aries", "taurus", "gemini", "cancer", "leo", "virgo",
#     "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
# ]

# ZODIAC_SIGNS_HI = [
#     "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
#     "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"
# ]

# PLANET_NAMES_EN = {
#     "sun": "Sun",
#     "moon": "Moon",
#     "mars": "Mars",
#     "mercury": "Mercury",
#     "jupiter": "Jupiter",
#     "venus": "Venus",
#     "saturn": "Saturn",
#     "rahu": "Rahu",
#     "ketu": "Ketu"
# }

# PLANET_NAMES_HI = {
#     "sun": "सूर्य",
#     "moon": "चंद्र",
#     "mars": "मंगल",
#     "mercury": "बुध",
#     "jupiter": "गुरु",
#     "venus": "शुक्र",
#     "saturn": "शनि",
#     "rahu": "राहु",
#     "ketu": "केतु"
# }

# TRUSTED_SITES = [
#     {"name": "GemPundit", "url": "https://www.gempundit.com"},
#     {"name": "Gemstone Universe", "url": "https://www.gemstoneuniverse.com"},
#     {"name": "Khanna Gems", "url": "https://www.khannagems.com"},
# ]

# def calculate_jd(dob, tob, offset_hrs):
#     dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
#     utc_time = dt - timedelta(hours=offset_hrs)
#     jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_time.hour + utc_time.minute / 60)
#     return jd

# def get_sign(jd, planet, language='en'):
#     if planet is None:  # Special handling for ascendant
#         lat, lon = 28.6139, 77.2090  # Default Delhi coordinates
#         asc_deg = swe.houses(jd, lat, lon)[1][0]
#         zodiac_signs = ZODIAC_SIGNS_HI if language == 'hi' else ZODIAC_SIGNS_EN
#         return zodiac_signs[int(asc_deg // 30)]
    
#     planet_data = swe.calc_ut(jd, planet)
#     longitude = planet_data[0][0]
#     zodiac_signs = ZODIAC_SIGNS_HI if language == 'hi' else ZODIAC_SIGNS_EN
#     return zodiac_signs[int(longitude // 30)]

# def moon_sign_to_planet_and_gem(sign, language='en'):
#     if language == 'hi':
#         mapping = {
#             "मेष": ("मंगल", "मूंगा"),
#             "वृषभ": ("शुक्र", "हीरा"),
#             "मिथुन": ("बुध", "पन्ना"),
#             "कर्क": ("चंद्र", "मोती"),
#             "सिंह": ("सूर्य", "माणिक्य"),
#             "कन्या": ("बुध", "पन्ना"),
#             "तुला": ("शुक्र", "हीरा"),
#             "वृश्चिक": ("मंगल", "मूंगा"),
#             "धनु": ("गुरु", "पुखराज"),
#             "मकर": ("शनि", "नीलम"),
#             "कुंभ": ("शनि", "नीलम"),
#             "मीन": ("गुरु", "पुखराज")
#         }
#     else:
#         mapping = {
#             "aries": ("Mars", "Red Coral"),
#             "taurus": ("Venus", "Diamond"),
#             "gemini": ("Mercury", "Emerald"),
#             "cancer": ("Moon", "Pearl"),
#             "leo": ("Sun", "Ruby"),
#             "virgo": ("Mercury", "Emerald"),
#             "libra": ("Venus", "Diamond"),
#             "scorpio": ("Mars", "Red Coral"),
#             "sagittarius": ("Jupiter", "Yellow Sapphire"),
#             "capricorn": ("Saturn", "Blue Sapphire"),
#             "aquarius": ("Saturn", "Blue Sapphire"),
#             "pisces": ("Jupiter", "Yellow Sapphire")
#         }
#     return mapping[sign]

# def get_dasha_info(jd, language='en'):
#     moon_longitude = swe.calc_ut(jd, swe.MOON)[0][0]
#     moon_deg = moon_longitude % 30
#     nak_index = int(moon_deg // (13 + 1/3))
    
#     dasha_planets = ["ketu", "venus", "sun", "moon", "mars", "rahu", "jupiter", "saturn", "mercury"]
#     dasha_planet = dasha_planets[nak_index % 9]
    
#     dasha_balance = (1 - (moon_deg % (13 + 1/3)) / (13 + 1/3)) * 100
    
#     planet_names = PLANET_NAMES_HI if language == 'hi' else PLANET_NAMES_EN
#     return dasha_planet, round(dasha_balance, 2), planet_names[dasha_planet]

# def gemstone_recommendation(dob, tob, pob="Delhi", weight_kg=None, language='en'):
#     try:
#         offset = 5.5  # IST
#         jd = calculate_jd(dob, tob, offset)
        
#         lat, lon = 28.6139, 77.2090
#         swe.set_topo(lon, lat, 0)

#         # Get signs
#         moon_sign = get_sign(jd, swe.MOON, language)
#         moon_planet, moon_gem = moon_sign_to_planet_and_gem(moon_sign, language)
        
#         sun_sign = get_sign(jd, swe.SUN, language)
#         sun_planet, sun_gem = moon_sign_to_planet_and_gem(sun_sign, language)

#         # Get Ascendant
#         lagna_sign = get_sign(jd, None, language)
#         lagna_planet, lagna_gem = moon_sign_to_planet_and_gem(lagna_sign, language)

#         # Dasha info
#         dasha_planet, dasha_balance, dasha_planet_name = get_dasha_info(jd, language)
#         gemstone_data = GEMSTONE_DATA_HI if language == 'hi' else GEMSTONE_DATA_EN
#         dasha_instr = gemstone_data[dasha_planet]
#         moon_instr = gemstone_data[moon_planet.lower()]

#         # Weight calculation
#         if weight_kg:
#             ratti = round(weight_kg * 2, 1)
#             ratti_text = f"{ratti} {'रत्ती' if language == 'hi' else 'ratti'}"
#         else:
#             ratti_text = "निर्दिष्ट नहीं" if language == 'hi' else "Not provided"

#         # Create response dictionary with all required fields
#         response = {
#             "moon_sign": moon_sign,
#             "sun_sign": sun_sign,
#             "lagna_sign": lagna_sign,
#             "moon_gem": moon_gem,
#             "lagna_gem": lagna_gem,
#             "moon_planet": moon_planet,  # Added this field
#             "lagna_planet": lagna_planet,  # Added this field
#             "dasha_info": f"{dasha_planet_name} ({dasha_balance}% {'शेष' if language == 'hi' else 'remaining'})",
#             "dasha_gem": dasha_instr[0],
#             "weight": ratti_text,
#             "metal": moon_instr[3],
#             "finger": moon_instr[4],
#             "day": moon_instr[1],
#             "mantra": moon_instr[5],
#             "language": language
#         }

#         return response

#     except Exception as e:
#         error_msg = str(e)
#         return {"error": error_msg, "language": language}
# Example usage:
# English output
# print(gemstone_recommendation("1990-05-15", "08:30", weight_kg=60))

# Hindi output
# print(gemstone_recommendation("1990-05-15", "08:30", weight_kg=60, language='hi'))
# from datetime import datetime, timedelta
# import swisseph as swe
# import pytz

# # Mapping: planet -> (gemstone, wear_day, ring_type, metal, finger)
# GEMSTONE_DATA = {
#     "mars":      ("Red Coral",     "Tuesday",  "Ring", "Copper or Silver", "Ring finger"),
#     "venus":     ("Diamond",       "Friday",   "Ring", "Silver or Platinum", "Middle finger"),
#     "mercury":   ("Emerald",       "Wednesday","Ring", "Gold",              "Little finger"),
#     "moon":      ("Pearl",         "Monday",   "Ring", "Silver",            "Little finger"),
#     "sun":       ("Ruby",          "Sunday",   "Ring", "Gold or Copper",    "Ring finger"),
#     "jupiter":   ("Yellow Sapphire","Thursday","Ring", "Gold",              "Index finger"),
#     "saturn":    ("Blue Sapphire", "Saturday", "Ring", "Iron or Silver",    "Middle finger"),
#     "rahu":      ("Hessonite",     "Saturday", "Ring", "Silver",            "Middle finger"),
#     "ketu":      ("Cat's Eye",     "Tuesday",  "Ring", "Silver",            "Little finger"),
# }

# ZODIAC_SIGNS = [
#     "aries", "taurus", "gemini", "cancer", "leo", "virgo",
#     "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
# ]

# TRUSTED_SITES = [
#     {"name": "GemPundit", "url": "https://www.gempundit.com"},
#     {"name": "Gemstone Universe", "url": "https://www.gemstoneuniverse.com"},
#     {"name": "Khanna Gems", "url": "https://www.khannagems.com"},
# ]

# def calculate_jd(dob, tob, offset_hrs):
#     dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
#     utc_time = dt - timedelta(hours=offset_hrs)
#     jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_time.hour + utc_time.minute / 60)
#     return jd

# def get_sign(jd, planet):
#     planet_data = swe.calc_ut(jd, planet)  # Returns a tuple (longitude, latitude, distance, etc.)
#     longitude = planet_data[0][0]  # Extract the longitude value from the first element of the tuple
#     return ZODIAC_SIGNS[int(longitude // 30)]

# def moon_sign_to_planet_and_gem(sign):
#     sign = sign.lower()
#     mapping = {
#         "aries": ("Mars", "Red Coral"),
#         "taurus": ("Venus", "Diamond"),
#         "gemini": ("Mercury", "Emerald"),
#         "cancer": ("Moon", "Pearl"),
#         "leo": ("Sun", "Ruby"),
#         "virgo": ("Mercury", "Emerald"),
#         "libra": ("Venus", "Diamond"),
#         "scorpio": ("Mars", "Red Coral"),
#         "sagittarius": ("Jupiter", "Yellow Sapphire"),
#         "capricorn": ("Saturn", "Blue Sapphire"),
#         "aquarius": ("Saturn", "Blue Sapphire"),
#         "pisces": ("Jupiter", "Yellow Sapphire")
#     }
#     return mapping[sign]

# def gemstone_recommendation(dob, tob, pob="Delhi", weight_kg=None):
#     try:
#         offset = 5.5  # default IST
#         jd = calculate_jd(dob, tob, offset)

#         # Default location: Delhi (can integrate with geocoder later)
#         lat, lon = 28.6139, 77.2090
#         swe.set_topo(lon, lat, 0)

#         # Get Moon sign
#         moon_sign = get_sign(jd, swe.MOON)
#         moon_planet, moon_gem = moon_sign_to_planet_and_gem(moon_sign)

#         # Get Ascendant (Lagna)
#         asc_deg = swe.houses(jd, lat, lon)[1][0]
#         lagna_sign = ZODIAC_SIGNS[int(asc_deg // 30)]
#         lagna_planet, lagna_gem = moon_sign_to_planet_and_gem(lagna_sign)

#         # Mahadasha planet from nakshatra
#         moon_longitude = swe.calc_ut(jd, swe.MOON)[0][0]  # Extract longitude value
#         moon_deg = moon_longitude % 30
#         nak_index = int(moon_deg // (13 + 1/3))
#         dasha_planet = [
#             "ketu", "venus", "sun", "moon", "mars", "rahu",
#             "jupiter", "saturn", "mercury"
#         ][nak_index % 9]
#         dasha_instr = GEMSTONE_DATA[dasha_planet]

#         ratti = round(weight_kg * 2, 1) if weight_kg else "Not provided"
#         moon_instr = GEMSTONE_DATA[moon_planet.lower()]

#         return {
#             "moon_sign": moon_sign.capitalize(),
#             "lagna_sign": lagna_sign.capitalize(),
#             "moon_gem": moon_gem,
#             "lagna_gem": lagna_gem,
#             "moon_planet": moon_planet,
#             "lagna_planet": lagna_planet,
#             "ratti": f"{ratti} ratti" if isinstance(ratti, float) else "Not provided",
#             "wear_day": moon_instr[1],
#             "wear_metal": moon_instr[3],
#             "wear_finger": moon_instr[4],
#             "dasha_planet": dasha_planet.capitalize(),
#             "dasha_gem": dasha_instr[0],
#             "purchase_links": TRUSTED_SITES
#         }

#     except Exception as e:
#         return {"error": str(e)}