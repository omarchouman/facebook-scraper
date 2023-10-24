import time
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

    url = f"https://www.facebook.com/{account}"

    driver.get(url)

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.find_all("div", class_="x1iorvi4 x1pi30zi x1l90r2v x1swvt13")

    results = []

    for post in posts:
        post_text_element = post.select_one(".x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h")
        if post_text_element:
            post_text = post_text_element.get_text(strip=True)
        else:
            post_text = "No text available"

        post_date = post.find("span", class_="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb hrzyx87i")

        if post_date:
            post_date = post_date.get_text(strip=True)
        else:
            post_date = "No date available"

        results.append({"text": post_text, "date": post_date})

    driver.quit()
    return results


if __name__ == "__main__":
    account_name = input("Enter the Facebook account username or ID: ")

    posts = get_posts(account_name)

    for post in posts:
        print("Post Text:", post["text"])
        print("Post Date:", post["date"])
        print("\n")
