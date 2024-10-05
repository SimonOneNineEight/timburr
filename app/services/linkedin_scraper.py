from bs4 import BeautifulSoup
import requests
import time as tm

keyword = "Software%2BIntern%2B2025"
location = "95112"

url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location=95112&geoId=104110784&trk=public_jobs_jobs-search-bar_search-submit&original_referer=https%3A%2F%2Fwww.linkedin.com%2Fjobs%2Fsearch%3Fkeywords%3D{keyword}&location%3DSan%2BJose%252C%2BCA%26geoId%3D104110784%26trk%3Dpublic_jobs_jobs-search-bar_search-submit&start=100"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_with_retry(retries=5, delay=3):
    for i in range(retries):
        try:
            r = requests.get(url, headers=headers, timeout=5)
            print(f"r.status_code:{r.status_code}")
            if r.status_code != requests.codes.ok:
                tm.sleep(delay)
                continue
            return BeautifulSoup(r.content, "html.parser")
        except requests.exceptions.Timeout:
            print(f"Timeout occurred for URL: {url}, retrying in {delay}sec...")
            tm.sleep(delay)
        except Exception as e:
            print(f"An error occurred while retrieving the URL: {url}, error: {e}")
    return None


def transform(soup):
    job_list = []
    try:
        divs = soup.find_all("div", class_="base-search-card__info")
    except:
        print("Empty page, no jobs found")
        return job_list

    for item in divs:
        title = item.find("h3").text.strip()
        company = item.find("a", class_="hidden-nested-link")
        location = item.find("span", class_="job-search-card__location")
        parent_div = item.parent
        entity_urn = parent_div["data-entity-urn"]
        job_posting_id = entity_urn.split(":")[-1]
        job_url = "https://www.linkedin.com/jobs/view/" + job_posting_id + "/"

        date_tag_new = item.find("time", class_="job-search-card__listdate--new")
        date_tag = item.find("time", class_="job-search-card__listdate")
        date = (
            date_tag["datetime"]
            if date_tag
            else date_tag_new["datetime"]
            if date_tag_new
            else ""
        )
        job_description = ""

        job = {
            "title": title,
            "company": company.text.strip().replace("\n", " ") if company else "",
            "location": location.text.strip() if location else "",
            "date": date,
            "job_url": job_url,
            "job_description": job_description,
            "applied": 0,
            "hidden": 0,
            "interview": 0,
            "rejected": 0,
        }

        job_list.append(job)

    return job_list


def main():
    soup = get_with_retry()
    if soup:
        job_list = transform(soup)
        for job in job_list:
            print(job)


# --------------------
if __name__ == "__main__":
    main()
