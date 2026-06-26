import pandas as pd
import os

# Postcode to suburb mapping for Greater Sydney
POSTCODE_SUBURB_MAP = {
    2000: ("Sydney CBD", "City & Inner South"),
    2007: ("Ultimo", "City & Inner South"),
    2008: ("Chippendale", "City & Inner South"),
    2009: ("Pyrmont", "City & Inner South"),
    2010: ("Surry Hills", "City & Inner South"),
    2011: ("Rushcutters Bay", "Eastern Suburbs"),
    2015: ("Eveleigh", "City & Inner South"),
    2016: ("Redfern", "City & Inner South"),
    2017: ("Waterloo", "City & Inner South"),
    2018: ("Mascot", "City & Inner South"),
    2019: ("Botany", "City & Inner South"),
    2020: ("Mascot", "City & Inner South"),
    2021: ("Paddington", "Eastern Suburbs"),
    2022: ("Bondi Junction", "Eastern Suburbs"),
    2023: ("Bellevue Hill", "Eastern Suburbs"),
    2024: ("Vaucluse", "Eastern Suburbs"),
    2025: ("Double Bay", "Eastern Suburbs"),
    2026: ("Bondi", "Eastern Suburbs"),
    2027: ("Darling Point", "Eastern Suburbs"),
    2028: ("Rose Bay", "Eastern Suburbs"),
    2029: ("Edgecliff", "Eastern Suburbs"),
    2030: ("Vaucluse", "Eastern Suburbs"),
    2031: ("Coogee", "Eastern Suburbs"),
    2032: ("Kingsford", "Eastern Suburbs"),
    2033: ("Randwick", "Eastern Suburbs"),
    2034: ("Clovelly", "Eastern Suburbs"),
    2035: ("Maroubra", "Eastern Suburbs"),
    2036: ("Matraville", "Eastern Suburbs"),
    2037: ("Glebe", "Inner West"),
    2038: ("Annandale", "Inner West"),
    2039: ("Rozelle", "Inner West"),
    2040: ("Leichhardt", "Inner West"),
    2041: ("Balmain", "Inner West"),
    2042: ("Newtown", "Inner West"),
    2043: ("Erskineville", "Inner West"),
    2044: ("St Peters", "Inner West"),
    2045: ("Haberfield", "Inner West"),
    2046: ("Drummoyne", "Inner West"),
    2047: ("Abbotsford", "Inner West"),
    2048: ("Stanmore", "Inner West"),
    2049: ("Petersham", "Inner West"),
    2050: ("Camperdown", "Inner West"),
    2060: ("Lavender Bay", "North Shore"),
    2061: ("Kirribilli", "North Shore"),
    2062: ("Cammeray", "North Shore"),
    2063: ("Northbridge", "North Shore"),
    2064: ("Artarmon", "North Shore"),
    2065: ("St Leonards", "North Shore"),
    2066: ("Lane Cove", "North Shore"),
    2067: ("Chatswood", "North Shore"),
    2068: ("Willoughby", "North Shore"),
    2069: ("Roseville", "North Shore"),
    2070: ("Lindfield", "North Shore"),
    2071: ("Killara", "North Shore"),
    2072: ("Gordon", "North Shore"),
    2073: ("Pymble", "North Shore"),
    2074: ("Turramurra", "North Shore"),
    2075: ("St Ives", "North Shore"),
    2076: ("Wahroonga", "North Shore"),
    2077: ("Hornsby", "North Shore"),
    2079: ("Mount Colah", "North Shore"),
    2085: ("Seaforth", "Northern Beaches"),
    2086: ("Frenchs Forest", "Northern Beaches"),
    2087: ("Forestville", "Northern Beaches"),
    2088: ("Mosman", "North Shore"),
    2089: ("Neutral Bay", "North Shore"),
    2090: ("Cremorne", "North Shore"),
    2092: ("Queenscliff", "Northern Beaches"),
    2093: ("Curl Curl", "Northern Beaches"),
    2094: ("Brookvale", "Northern Beaches"),
    2095: ("Manly", "Northern Beaches"),
    2096: ("Freshwater", "Northern Beaches"),
    2097: ("Narraweena", "Northern Beaches"),
    2099: ("Collaroy", "Northern Beaches"),
    2100: ("Narrabeen", "Northern Beaches"),
    2101: ("Mona Vale", "Northern Beaches"),
    2102: ("Warriewood", "Northern Beaches"),
    2103: ("Church Point", "Northern Beaches"),
    2106: ("Newport", "Northern Beaches"),
    2107: ("Avalon", "Northern Beaches"),
    2108: ("Palm Beach", "Northern Beaches"),
    2110: ("Drummoyne", "Inner West"),
    2111: ("Ryde", "Northern Sydney"),
    2112: ("Meadowbank", "Northern Sydney"),
    2113: ("Putney", "Northern Sydney"),
    2114: ("Eastwood", "Northern Sydney"),
    2115: ("Epping", "Northern Sydney"),
    2116: ("Burwood", "Inner West"),
    2117: ("Ermington", "Northern Sydney"),
    2118: ("Carlingford", "Northern Sydney"),
    2119: ("Beecroft", "Northern Sydney"),
    2120: ("Thornleigh", "Northern Sydney"),
    2121: ("Pennant Hills", "Northern Sydney"),
    2122: ("Eastwood", "Northern Sydney"),
    2125: ("West Pennant Hills", "Hills District"),
    2126: ("Cherrybrook", "Hills District"),
    2127: ("Newington", "Northern Sydney"),
    2130: ("Summer Hill", "Inner West"),
    2131: ("Croydon", "Inner West"),
    2132: ("Burwood", "Inner West"),
    2133: ("Homebush", "Inner West"),
    2134: ("Strathfield", "Inner West"),
    2135: ("Flemington", "Inner West"),
    2136: ("Flemington", "Inner West"),
    2137: ("Concord", "Inner West"),
    2138: ("Rhodes", "Inner West"),
    2140: ("Homebush", "Inner West"),
    2141: ("Lidcombe", "Western Sydney"),
    2142: ("Granville", "Western Sydney"),
    2143: ("Fairfield", "Western Sydney"),
    2144: ("Auburn", "Western Sydney"),
    2145: ("Westmead", "Western Sydney"),
    2146: ("Toongabbie", "Western Sydney"),
    2147: ("Lalor Park", "Western Sydney"),
    2148: ("Blacktown", "Western Sydney"),
    2150: ("Parramatta", "Western Sydney"),
    2151: ("North Rocks", "Western Sydney"),
    2152: ("Northmead", "Western Sydney"),
    2153: ("Baulkham Hills", "Hills District"),
    2154: ("Castle Hill", "Hills District"),
    2155: ("Rouse Hill", "Hills District"),
    2156: ("Annangrove", "Hills District"),
    2158: ("Kenthurst", "Hills District"),
    2159: ("Galston", "Hills District"),
    2160: ("Merrylands", "Western Sydney"),
    2161: ("Guildford", "Western Sydney"),
    2162: ("Sefton", "Western Sydney"),
    2163: ("Yagoona", "Western Sydney"),
    2164: ("Smithfield", "Western Sydney"),
    2165: ("Cabramatta", "Western Sydney"),
    2166: ("Canley Vale", "Western Sydney"),
    2167: ("Casula", "South Western Sydney"),
    2168: ("Moorebank", "South Western Sydney"),
    2170: ("Liverpool", "South Western Sydney"),
    2171: ("Lurnea", "South Western Sydney"),
    2173: ("Hammondville", "South Western Sydney"),
    2174: ("Holsworthy", "South Western Sydney"),
    2176: ("Wetherill Park", "Western Sydney"),
    2177: ("Bossley Park", "Western Sydney"),
    2179: ("Luddenham", "Western Sydney"),
    2190: ("Marrickville", "Inner West"),
    2191: ("Dulwich Hill", "Inner West"),
    2192: ("Earlwood", "Inner West"),
    2193: ("Canterbury", "Inner West"),
    2194: ("Campsie", "Inner West"),
    2195: ("Lakemba", "Inner West"),
    2196: ("Wiley Park", "Inner West"),
    2197: ("Bass Hill", "South Western Sydney"),
    2198: ("Yagoona", "Western Sydney"),
    2199: ("Bankstown", "South Western Sydney"),
    2200: ("Bankstown", "South Western Sydney"),
    2203: ("Dulwich Hill", "Inner West"),
    2204: ("Marrickville", "Inner West"),
    2205: ("Arncliffe", "South Sydney"),
    2206: ("Bexley", "South Sydney"),
    2207: ("Hurstville", "South Sydney"),
    2208: ("Kingsgrove", "South Sydney"),
    2209: ("Beverly Hills", "South Sydney"),
    2210: ("Riverwood", "South Sydney"),
    2211: ("Padstow", "South Sydney"),
    2212: ("Revesby", "South Sydney"),
    2213: ("Panania", "South Sydney"),
    2214: ("Peakhurst", "South Sydney"),
    2216: ("Rockdale", "South Sydney"),
    2217: ("Brighton-Le-Sands", "South Sydney"),
    2218: ("Kogarah", "South Sydney"),
    2219: ("Ramsgate", "South Sydney"),
    2220: ("Hurstville", "South Sydney"),
    2221: ("Blakehurst", "South Sydney"),
    2222: ("Penshurst", "South Sydney"),
    2223: ("Mortdale", "South Sydney"),
    2224: ("Sylvania", "South Sydney"),
    2225: ("Gymea", "South Sydney"),
    2226: ("Caringbah", "South Sydney"),
    2227: ("Miranda", "South Sydney"),
    2228: ("Kirrawee", "South Sydney"),
    2229: ("Cronulla", "South Sydney"),
    2230: ("Bundeena", "South Sydney"),
    2232: ("Sutherland", "South Sydney"),
    2233: ("Engadine", "South Sydney"),
    2234: ("Menai", "South Sydney"),
    2250: ("Gosford", "Central Coast"),
}

