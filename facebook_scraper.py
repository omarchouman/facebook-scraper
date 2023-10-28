import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from helpers import get_page_name, convert_facebook_date
from datetime import datetime, timedelta


def get_posts(account: str, limit: int = 5):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    page_name = get_page_name(account)

    if not page_name:
        print("Invalid input. Please enter a valid Facebook URL or username/ID.")
        return []

    url = f"https://www.facebook.com/{page_name}"

    driver.get(url)

    time.sleep(3)

    try:
        close_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Close']")
        close_button.click()
        time.sleep(1)
    except Exception as e:
        print("Close button not found or not clickable:", str(e))

    results = []

    while len(results) < limit:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        posts = soup.find_all("div", class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")

        for post in posts:
            if len(results) >= limit:
                break

            post_link_element = post.find("a", class_="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lliihq x1pdlv7q")
            if post_link_element:
                href_value = post_link_element.get("href")
                match = re.search(r"fbid=(\d+)", href_value)
                post_id = match.group(1) if match else "No post ID available"
            else:
                post_id = "No post ID available"

            post_text_element = post.select_one(".x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h")
            if post_text_element:
                post_text = post_text_element.get_text(strip=True)
            else:
                post_text = "No text available"

            # post_date_element = post.select_one(".x1iyjqo2 span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.xo1l8bm.xi81zsa.x1yc453h")
            # if post_date_element:
            #     post_date = post_date_element.get_text(strip=True)
            # else:
            #     post_date = "No date available"

            post_date_element = post.select_one(
                ".x1iyjqo2 span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.xo1l8bm.xi81zsa.x1yc453h")
            if post_date_element:
                post_date = parse_facebook_date(post_date_element.get_text(strip=True))
            else:
                post_date = "No date available"

            reaction_count_element = post.select_one('.xrbpyxo span.x1e558r4')
            if reaction_count_element:
                reaction_count = reaction_count_element.text
            else:
                reaction_count = "No reaction count available"

            image_element = post.select_one("img.x1ey2m1c")
            if image_element:
                image_link = image_element.get("src")
            else:
                image_link = "No image available"

            results.append({
                "post_id": post_id,
                "text": post_text,
                "date": post_date,
                "reaction_count": reaction_count,
                "image_link": image_link
            })

    driver.quit()
    return results


def convert_relative_time(relative_time):
    current_time = datetime.now()

    if 's' in relative_time:
        seconds_ago = int(relative_time.split(' ')[0])
        return current_time - timedelta(seconds=seconds_ago)
    elif 'm' in relative_time:
        minutes_ago = int(relative_time.split(' ')[0])
        return current_time - timedelta(minutes=minutes_ago)
    elif 'h' in relative_time:
        hours_ago = int(relative_time.split(' ')[0])
        return current_time - timedelta(hours=hours_ago)
    elif 'd' in relative_time:
        days_ago = int(relative_time.split(' ')[0])
        return current_time - timedelta(days=days_ago)
    else:
        return None


def parse_facebook_date(date_str):
    # Check if the date contains a duration
    if 'ago' in date_str:
        relative_time_match = re.search(r'(\d+)\s\w', date_str)
        if relative_time_match:
            relative_time = relative_time_match.group(1)
            absolute_time = convert_relative_time(relative_time)
            return absolute_time.strftime("%Y-%m-%d %H:%M:%S") if absolute_time else "Invalid date"
        else:
            return "Invalid date"

    # Try to extract the date in "day month at time" format
    absolute_date_match = re.search(r'(\d{1,2} \w+ at \d{1,2}:\d{2})', date_str)
    if absolute_date_match:
        return absolute_date_match.group(1)

    # Try to extract the date in "day month" format
    absolute_date_match = re.search(r'(\d{1,2} \w+)', date_str)
    if absolute_date_match:
        return absolute_date_match.group(1)

    return "Invalid date"