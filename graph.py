"""Test file."""
import json
import pdb
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.offline as offline


def json_to_list(filename):
    """Turn a json file into a python list."""
    data = json.load(open(filename))
    return data


def wordcount(data, search_word):
    """Return the number of times a word has been used."""
    count = 0
    for result in data:  # do something which each result from scrape
        for key in result:
            text_list = result[key].split()
            for word in text_list:
                if word.lower() == search_word.lower():
                    count += 1
    return count


def generate_chart_on_keyword(words, filename, count_function):
    """Make a bar chart based on given words."""
    yvalues = []
    data = json_to_list(filename)
    for word in words:
        yvalues.append(count_function(data, word))
    chart_data = [go.Bar(
        x=words,
        y=yvalues)]
    div = offline.plot(chart_data, auto_open=False, output_type='div')
    return div


def generate_chart_on_keyword_v2(words, counter, title):
    """Make a bar chart based on given words."""
    from TechLurker.searching import count_words as cw
    xvals = []
    yvalues = []
    for word in words:
        xvals.append(word)
        yvalues.append(counter.get(word))
    chart_data = [go.Bar(
        x=xvals,
        y=yvalues)]
    layout = go.Layout(
        title=title
    )
    fig = go.Figure(data=chart_data, layout=layout)
    div = offline.plot(fig, auto_open=False, output_type='div')
    return div


def generate_pie_chart_on_keyword(words, counter, title):
    """Make a bar chart based on given words."""
    from TechLurker.searching import count_words as cw
    xvals = []
    yvalues = []
    for word in words:
        xvals.append(word)
        yvalues.append(counter.get(word))
    chart_data = [go.Pie(
        labels=xvals,
        values=yvalues)]
    layout = go.Layout(
        title=title
    )
    fig = go.Figure(data=chart_data, layout=layout)
    div = offline.plot(fig, auto_open=False, output_type='div')
    return div


def dict_to_pie_chart_tag(dict, title):
    """Turn dictionary into chart based on kvp."""
    labels = []
    values = []
    for key in dict:
        labels.append(key)
        values.append(dict[key])
    trace = [go.Pie(labels=labels, values=values)]
    layout = go.Layout(
        title=title
    )
    fig = go.Figure(data=trace, layout=layout)
    url = offline.plot(fig, auto_open=False, output_type='div')
    return url


def get_job_locations(filename):
    """Get the number of jobs by country as a dictionary."""
    raw_data = json_to_list('python_jobs.json')
    countries = {}
    for job in raw_data:
        location = job['loc']
        country = location.split()[-1].lower()
        if country == 'usa' or country == 'states' or country == 'us':
            countries.setdefault('usa', 0)
            countries['usa'] += 1
        elif country == 'uk' or country == 'kingdom' or country == 'england':
            countries.setdefault('uk', 0)
            countries['uk'] += 1
        else:
            countries.setdefault(country, 0)
            countries[country] += 1
    return countries


def get_job_locations_from_db(loc_list):
    """Get the number of jobs by country as a dictionary."""
    countries = {}
    for loc in loc_list:
        country = loc.split()[-1].lower()
        if country == 'usa' or country == 'states' or country == 'us':
            countries.setdefault('usa', 0)
            countries['usa'] += 1
        elif country == 'uk' or country == 'kingdom' or country == 'england':
            countries.setdefault('uk', 0)
            countries['uk'] += 1
        else:
            countries.setdefault(country, 0)
            countries[country] += 1
    return countries


def get_job_types(filename):
    """Get the number of jobs by country as a dictionary."""
    raw_data = json_to_list('python_jobs.json')
    job_types = {}
    for job in raw_data:
        types = job['job_type']
        for item in types:
            job_types.setdefault(item, 0)
            job_types[item] += 1
    return job_types


def get_job_types_from_db(job_list):
    """Get the number of jobs by country as a dictionary."""
    job_types = {}
    for job in job_list:
        job_types.setdefault(job, 0)
        job_types[job] += 1
    return job_types


def dict_to_pie_chart_url(dict):
    """Turn dictionary into chart based on kvp."""
    labels = []
    values = []
    for key in dict:
        labels.append(key)
        values.append(dict[key])
    trace = go.Pie(labels=labels, values=values)
    url = py.plot([trace], auto_open=False)
    # pdb.set_trace()
    return url


languages = ['python', 'c', 'java', 'c++', 'c#', 'r', 'javascript', 'swift', 'kotlin', 'php']
security = ['malware', 'breach', 'hacking', 'phish', 'infection']
countries = []


def wordcount_for_reddit(data, search_word):
    """Return the number of times a word has been used."""
    count = 0
    index_counter = 0
    for result in data:  # do something which each result from scrape
        for key in result:
            stringed_list = str(result[key])
            text_list = stringed_list.split()
            for word in text_list:
                if search_word == 'Go':
                    if word == search_word:
                        count += 1
                elif len(search_word.split()) == 2:
                    try:
                        if text_list[index_counter + 1] is not None:
                            if(word + text_list[index_counter + 1]) == search_word:
                                count += 1
                    except IndexError:
                        return count
                elif word.lower() == search_word.lower():
                    count += 1
                index_counter += 1
    return count


class TopFive(object):
    """Class to hold the top ten reddit posts."""

    def __init__(self):
        """Init for top ten object."""
        self.container = [('title', -1), ('title', -1), ('title', -1), ('title', -1), ('title', -1), ('title', -1)]
        self.lowest = 4

    def add_new_post(self, post):
        """Check if a post has a higher score and add it if so."""
        if int(post.score) > self.container[self.lowest][1]:
            del self.container[self.lowest]
            self.container.append((post.title, int(post.score)))
        lowest = self.find_lowest_score()
        self.lowest = lowest

    def find_lowest_score(self):
        """Find the lowest scoring post."""
        lowest = 100000
        index = -1
        for idx, post in enumerate(self.container):
            if post[1] < lowest:
                lowest = post[1]
                index = idx
        return index


if __name__ == '__main__':
    data = json_to_list('example.json')
    count1 = wordcount(data, 'and')
    print(count1)
