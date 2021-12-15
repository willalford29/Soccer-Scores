from tkinter import *
import threading
from time import *
import urllib
from bs4 import BeautifulSoup
import requests
from datetime import datetime

root = Tk()
root.geometry("420x200")
label1 = Label(root, text="Live Scores")
label1.place(x=10,y=10)

labelT = Label(root, text="Time: ")
labelT.place(x=190,y=10)

label = Label(root, text="Soccer")
label.place(x=10,y=30)

fTime = Label(root, text="Time")
fTime.place(x=10,y=50)

fHome = Label(root, text="")
fHome.place(x=10,y=70)

fAway = Label(root, text="")
fAway.place(x=10,y=90)

label2 = Label(root, text="Sport 2")
label2.place(x=150,y=30)

fTime2 = Label(root, text="Time")
fTime2.place(x=150,y=50)

fHome2 = Label(root, text="")
fHome2.place(x=150,y=70)

fAway2 = Label(root, text="")
fAway2.place(x=150,y=90)

label3 = Label(root, text="Sport 3")
label3.place(x=290,y=30)

fTime3 = Label(root, text="Time")
fTime3.place(x=290,y=50)

fHome3 = Label(root, text="")
fHome3.place(x=290,y=70)

fAway3 = Label(root, text="")
fAway3.place(x=290,y=90)

def refresh():
    global time
    for i in range(1000):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        labelT.configure(text="Time: "+str(current_time))
        fetchData(fTime, fHome, fAway, "https://www.goal.com/en/live-scores",
                  fTime2, fHome2, fAway2, fTime3, fHome3, fAway3)
        sleep(60)

def fetchData(timeR, teamH, teamA, url,
              timeR2, teamH2, teamA2,
              timeR3, teamH3, teamA3):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all("div")
    matchDivs = []
    for div in divs:
        if div.has_attr('class'):
            if div['class'][0] == 'match-row-list':
                divs2 = div.find_all("div")
                for div in divs2:
                    if div.has_attr('class'):
                        if div['class'][0] == 'match-row':
                            matchDivs.append(div)
    count = 0
    for div in matchDivs:
        divs = div.find_all("div")
        for div in divs:
            if div.has_attr('class'):
                if len(div.find_all("div")) == 0:
                    continue
                div2 = div.find_all("div")[0]
                data = ""
                # for div2 in divs2:
                span = div2.find_all("span")[0]
                data = span.get_text()
                    # print(span.get_text())
                table = div.find_all("table")[0]
                goalsH = table.find_all(class_="match-row__goals")[0].get_text()
                goalsA = table.find_all(class_="match-row__goals")[1].get_text()

                team1 = table.find_all(class_="match-row__team-name")[0].get_text()
                team2 = table.find_all(class_="match-row__team-name")[1].get_text()

                # print(data+" "+teamH+" "+str(goalsH)+" "+teamA+" "+str(goalsA))
                if "'" in data or data == "HT":
                    if count == 0:
                        timeR.configure(text="Time: "+data)
                        teamH.configure(text=team1+": "+goalsH)
                        teamA.configure(text=team2 + ": " + goalsA)
                        count+=1
                    elif count == 1:
                        timeR2.configure(text="Time: "+data)
                        teamH2.configure(text=team1+": "+goalsH)
                        teamA2.configure(text=team2 + ": " + goalsA)
                        count += 1
                    elif count == 2:
                        timeR3.configure(text="Time: "+data)
                        teamH3.configure(text=team1+": "+goalsH)
                        teamA3.configure(text=team2 + ": " + goalsA)
                        count += 1
                    else:
                        return



thr = threading.Thread(target=refresh)
thr.start()
root.mainloop()
