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


# def make_graph_data(data):
#     """Generate x and y coordinates based on JSON object."""
#


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


def generate_chart(words, filename):
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


if __name__ == '__main__':
    data = json_to_list('example.json')
    count1 = wordcount(data, 'and')
    print(count1)
