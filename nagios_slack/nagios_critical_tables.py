def get_Page():
    import pycurl
    from io import BytesIO
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://nagios.avantis.pl/nagios/cgi-bin/status.cgi?host=all&servicestatustypes=28')
    c.setopt(pycurl.USERPWD, '%s:%s' % ("tkedziora", "Kedziora01!@"))
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
    check_info = []
    from bs4 import BeautifulSoup
    search_data = BeautifulSoup(file, 'html.parser')
    for row in search_data.find_all(class_="statusBGCRITICALACK"):
        data = row.get_text().strip()
        # print(data)
        # print(len(data))
        if len(data) > 1:
        #  in check_info:
            check_info.append(data)
        # print(row.get_text())
        # print(len(check_info))
    return check_info


def display(check_info):
        print(check_info)


# def get_alert_url(file):



file = get_Page()
check_info = get_alerts_data(file)
display(check_info)
print(len(check_info))
