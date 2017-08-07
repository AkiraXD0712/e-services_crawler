from bs4 import BeautifulSoup
import datetime
from log import logger


class Analyser:
    def __init__(self):
        logger.info("Start analyser")

    def analyze_absences(self, inner):
        logger.info("Analyzing absences")
        setattr(self.__class__, "soup", BeautifulSoup(inner, "lxml"))
        # print(soup.prettify())
        # setattr(self.__class__, "soup", BeautifulSoup(open("text.txt", "r", encoding="utf8"), "lxml"))
        # date_time_now = datetime.datetime.now()
        # logger.info("Current time: " + str(date_time_now))

        logger.debug("Filtering data")
        absences = self.soup.div.tbody.find_all("tr")
        for absence in absences:
            iter = absence.td
            date = iter.contents[1]
            date_time = datetime.datetime.strptime(date, '%d/%m/%y')
            # diff = (date_time_now - date_time).days
            if date_time.year >= 2017:
                print(iter.contents[0].string + ": " + str(date_time))
                iter = iter.next_sibling.next_sibling.next_sibling
                horaire = iter.contents[1]
                print(iter.contents[0].string + ": " + horaire)
                iter = iter.next_sibling
                if len(iter) == 1:
                    print(iter.contents[0].string + ": ")
                else:
                    cours = iter.contents[1]
                    print(iter.contents[0].string + ": " + cours)
                print("\n")

    def analyze_notes(self, inner):
        logger.info("Analyzing notes")
        setattr(self.__class__, "soup", BeautifulSoup(inner, "lxml"))
        # print(soup.prettify())
        # setattr(self.__class__, "soup", BeautifulSoup(open("note.txt", "r", encoding="utf8"), "lxml"))

        logger.debug("Filtering data")
        notes = self.soup.tbody.find_all("tr")
        for note in notes:
            iter = note.td
            date = iter.contents[1].string
            date_time = datetime.datetime.strptime(date[:-6], '%d/%m/%Y')
            if date_time.year >= 2017:
                for i in range(len(note)):
                    name = iter.contents[0].string
                    value = iter.contents[1].string
                    print(name + ": " + value)
                    iter = iter.next_sibling
                print("\n")

if __name__ == "__main__":
    analyser = Analyser()
    analyser.analyze_absences()