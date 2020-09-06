import re
from typing import Optional

from bs4 import BeautifulSoup


# .find()
# .find_all()

# .parent - property
# .find_parent()

# .parents
# .find_parents()

# .find_next_sibling()
# .find_previous_sibling()


def get_copywriter(tag: BeautifulSoup) -> Optional[BeautifulSoup]:
    whois = tag.find("div", id="whois").text.strip()
    if "Copywriter" in whois:
        return tag
    return None


def get_salary(salary_row: str):
    pattern = r"\d{1,9}"
    # salary = re.findall(pattern, salary_row)
    salary = re.search(pattern, salary_row).group()
    return salary if salary is not None else "-"


def main():
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "lxml")

    # filter = {"data-set": "salary"}
    # row = soup.find_all("div", filter)
    # a = soup.find("div", text="Kate").find_parent(class_="row")
    # print(a)

    # persons = soup.find_all("div", class_="row")
    # copywriters = [person for person in persons if get_copywriter(person) is not None]
    # print([copywriter.text for copywriter in copywriters])

    salary = soup.find_all("div", {"data-set": "salary"})
    for i in salary:
        print(get_salary(i.text))
    print(salary)


if __name__ == "__main__":
    main()
