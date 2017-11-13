"""Test file."""
import json
import pdb


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
            # pdb.set_trace()
            text_list = result[key].split()
            for word in text_list:
                if word.lower() == serach_word.lower():
                    count += 1
    return count


if __name__ == '__main__':
    data = json_to_list('example.json')
    count1 = wordcount(data, 'and')
    print(count1)
