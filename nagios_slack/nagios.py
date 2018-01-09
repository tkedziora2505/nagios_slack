import pycurl
from io import BytesIO
from bs4 import BeautifulSoup

import time
import requests
import json
import pyglet

def get_page(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.USERPWD, '%s:%s' % ("tkedziora", "Kedziora02!@"))
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    file = buffer.getvalue()
    file = file.decode('utf-8')

    # print(file)
    return file


def get_alerts_data(file):
    # print(file)
    check_info = []
    search_data = BeautifulSoup(file, "html.parser")
    classList = ["statusBGCRITICAL", "statusBGCRITICALACK", "statusBGWARNING"]
    for row in search_data.find_all(class_=classList, text=True):
        # print(row)
        link = row.find_all('a')
        data = row.get_text().strip()
        # print(data)
        # print(len(data))
        # if len(data) > 1:
        #  in check_info:
        check_info.append(data)
        if len(link) == 1:
            link = str(link)
            link = link[10:]
            # start = link.find('"')
            end = link.rfind('"')
            link = link[:end].replace("amp;", '')
            nagios = "https://nagios.avantis.pl/nagios/cgi-bin/"
            check_info.append(nagios + link)
        # print(row.get_text())
        # print(len(check_info))
    return check_info


def display(check_info):
    print(check_info)


def get_alerts_crit(check_info):
    critical_alert_list = []
    x = 0
    ilosc_elementow = len(check_info)
    ilosc_checkow = ilosc_elementow / 6
    ilosc_checkow = int(ilosc_checkow)
    print("ilosc checkow = " + str(ilosc_checkow))
    for x in range(ilosc_checkow):
        date = check_info[x * 6 + 3]
        # print("wersja1= " + date)
        pos_h = date.rfind('h') + 1
        pos_m = date.rfind('m')
        pos_d = date.rfind('d') + 1
        minuts = date[pos_h:pos_m]
        minuts = int(minuts)
        hour = date[pos_d:pos_h - 1]
        hour = int(hour)
        # print("Minuty")
        # print(date)
        if (minuts > 7) or (hour > 0):
            y = x * 6
            z = x * 6 + 6
            for o in range(y, z):
                if o == y:
                    string = str(check_info[o]).upper()
                    print(string)
                    critical_alert_list.append(string)
                else:
                    critical_alert_list.append(check_info[o])
    return critical_alert_list


def send_to_slack(alerts_to_send):
    slack_url = "https://hooks.slack.com/services/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"
    payload = {
        'channel': '#nagios_alert_test',
        'username': 'Checki do wystawienia',
        'icon_emoji': ':boom: :collision:'
    }
    string = "\n ".join(alerts_to_send)
    payload['text'] = string
    response = requests.post(slack_url, data=json.dumps(payload))
    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))


# CURL
url = 'https://nagios.avantis.pl/nagios/cgi-bin/status.cgi?host=all&type=detail&hoststatustypes=3&serviceprops=10&servicestatustypes=28'
file = get_page(url)
if file is None:
    music = pyglet.resource.media('ringtones-technology-cell-ringtone-loop-26.wav')
    music.play()
    pyglet.app.run()		
# print(file)
# WYCIAGNIECIE DANYCH Z CURLA
check_info = get_alerts_data(file)
# WYSWIETL
display(check_info)

# WYCIAGANIE CHECKOW DO WYSLANIA
alerts_to_send = get_alerts_crit(check_info)
print(alerts_to_send)

# wWYSYLANIE
if (len(alerts_to_send) > 0):
    send_to_slack(alerts_to_send)
    music = pyglet.resource.media('ringtones-technology-cell-ringtone-loop-26.wav')
    music.play()
    pyglet.app.run()



