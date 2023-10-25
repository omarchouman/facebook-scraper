import time
import re
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup


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

        reaction_count_element = post.select_one(".x1ja2u2z .xrbpyxo span span span.xt0b8zv.x1e558r4")
        if reaction_count_element:
            reaction_count = reaction_count_element.get_text(strip=True)
        else:
            reaction_count = "No reaction count available"

        image_element = post.select_one("img.x1ey2m1c")
        if image_element:
            image_link = image_element.get("src")
        else:
            image_link = "No image available"

        results.append({
            "text": post_text,
            "date": post_date,
            "reaction_count": reaction_count,
            "image_link": image_link
        })

    driver.quit()
    return results


def get_page_name_from_url(url):
    match = re.search(r'https://www\.facebook\.com/(?P<page_name>\w+)', url)
    if match:
        return match.group('page_name')
    else:
        return None


def get_page_name(user_input):
    if re.match(r'https://www\.facebook\.com/(\w+)', user_input):
        return get_page_name_from_url(user_input)
    else:
        return user_input