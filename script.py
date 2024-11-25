import requests
import re

# URL untuk mendapatkan aliran dan EPG
BASE_URLS = {
    "mana2": "https://www.mana2.my/live-tv",
    "tv3": "https://tonton.com.my/tv3-live-stream"
}
EPG_URL = "https://raw.githubusercontent.com/iptv-org/epg/master/streams/my.xml"

OUTPUT_FILE = "playlist.m3u"

def get_updated_url_mana2(channel_name):
    response = requests.get(BASE_URLS["mana2"])
    if response.status_code != 200:
        raise Exception(f"Failed to fetch mana2.my page: {response.status_code}")
    match = re.search(rf'https://live\.mana2\.my/{channel_name}/[^"]+', response.text)
    if not match:
        raise Exception(f"Stream URL for {channel_name} not found on mana2.my!")
    return match.group(0)

def get_updated_url_tv3():
    response = requests.get(BASE_URLS["tv3"])
    if response.status_code != 200:
        raise Exception(f"Failed to fetch TV3 page: {response.status_code}")
    match = re.search(r'https://tonton-live-switch-ssar\.akamaized\.net/stream-tv3/[^"]+', response.text)
    if not match:
        raise Exception("Stream URL for TV3 not found on tonton.com.my!")
    return match.group(0)

def update_playlist():
    channels = {
        "TV2": ("tv2.my", "https://example.com/logo-tv2.png", lambda: get_updated_url_mana2("Tv2")),
        "TV3": ("tv3.my", "https://example.com/logo-tv3.png", get_updated_url_tv3)
    }
    playlist = "#EXTM3U\n"
    playlist += f"#EXTINF:-1 tvg-url=\"{EPG_URL}\"\n"
    
    for name, (tvg_id, tvg_logo, fetch_url_func) in channels.items():
        try:
            url = fetch_url_func()
            playlist += f"#EXTINF:-1 tvg-id=\"{tvg_id}\" tvg-name=\"{name}\" tvg-logo=\"{tvg_logo}\" group-title=\"Malaysia\", {name}\n{url}\n"
        except Exception as e:
            print(f"Error updating {name}: {e}")
    
    # Simpan ke fail .m3u
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(playlist)
    print(f"Playlist updated: {OUTPUT_FILE}")

if __name__ == "__main__":
    update_playlist()
