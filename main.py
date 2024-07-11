import requests
from bs4 import BeautifulSoup
from db.rq import *
import random
import threading
import queue

class CrawlerThread(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue

    def run(self):
        while True:
            try:
                site = self.work_queue.get(timeout=1)  # Wait for a website to crawl
                if site is None:
                      get_data(self.work_queue)

                try:
                    r = requests.get(site)
                    r.raise_for_status()  # Raise an HTTPError for bad responses
                    try:
                        soup = BeautifulSoup(r.content, 'html.parser')
                    except:
                        CrawlerDB().validaded_website(site, "", "", "")
                        continue

                    title = soup.find("title").text if soup.find("title") else ""

# Récupérer tous les textes des balises courantes
                    text_elements = soup.find_all(['p', 'div', 'span', 'li', 'blockquote'])
                    text = " ".join([element.get_text(separator=" ", strip=True) for element in text_elements]) if text_elements else ""

                    # Récupérer les métadonnées
                    meta = {meta.attrs.get("name"): meta.attrs.get("content") for meta in soup.find_all("meta") if meta.attrs.get("name")}

                    # Récupérer les en-têtes
                    headers = []
                    for header in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        headers.extend([h.get_text(strip=True) for h in soup.find_all(header)])


                    for link in soup.find_all("a"):
                        href = link.get("href")
                        if href and (href.startswith("https://") or href.startswith("http://")):
                            if not CrawlerDB().check_website(href) and not CrawlerDB().check_double_website(href):
                                CrawlerDB().register_website(link=href)
                                print(f"{site} | New website: {href}")

                    CrawlerDB().validaded_website(site, headers[:2147000000], text[:2147000000], meta)

                except requests.RequestException as e:
                    print(f"Error fetching {site}: {e}")
                    CrawlerDB().validaded_website(site, "No Title", "No Content", "No Meta")

                self.work_queue.task_done()  # Mark task as done

            except queue.Empty:
                continue

def get_data(work_queue):
    QUEUE = CrawlerDB().get_all_website() if CrawlerDB().get_all_website() else ['https://awakno.fr/']
    random.shuffle(QUEUE)
    
    for site in QUEUE:
        work_queue.put(site)

def startup(num_threads=20):
    work_queue = queue.Queue()
    
    # Start threads
    threads = []
    for i in range(num_threads):
        thread = CrawlerThread(work_queue)
        thread.start()
        threads.append(thread)

    get_data(work_queue)
    
    # Wait for all tasks to be done
    work_queue.join()

    # Stop threads
    for _ in range(num_threads):
        work_queue.put(None)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    startup()
