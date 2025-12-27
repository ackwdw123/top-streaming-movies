import os
import requests
from datetime import datetime
import json

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
REGION = "US"

# Provider → Icon filename mapping
PROVIDER_ICONS = {
    "Netflix": "netflix.png",
    "Hulu": "hulu.png",
    "Disney Plus": "disneyplus.png",
    "Disney+": "disneyplus.png",
    "Amazon Prime Video": "primevideo.png",

    # Apple family
    "Apple TV Plus": "appletv.png",
    "Apple TV+": "appletv.png",
    "Apple TV": "appletv.png",
    "Apple TV App": "appletv.png",
    "Apple TV Amazon Channel": "appletv.png",
    "Apple iTunes": "appletv.png",

    # Max family
    "Max": "max.png",
    "HBO Max": "max.png",

    # AMC family
    "AMC": "amc.png",
    "AMC+": "amc.png",
    "AMC Plus": "amc.png",
    "AMC Premiere": "amc.png",

    # Starz family
    "Starz": "starz.png",
    "Starz Play": "starz.png",
    "Starz Amazon Channel": "starz.png",
    "Starz Apple TV Channel": "starz.png",

    # Spectrum family
    "Spectrum": "spectrum.png",
    "Spectrum TV": "spectrum.png",
    "Spectrum On Demand": "spectrum.png",
}

def tmdb_get(path, params=None):
    if params is None:
        params = {}
    params["api_key"] = TMDB_API_KEY
    response = requests.get(f"{TMDB_BASE_URL}{path}", params=params)
    response.raise_for_status()
    return response.json()

def fetch_movie_providers(movie_id):
    data = tmdb_get(f"/movie/{movie_id}/watch/providers")
    results = data.get("results", {})
    us = results.get(REGION, {})

    flatrate = us.get("flatrate", []) or []
    buy = us.get("buy", []) or []
    rent = us.get("rent", []) or []

    providers = []

    for item in flatrate:
        providers.append(item.get("provider_name"))
    if not providers:
        for item in buy:
            providers.append(item.get("provider_name"))
    if not providers:
        for item in rent:
            providers.append(item.get("provider_name"))

    seen = set()
    unique = []
    for p in providers:
        if p and p not in seen:
            seen.add(p)
            unique.append(p)
    return unique

def fetch_trending_movies_us_only(limit=10):
    data = tmdb_get("/trending/movie/day")
    results = data.get("results", [])

    us_movies = []
    for item in results:
        movie_id = item.get("id")
        providers = fetch_movie_providers(movie_id)

        # Only include movies with at least one US provider
        if providers:
            us_movies.append(item)

        if len(us_movies) == limit:
            break

    return us_movies

def build_movie_record(item):
    movie_id = item.get("id")
    title = item.get("title") or item.get("original_title") or "Unknown Title"
    overview = item.get("overview") or ""
    vote = item.get("vote_average") or 0
    release_date = item.get("release_date") or ""
    poster_path = item.get("poster_path")
    poster_url = f"{IMAGE_BASE}{poster_path}" if poster_path else None
    tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}" if movie_id else None

    providers = fetch_movie_providers(movie_id) if movie_id else []

    return {
        "id": movie_id,
        "title": title,
        "overview": overview,
        "rating": round(vote, 1) if vote else None,
        "release_date": release_date,
        "poster_url": poster_url,
        "tmdb_url": tmdb_url,
        "providers": providers,
    }

def generate_movies_json(movies):
    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "TMDB",
        "region": REGION,
        "type": "movie",
        "movies": movies,
    }
    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def generate_movies_html(movies):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    rows = ""
    for idx, movie in enumerate(movies, start=1):
        providers = movie["providers"]

        provider_icons_html = ""
        for p in providers:
            icon = PROVIDER_ICONS.get(p)
            if icon:
                provider_icons_html += (
                    f"<img src='icons/{icon}' class='provider-icon' alt='{p}' />"
                )

        poster = (
            f"<img src='{movie['poster_url']}' "
            f"alt='Poster for {movie['title']}' "
            f"style='height:140px;border-radius:6px;'/>"
            if movie["poster_url"]
            else ""
        )
        rating = movie["rating"] if movie["rating"] is not None else "—"

        rows += f"""
        <tr>
          <td style="text-align:center; color:#999;">{idx}</td>

          <td style="display:flex; gap:16px; align-items:center;">
            {poster}
            <div>
              <div style="font-size:20px; font-weight:600;">{movie['title']}</div>

              <div style="font-size:14px; color:#aaa; margin-top:4px;">
                Release date: {movie['release_date'] or 'Unknown'}
              </div>

              <div style="font-size:15px; color:#bbb; margin-top:6px; max-width:600px; line-height:1.35;">
                {movie['overview'][:260] + ('…' if len(movie['overview']) > 260 else '')}
              </div>

              <div style="font-size:14px; color:#8fd3ff; margin-top:6px;">
                {provider_icons_html}
              </div>
            </div>
          </td>

          <td style="text-align:center; font-size:18px;">{rating}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Top Streaming Movies (TMDB)</title>

  <style>
    body {{
      margin: 0;
      padding: 24px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #05070a;
      color: #f5f5f5;
    }}
    h1 {{
      font-size: 32px;
      margin-bottom: 4px;
    }}
    .subtitle {{
      color: #aaa;
      font-size: 14px;
      margin-bottom: 20px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      padding: 12px 10px;
      border-bottom: 1px solid #222;
      vertical-align: top;
    }}
    th {{
      text-align: left;
      font-size: 14px;
      color: #ccc;
    }}
    .provider-icon {{
      height: 34px;
      margin-right: 10px;
      vertical-align: middle;
    }}
  </style>

</head>
<body>
  <h1>Top Streaming Movies</h1>
  <div class="subtitle">
    Auto‑updated from TMDB • Region: {REGION} • Last updated: {now}
  </div>

  <table>
    <thead>
      <tr>
        <th style="width:40px; text-align:center;">#</th>
        <th>Movie</th>
        <th style="width:80px; text-align:center;">Rating</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>

</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY environment variable is not set")

    trending = fetch_trending_movies_us_only(limit=10)
    movies = [build_movie_record(item) for item in trending]

    generate_movies_json(movies)
    generate_movies_html(movies)
    print("index.html and movies.json updated successfully.")

if __name__ == "__main__":
    main()
