import requests
import re

# URL laman web dengan senarai saluran
BASE_URL = "https://www.mana2.my/live-tv"
OUTPUT_FILE = "playlist.m3u"

def get_updated_url(channel_name):
    # Memuat laman web
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")
    
    # Cari URL aliran dengan token
    match = re.search(rf'https://live\.mana2\.my/{channel_name}/[^"]+', response.text)
    if not match:
        raise Exception(f"Stream URL for {channel_name} not found!")
    
    return match.group(0)

def update_playlist():
    channels = {
        "TV2": "Tv2",  # Tambah saluran lain jika perlu
    }
    playlist = "#EXTM3U\n"
    
    for name, slug in channels.items():
        try:
            url = get_updated_url(slug)
            playlist += f"#EXTINF:-1, {name}\n{url}\n"
        except Exception as e:
            print(f"Error updating {name}: {e}")
    
    # Simpan ke fail .m3u
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(playlist)
    print(f"Playlist updated: {OUTPUT_FILE}")

if __name__ == "__main__":
    update_playlist()
