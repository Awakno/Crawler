from db.connexion import queue, already_rq
import re



class CrawlerDB:
    def register_website(self,link):
        check = self.check_website(link)
        if not check:
            queue.insert_one({"url": link})
        if check:
            if len(check) == 1 and "Queue" in check :
                return
            if len(check) == 1 and "Validaded" in check:
                return
            if len(check) == 2:
                queue.delete_one({"url": link})

    def validaded_website(self,link,h1,text,meta):
        queue.delete_one({"url": link})
        website = {"url": link,"h1": h1,"text": text,"meta": meta}
        already_rq.insert_one(website)

    def check_website(self,link):
        end = []
        if queue.find_one({"url": link}):
            end.append("Queue")
        if already_rq.find_one({"url": link}):
            end.append("Validaded")
        return end
    def get_all_website(self):
        site = []
        for url in queue.find({}):
            site.append(url.get('url'))
        return site
    def check_double_website(self,link):
        if queue.find_one({"url": link}):
            return True
        if already_rq.find_one({"url": link}):
            return True
        return False