def get_sydney_data():
    # File paths — works both locally and on Streamlit Cloud
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rent_path = os.path.join(base_dir, "data", "rent-tables-march-2026-quarter.xlsx")
    sales_path = os.path.join(base_dir, "data", "sales-tables-december-2025-quarter.xlsx")

    # Load rent data
    rent_df = pd.read_excel(rent_path, sheet_name='Postcode', skiprows=8)
    rent_df.columns = ['Postcode','Dwelling_Type','Bedrooms','Q1_Rent','Median_Rent',
                       'Q3_Rent','New_Bonds','Total_Bonds','Qtly_Rent_Change',
                       'Annual_Rent_Change','Qtly_Bonds_Change','Annual_Bonds_Change']
    rent_df = rent_df[(rent_df['Dwelling_Type']=='Total') & (rent_df['Bedrooms']=='Total')].copy()
    rent_df['Postcode'] = pd.to_numeric(rent_df['Postcode'], errors='coerce')
    rent_df['Median_Rent'] = pd.to_numeric(rent_df['Median_Rent'], errors='coerce')
    rent_df = rent_df.dropna(subset=['Postcode','Median_Rent'])

    # Load sales data
    sales_df = pd.read_excel(sales_path, sheet_name='Postcode', skiprows=6)
    sales_df.columns = ['Postcode','Dwelling_Type','Q1_Price','Median_Price','Q3_Price',
                        'Mean_Price','Sales_Count','Qtly_Price_Change','Annual_Price_Change',
                        'Qtly_Count_Change','Annual_Count_Change']
    sales_df = sales_df[sales_df['Dwelling_Type']=='Total'].copy()
    sales_df['Postcode'] = pd.to_numeric(sales_df['Postcode'], errors='coerce')
    sales_df['Median_Price'] = pd.to_numeric(sales_df['Median_Price'], errors='coerce')
    sales_df = sales_df.dropna(subset=['Postcode','Median_Price'])

    # Filter Greater Sydney
    rent_sydney = rent_df[(rent_df['Postcode'] >= 2000) & (rent_df['Postcode'] <= 2250)]
    sales_sydney = sales_df[(sales_df['Postcode'] >= 2000) & (sales_df['Postcode'] <= 2250)]

    # Merge
    merged = pd.merge(
        rent_sydney[['Postcode','Median_Rent','Annual_Rent_Change']],
        sales_sydney[['Postcode','Median_Price','Annual_Price_Change']],
        on='Postcode'
    )

    # Sales prices are in $'000s — convert to actual dollars
    merged['median_price'] = merged['Median_Price'] * 1000
    merged['median_weekly_rent'] = merged['Median_Rent']

    # Add suburb and region names
    merged['suburb'] = merged['Postcode'].apply(
        lambda x: POSTCODE_SUBURB_MAP.get(int(x), (f"Postcode {int(x)}", "Other"))[0]
    )
    merged['region'] = merged['Postcode'].apply(
        lambda x: POSTCODE_SUBURB_MAP.get(int(x), (f"Postcode {int(x)}", "Other"))[1]
    )

    # Calculate yield
    merged['annual_rent'] = merged['median_weekly_rent'] * 52
    merged['gross_yield_pct'] = (merged['annual_rent'] / merged['median_price'] * 100).round(2)

    # Yield category
    def yield_category(y):
        if y >= 5.0:
            return "High (5%+)"
        elif y >= 4.0:
            return "Good (4-5%)"
        elif y >= 3.0:
            return "Medium (3-4%)"
        else:
            return "Low (<3%)"

    merged['yield_category'] = merged['gross_yield_pct'].apply(yield_category)

    # Affordability score
    max_price = merged['median_price'].max()
    merged['affordability_score'] = ((max_price - merged['median_price']) / max_price * 10).round(1)

    # Investment score
    merged['investment_score'] = ((merged['gross_yield_pct'] * 0.6) + (merged['affordability_score'] * 0.4)).round(2)

    # Rename for display
    merged = merged.rename(columns={'Postcode': 'postcode'})

    return merged[['postcode','suburb','region','median_price','median_weekly_rent',
                   'gross_yield_pct','yield_category','affordability_score',
                   'investment_score','annual_rent']]
