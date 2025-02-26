import requests
import pandas as pd
import time
from datetime import datetime

years = range(2020, 2025)  # 2020 to 2024
seasons = ['winter', 'spring', 'summer', 'fall']
anime_list = []
BASE_URL = "https://api.jikan.moe/v4/seasons"
for year in years:
    for season in seasons:
        try:
            url = f"{BASE_URL}/{year}/{season}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                for anime in data.get("data", []):
                    english_title = anime.get("title_english") or anime.get("title")
                    anime_list.append({
                        "Anime ID": anime.get("mal_id"),
                        "Title": english_title,
                        "Type": anime.get("type", "Unknown"),
                        "Score": anime.get("score", "N/A"),
                        "Popularity": anime.get("popularity", "N/A"),
                        "Members": anime.get("members", "N/A"),
                        "Genres": ", ".join([genre['name'] for genre in anime.get("genres", [])]),
                        "Studios": ", ".join([studio['name'] for studio in anime.get("studios", [])]),
                        "Year": year,
                        "Season": season,
                        "Updated_At": datetime.now().strftime("%Y-%m-%d")
                    })
                print(f"Fetched {len(data.get('data', []))} anime from {season} {year}")
            else:
                print(f"Failed to fetch data for {season} {year}. Status code: {response.status_code}")

            time.sleep(1.5)  

        except Exception as e:
            print(f"Error fetching data for {season} {year}: {e}")
anime_df = pd.DataFrame(anime_list)
anime_df.to_csv('anime_2020_2024.csv', index=False, encoding='utf-8')
print("Data saved to anime_2020_2024.csv")