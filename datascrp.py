import requests
from bs4 import BeautifulSoup
import dateparser
class Player(object):
    def __init__(self, player_id):
        self.url = "https://www.espncricinfo.com/ci/content/player/{0}.html".format(str(player_id))
        self.json_url = "http://core.espnuk.org/v2/sports/cricket/athletes/{0}".format(str(player_id))
        self.parsed_html = self.get_html()
        self.json = self.get_json()
        self.player_information = self._parse_player_information()
        self.cricinfo_id = str(player_id)
    def photo(self):
        return self.json["headshot"]["href"]
    def get_html(self):
        r = requests.get(self.url)
        if r.status_code == 404:
            raise PlayerNotFoundError
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup.find("div", class_="pnl490M")
    def get_json(self):
        r = requests.get(self.json_url)
        if r.status_code == 404:
            raise PlayerNotFoundError
        else:
            return r.json()
    def _parse_player_information(self):
        return self.parsed_html.find_all('p', class_='ciPlayerinformationtxt')
    def _name(self):
        return self.json['name']
    def _first_name(self):
        return self.json['firstName']
    def _middle_name(self):
        return self.json['middleName']
    def _last_name(self):
        return self.json['lastName']
    def _full_name(self):
        return self.json['fullName']
    def _date_of_birth(self):
        return self.json['dateOfBirth']
    def _current_age(self):
        return self.json['age']
    def _major_teams(self):
        return next((p.text.replace('Major teams ','').split(', ') for p in self.player_information if p.find('b').text == 'Major teams'), None)
    def _playing_role(self):
        return self.json['position']
    def _batting_style(self):
        return next((x for x in self.json['style'] if x['type'] == 'batting'), None)
    def _bowling_style(self):
        return next((x for x in self.json['style'] if x['type'] == 'bowling'), None)
    def _batting_fielding_averages(self):
        if len(self.parsed_html.findAll('table', class_='engineTable')) == 4:
            headers = ['matches', 'innings', 'not_out', 'runs', 'high_score', 'batting_average', 'balls_faced', 'strike_rate', 'centuries', 'fifties', 'fours', 'sixes', 'catches', 'stumpings']
            bat_field = [td.text.strip() for td in self.parsed_html.find('table', class_='engineTable').findAll('td')]
            num_formats = int(len(bat_field)/15)
            format_positions = [15*x for x in range(num_formats)]
            formats = [bat_field[x] for x in format_positions]
            avg_starts = [x+1 for x in format_positions[:num_formats]]
            avg_finish = [x+14 for x in avg_starts]
            format_averages = [bat_field[x:y] for x,y in zip(avg_starts, avg_finish)]
            combined = list(zip(formats, format_averages))
            l = [{x: dict(zip(headers, y))} for x,y in combined]
            return { k: v for d in l for k, v in d.items() }
        else:
            return None
    def _bowling_averages(self):
        if len(self.parsed_html.findAll('table', class_='engineTable')) == 4:
            headers = ['matches', 'innings', 'balls_delivered', 'runs', 'wickets', 'best_innings', 'best_match', 'bowling_average', 'economy', 'strike_rate', 'four_wickets', 'five_wickets', 'ten_wickets']
            bowling = [td.text.strip() for td in self.parsed_html.findAll('table', class_='engineTable')[1].findAll('td')]
            num_formats = int(len(bowling)/14)
            format_positions = [14*x for x in range(num_formats)]
            formats = [bowling[x] for x in format_positions]
            avg_starts = [x+1 for x in format_positions[:num_formats]]
            avg_finish = [x+13 for x in avg_starts]
            format_averages = [bowling[x:y] for x,y in zip(avg_starts, avg_finish)]
            combined = list(zip(formats, format_averages))
            l = [{x: dict(zip(headers, y))} for x,y in combined]
            return { k: v for d in l for k, v in d.items() }
        else:
            return None
    def _debuts_and_lasts(self):
        if len(self.parsed_html.findAll('table', class_='engineTable')) == 4:
            return self.parsed_html.findAll('table', class_='engineTable')[2]
        else:
            return None
    def _test_debut(self):
        if self._debuts_and_lasts() is not None:
            test_debut = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'Test debut'), None)
            if test_debut:
                title = test_debut.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None
    def _last_test(self):
        if self._debuts_and_lasts() is not None:
            last_test = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'Last Test'), None)
            if last_test:
                title = last_test.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None
    def _t20i_debut(self):
        if self._debuts_and_lasts() is not None:
            t20i_debut = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'T20I debut'), None)
            if t20i_debut:
                title = t20i_debut.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None
    def _last_t20i(self):
        if self._debuts_and_lasts() is not None:
            last_t20i = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'Last T20I'), None)
            if last_t20i:
                title = last_t20i.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None
    def _first_class_debut(self):
        if self._debuts_and_lasts() is not None:
            first_class_debut = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'First-class debut'), None)
            if first_class_debut:
                try:
                    title = first_class_debut.findAll('td')[1].text.replace(' scorecard','')
                    return title
                except:
                    return first_class_debut.findAll('td')[1].text
            else:
                return None
        else:
            return None
    def _last_first_class(self):
        if self._debuts_and_lasts() is not None:
            last_first_class = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'Last First-class'), None)
            if last_first_class:
                title = last_first_class.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        return None
    def _list_a_debut(self):
        if self._debuts_and_lasts() is not None:
            list_a_debut = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'List A debut'), None)
            if list_a_debut:
                try:
                    title = list_a_debut.findAll('td')[1].text.replace(' scorecard','')
                    return title
                except:
                    return list_a_debut.findAll('td')[1].text
            else:
                return None
        else:
            return None
    def _last_list_a(self):
        if self._debuts_and_lasts() is not None:
            last_list_a = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'Last List A'), None)
            if last_list_a:
                title = last_list_a.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None
    def _t20_debut(self):
        if self._debuts_and_lasts() is not None:
            t20_debut = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'T20s debut'), None)
            if t20_debut:
                title = t20_debut.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None
    def _last_t20(self):
        if self._debuts_and_lasts() is not None:
            last_t20 = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'Last T20s'), None)
            if last_t20:
                title = last_t20.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None
    def _odi_debut(self):
        if self._debuts_and_lasts() is not None:
            odi_debut = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'ODI debut'), None)
            if odi_debut:
                title = odi_debut.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None
    def _last_odi(self):
        if self._debuts_and_lasts() is not None:
            last_odi = next((tr for tr in self._debuts_and_lasts().findAll('tr') if tr.find('b').text == 'Last ODI'), None)
            if last_odi:
                title = last_odi.findAll('td')[1].text.replace(' scorecard','')
                return title
            else:
                return None
        else:
            return None    