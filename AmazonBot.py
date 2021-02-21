from bs4 import BeautifulSoup
from selenium import webdriver
import smtplib
from email.message import EmailMessage

driver = webdriver.Chrome(executable_path='C:\webdrivers\chromedriver.exe')

url = 'https://www.amazon.com'
driver.get(url)

def get_search(item_search):
    ''' Generates an URL that works for whatever item we are looking '''

    template_url = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
    item_search = item_search.replace(' ', '+')
    return template_url.format(item_search)

def get_items():
    ''' Returns all items from the first page'''

    soup = BeautifulSoup(driver.page_source, 'lxml')
    items = soup.find_all('div', {'data-component-type': 's-search-result'})
    item_description = {}
    urls = []

    for i in range(len(items)):
        try:
            item = items[i]
            price = item.find('span', 'a-offscreen').get_text().strip('$')
            title = item.h2.a.get_text().strip('\n')
            url = 'https://www.amazon.com/' + item.h2.a.get('href')

            item_description[title] = float(price), str(url) # Forms a dictionary

        except: # Skips the items that aren't real products.
            continue

    bycheapest = sorted(item_description.items(), key=lambda t:t[1])
    return bycheapest

'''
def display_items():
    Displays to console the items produced by get_items()

    print("These are the 5 cheapest items:")
    for i in get_items()[0:5]:
        print('- ', i)
'''

def get_email_content():
    ''' Build the message that will be sent to the email '''
    ''' The number of items that you get can be changed by
    changin both the range() functions. Currently it returns 10
    items, but you can decrease it or increase it'''

    titles = []
    urls = []
    prices = []

    for i in range(0, 10):
        urls.append(get_items()[i][1][1])
        titles.append(get_items()[i][0])
        prices.append(get_items()[i][1][0])

    message = 'Here are the links for the 10 cheapest items:\n\n'

    for i in range(0, 10):
        message += '- {} ${}\n'.format(titles[i],prices[i])
        message += urls[i]
        message += '\n\n'

    return message

def send_email():

    msg = EmailMessage()

    sender = 'ADD_YOUR_EMAIL_HERE'
    msg['From'] = sender
    pw = 'PASSWORD_FOR_EMAIL'
    msg['To'] = 'EMAIL_THAT_YOU_WANT_TO_SEND_DATA_TO'
    msg['Subject'] = 'AmazonBot'

    msg.set_content(get_email_content())

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, pw)
    server.send_message(msg)
    server.quit()
    print('\nEmail sent successfully.')


driver.get(get_search('WHAT_YOU_WANT_TO_LOOK_FOR'))
#display_items()
send_email()
