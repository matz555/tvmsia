from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_streaming_url():
    # Inisialisasi WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Untuk menjalankan tanpa membuka pelayar
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    try:
        # Buka laman web
        url = "https://www.tvmy.online/2021/12/tv3.html"
        driver.get(url)
        time.sleep(5)  # Tunggu laman web dimuatkan sepenuhnya

        # Cari butang "Play" berdasarkan kelas dan klik
        play_button = driver.find_element(By.CLASS_NAME, "player-poster")
        ActionChains(driver).move_to_element(play_button).click().perform()
        time.sleep(5)  # Tunggu video dimuatkan

        # Cari URL aliran `.m3u8` dalam network traffic
        logs = driver.get_log("performance")
        for log in logs:
            if ".m3u8" in log["message"]:
                if 'master' in log["message"]:  # Cari master playlist
                    start = log["message"].find("https")
                    end = log["message"].find(".m3u8") + 5
                    return log["message"][start:end]

        return None

    finally:
        driver.quit()

stream_url = get_streaming_url()
if stream_url:
    print(f"Streaming URL: {stream_url}")
else:
    print("Failed to retrieve streaming URL.")
