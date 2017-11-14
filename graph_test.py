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


def wordcount(data, serach_word):
    """Return the number of times a word has been used."""
    count = 0
    for result in data:  # do something which each result from scrape
        for key in result:
            text_list = result[key].split()
            for word in text_list:
                if word.lower() == serach_word.lower():
                    count += 1
    return count


def generate_chart_on_keyword(words, filename):
    """Make a bar chart based on given words."""
    yvalues = []
    data = json_to_list(filename)
    for word in words:
        yvalues.append(wordcount(data, word))
    chart_data = [go.Bar(
        x=words,
        y=yvalues)]
    url = offline.plot(chart_data, auto_open=False)
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


def dict_to_pie_chart(dict):
    """Turn dictionary into chart based on kvp."""
    labels = []
    values = []
    for key in dict:
        labels.append(key)
        values.append(dict[key])
    trace = go.Pie(labels=labels, values=values)
    url = offline.plot([trace], auto_open=False)
    return url


if __name__ == '__main__':
    data = json_to_list('example.json')
    count1 = wordcount(data, 'and')
    print(count1)
