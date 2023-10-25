import re
import html
from datetime import datetime


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


def convert_facebook_date(date_str):
    try:
        date_str = html.unescape(date_str)
        date_str = re.sub(r'\xa0', ' ', date_str)

        match = re.search(r'(\d+ [a-zA-Z]+) at (\d+:\d+)', date_str)

        if match:
            day_month, time_str = match.groups()

            current_year = datetime.now().year

            date_object = datetime.strptime(f"{day_month} {current_year} {time_str}", "%d %B %Y %H:%M")

            formatted_date = date_object.strftime("%Y-%m-%d")

            return formatted_date
        else:
            raise ValueError("Date not found in the expected format")
    except Exception as e:
        print(f"Error converting Facebook date: {e}")
        return None
