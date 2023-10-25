import json
from facebook_scraper import get_posts


def main():
    account_name = input("Enter the Facebook account username or ID: ")

    posts = get_posts(account_name)

    json_data = json.dumps(posts, indent=2)

    print(json_data)


if __name__ == "__main__":
    main()

