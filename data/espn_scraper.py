from bs4 import BeautifulSoup, Comment
import requests
import time
import csv


def get_soup(url):
    '''
    returns BeautifulSoup object of url
    '''
    source = requests.get(url).text
    return BeautifulSoup(source, 'html.parser')

def get_links(url):
    '''
    returns list of game links from pro-football-reference weekly scoreboard
    url_ex = 'https://www.pro-football-reference.com/years/2016/week_1.htm'
    '''
    links = []
    soup = get_soup(url)
    for i in soup.find_all('td', class_='right gamelink'):
        link = i.find(href=True)
        links.append('https://www.pro-football-reference.com' + link.get('href'))
    return links

def get_data(url):
    '''
    returns dictionary of data from single pro-football-reference game url
    url_ex = 'https://www.pro-football-reference.com/boxscores/201912290cin.htm'
    '''
    data = {}
    soup = get_soup(url)
    table = soup.find(id='all_game_info')
    comment = table.find(text=lambda text:isinstance(text, Comment))
    fresh_soup = BeautifulSoup(comment, 'html.parser')
    table_headers = [i.text for i in fresh_soup.find_all('th')]
    table_data = [i.text for i in fresh_soup.find_all('td')[1:]]
    for i in range(len(table_headers)):
        data[table_headers[i]] = table_data[i]
    return data

def main():
    # OPEN CSV
    csv_file = open('line_data.csv', 'w')
    fieldnames = ['Year', 'Week', 'Won Toss', 'Won OT Toss', 'Roof', 'Surface',
    'Duration', 'Attendance', 'Weather', 'Vegas Line', 'Over/Under', 'Link']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    years = range(2019, 2020)
    weeks = range(1, 18)

    for year in years:
        for week in weeks:
            game_counter = 1
            time.sleep(1)
            week_url = 'https://www.pro-football-reference.com/years/{}/week_{}.htm'.format(year, week)
            weekly_game_links = get_links(week_url)
            for game in weekly_game_links:
                time.sleep(1)
                game_data = get_data(game)
                game_data['Year'] = year
                game_data['Week'] = week
                game_data['Link'] = game
                writer.writerow(game_data)
                print('{} - {} - {}'.format(year, week, game_counter))
                game_counter += 1

    csv_file.close()

main()
# get_data('https://www.pro-football-reference.com/boxscores/201509130ram.htm')
