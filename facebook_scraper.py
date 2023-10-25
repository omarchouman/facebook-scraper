import re
import time
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from helpers import get_page_name, convert_facebook_date


def get_posts(account: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
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

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.find_all("div", class_="x78zum5 xdt5ytf")

    results = []

    for post in posts:
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

        post_date_element = post.select_one(".x1iyjqo2 span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.xo1l8bm.xi81zsa.x1yc453h")
        if post_date_element:
            post_date = post_date_element.get_text(strip=True)
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
            "date": convert_facebook_date(post_date),
            "reaction_count": int(reaction_count),
            "image_link": image_link
        })

    driver.quit()
    return results