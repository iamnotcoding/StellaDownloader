import gdown
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import chromedriver_autoinstaller
import wget


def is_the_site(full_url, needle_url: str) -> bool:
    if full_url.find(needle_url) != -1:
        return True
    else:
        return False


def download_dl_link(url: str) -> bool:
    """Returns True if download succeeded. Otherwise False"""
    result = True

    try:
        wget.download(url)
    except Exception as e:
        print(e)
        result = False

    return result


def download_unkown_link(url: str) -> bool:
    """Returns True if download succeeded. Otherwise False"""
    result = False
    
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "html.parser")

    for a in soup.find_all("a"):
        try:
            link = a["href"]
        except Exception:
            continue

        print(link)
        # download_unkown = False means the search deapth is 1
        if download(link, False):
            result = True
            break

    return result


def download(url: str, download_unkown=True) -> bool:
    """Returns True if download succeeded. Otherwise False"""
    result = True

    if is_the_site(url, "drive.google.com"):  # google drive
        gdown.download(url, fuzzy=True)
    elif is_the_site(url, "drive"):  # google drive 'can't' scan virus page'
        # convert the ulr to normal google dirve again
        return download(
            f"https://drive.google.com/file/d/{url.split('id=')[1].split('&')[0]}/view?usp=sharing"
        )
    elif is_the_site(url, "dream-pro.info"):  # IR2IR
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, "html.parser")

        trs = soup.find_all("tr")

        for tr in trs:
            if (
                tr.find("th") is not None and tr.find("th").text.find("URL") != -1
            ):  # 本体URL
                return download(tr.find("td").find("a")["href"])
                break

        print("Couldn't find a download link in a IR2IR site : ", url)
        result = False
    elif is_the_site(url, "manbow"):  # manbow
        download_unkown_link(url)
    elif is_the_site(url, "dropbox"):  # dropbox
        if is_the_site(url, "www.dropbox.com/s/"):
            id = url.split("www.dropbox.com/s/")[1].split("/")[0]

            download_dl_link(f"https://www.dropbox.com/s/{id}?dl=1")
        elif is_the_site(url, "www.dropbox.com/scl/fi/"):
            id = url.split("www.dropbox.com/scl/fi/")[1].split("/")[0]
            key = url.split("rlkey=")[1].split("&")[0]

            download_dl_link(f"https://www.dropbox.com/scl/fi/{id}?rlkey={key}&dl=1")
        else:
            print("Unkown dropbox site url : ", url)
            result = False
    elif is_the_site(url, "anonymous.nekokan.dyndns.info"):  # anonymouseFTP
        return download_dl_link(url)
    else:
        # in order to prevent infinite loop
        if download_unkown:
            return download_dl_link(url)
        else:
            result = False

    return result


if __name__ == "__main__":
    import os
    
    os.chdir("./d")
    
    download(
        "https://manbow.nothing.sh/event/event.cgi?action=More_def&num=17&event=127"
    )
