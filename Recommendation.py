import requests

# Your API key
API_KEY = '5d0d9b6dc1d1f10d2a5d28a59b0576e5'
SEARCH_QUERY = 'Bollywood'
url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={SEARCH_QUERY}'

# Send a GET request to the TMDb API
response = requests.get(url)

# Check if the response was successful
if response.status_code == 200:
    data = response.json()

    # Check if there are any results
    if data['results']:
        print("Bollywood Movie Recommendations:")
        for movie in data['results']:
            # Print movie details
            print(f"Title: {movie['title']}")
            print(f"Release Date: {movie['release_date']}")
            print(f"Overview: {movie['overview']}\n")
    else:
        print("No movies found.")
else:
    print(f"Error: {response.status_code} - {response.text}")
