import requests

def get_currency():
    """Получение курса доллара к EUR и RUB"""
    url = "https://open.er-api.com/v6/latest/USD"  # надёжное API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "rates" in data:
            print("📊 Курс доллара:")
            print(f"1 USD = {data['rates']['EUR']} EUR")
            print(f"1 USD = {data['rates']['RUB']} RUB")
        else:
            print("Нет данных о курсах:", data)
    else:
        print("Ошибка:", response.status_code)


def get_coordinates(city):
    """Получение координат города через Nominatim (OpenStreetMap)."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 3}  # до 3 совпадений
    response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        results = response.json()
        if results:
            best_match = results[0]
            return float(best_match["lat"]), float(best_match["lon"]), best_match["display_name"]
        else:
            return None, None, None
    else:
        return None, None, None


def get_weather(city):
    """Получение текущей погоды по названию города"""
    lat, lon, full_name = get_coordinates(city)
    if lat is None or lon is None:
        print("❌ Город не найден 😢 Попробуй уточнить, например: 'New York, USA'")
        return

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "current_weather" in data:
            weather = data["current_weather"]
            print(f"🌍 Погода в городе {full_name}:")
            print("Температура:", weather["temperature"], "°C")
            print("Скорость ветра:", weather["windspeed"], "км/ч")
        else:
            print("Нет данных о погоде:", data)
    else:
        print("Ошибка:", response.status_code)


# --- Главная программа ---
choice = input("Что показать (курс / погода)? ").strip().lower()

if choice == "курс":
    get_currency()
elif choice == "погода":
    city = input("Введите название города: ").strip()
    get_weather(city)
else:
    print("Неверный выбор. Попробуй ввести 'курс' или 'погода'.")
