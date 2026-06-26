import pandas as pd
import random

def get_sydney_data():
    suburbs = [
        # Inner City
        {"suburb": "Surry Hills", "region": "Inner City", "median_price": 1250000, "median_weekly_rent": 850},
        {"suburb": "Newtown", "region": "Inner City", "median_price": 1180000, "median_weekly_rent": 820},
        {"suburb": "Glebe", "region": "Inner City", "median_price": 1320000, "median_weekly_rent": 870},
        {"suburb": "Redfern", "region": "Inner City", "median_price": 1100000, "median_weekly_rent": 800},
        {"suburb": "Pyrmont", "region": "Inner City", "median_price": 1050000, "median_weekly_rent": 790},

        # Inner West
        {"suburb": "Leichhardt", "region": "Inner West", "median_price": 1450000, "median_weekly_rent": 880},
        {"suburb": "Balmain", "region": "Inner West", "median_price": 1750000, "median_weekly_rent": 950},
        {"suburb": "Marrickville", "region": "Inner West", "median_price": 1350000, "median_weekly_rent": 860},
        {"suburb": "Ashfield", "region": "Inner West", "median_price": 1200000, "median_weekly_rent": 780},
        {"suburb": "Strathfield", "region": "Inner West", "median_price": 1650000, "median_weekly_rent": 900},

        # North Shore
        {"suburb": "Chatswood", "region": "North Shore", "median_price": 1850000, "median_weekly_rent": 980},
        {"suburb": "Lane Cove", "region": "North Shore", "median_price": 1950000, "median_weekly_rent": 990},
        {"suburb": "Mosman", "region": "North Shore", "median_price": 3200000, "median_weekly_rent": 1400},
        {"suburb": "Neutral Bay", "region": "North Shore", "median_price": 1600000, "median_weekly_rent": 950},
        {"suburb": "Kirribilli", "region": "North Shore", "median_price": 1750000, "median_weekly_rent": 970},

        # Eastern Suburbs
        {"suburb": "Bondi", "region": "Eastern Suburbs", "median_price": 2100000, "median_weekly_rent": 1050},
        {"suburb": "Coogee", "region": "Eastern Suburbs", "median_price": 1950000, "median_weekly_rent": 1020},
        {"suburb": "Randwick", "region": "Eastern Suburbs", "median_price": 1800000, "median_weekly_rent": 980},
        {"suburb": "Maroubra", "region": "Eastern Suburbs", "median_price": 1550000, "median_weekly_rent": 900},
        {"suburb": "Bronte", "region": "Eastern Suburbs", "median_price": 2300000, "median_weekly_rent": 1100},

        # Western Sydney
        {"suburb": "Parramatta", "region": "Western Sydney", "median_price": 850000, "median_weekly_rent": 650},
        {"suburb": "Blacktown", "region": "Western Sydney", "median_price": 780000, "median_weekly_rent": 580},
        {"suburb": "Penrith", "region": "Western Sydney", "median_price": 720000, "median_weekly_rent": 550},
        {"suburb": "Liverpool", "region": "Western Sydney", "median_price": 760000, "median_weekly_rent": 570},
        {"suburb": "Fairfield", "region": "Western Sydney", "median_price": 740000, "median_weekly_rent": 560},

        # South Sydney
        {"suburb": "Hurstville", "region": "South Sydney", "median_price": 1100000, "median_weekly_rent": 720},
        {"suburb": "Rockdale", "region": "South Sydney", "median_price": 980000, "median_weekly_rent": 680},
        {"suburb": "Kogarah", "region": "South Sydney", "median_price": 1050000, "median_weekly_rent": 700},
        {"suburb": "Miranda", "region": "South Sydney", "median_price": 1150000, "median_weekly_rent": 730},
        {"suburb": "Cronulla", "region": "South Sydney", "median_price": 1400000, "median_weekly_rent": 820},

        # Hills District
        {"suburb": "Castle Hill", "region": "Hills District", "median_price": 1550000, "median_weekly_rent": 800},
        {"suburb": "Baulkham Hills", "region": "Hills District", "median_price": 1450000, "median_weekly_rent": 780},
        {"suburb": "Kellyville", "region": "Hills District", "median_price": 1350000, "median_weekly_rent": 750},
        {"suburb": "Rouse Hill", "region": "Hills District", "median_price": 1250000, "median_weekly_rent": 730},
        {"suburb": "Norwest", "region": "Hills District", "median_price": 1300000, "median_weekly_rent": 740},

        # Northern Beaches
        {"suburb": "Manly", "region": "Northern Beaches", "median_price": 2400000, "median_weekly_rent": 1150},
        {"suburb": "Dee Why", "region": "Northern Beaches", "median_price": 1400000, "median_weekly_rent": 850},
        {"suburb": "Curl Curl", "region": "Northern Beaches", "median_price": 2100000, "median_weekly_rent": 1050},
        {"suburb": "Narrabeen", "region": "Northern Beaches", "median_price": 1800000, "median_weekly_rent": 950},
        {"suburb": "Mona Vale", "region": "Northern Beaches", "median_price": 1650000, "median_weekly_rent": 900},
    ]

    df = pd.DataFrame(suburbs)

    # Calculate rental yield
    df["annual_rent"] = df["median_weekly_rent"] * 52
    df["gross_yield_pct"] = (df["annual_rent"] / df["median_price"] * 100).round(2)

    # Yield category
    def yield_category(y):
        if y >= 4.0:
            return "High (4%+)"
        elif y >= 3.0:
            return "Medium (3-4%)"
        else:
            return "Low (<3%)"

    df["yield_category"] = df["gross_yield_pct"].apply(yield_category)

    # Affordability score (lower price = more affordable = higher score)
    max_price = df["median_price"].max()
    df["affordability_score"] = ((max_price - df["median_price"]) / max_price * 10).round(1)

    # Investment score = yield + affordability
    df["investment_score"] = ((df["gross_yield_pct"] * 0.6) + (df["affordability_score"] * 0.4)).round(2)

    return df