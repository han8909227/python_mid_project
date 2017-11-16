import contextlib
import mock
import pytest


"""Searching module test."""
def test_count_words_word_found():
    """Function should return number of times given word in text."""
    from TechLurker.searching import count_words
    sentance = "The test is a test to test the word test"
    counts = count_words(sentance)
    assert counts.get('test') == 4


def test_count_words_with_numbers():
    """Can this function find numbers too?."""
    from TechLurker.searching import count_words
    sentance = "The number of the day is 4"
    counts = count_words(sentance)
    assert counts.get('4') == 1


def test_parse_job_titles():
    """Test parses db data properly."""
    from TechLurker.searching import parse_job_titles
    data = '{"Back end","Front end",Web,"Developer / Engineer"}'
    result = parse_job_titles(data)
    assert result == ['Back end', 'Front end', 'Web', 'Developer / Engineer']


"""Graph module tests."""
def test_chart_on_keyword_returns_chart():
    """Test that html is generated for the chart."""
    from graph import generate_chart_on_keyword_v2
    from TechLurker.searching import count_words
    text = 'a b c d e f g h'
    word_count = count_words(text)
    data = ['a', 'b', 'c']
    results = generate_chart_on_keyword_v2(data, word_count)
    assert '<div>' in results


def test_chart_on_keyword_returns_type_error_if_no_data():
    """Test a type error returned if missing data."""
    from graph import generate_chart_on_keyword_v2
    from TechLurker.searching import count_words
    with pytest.raises(TypeError):
        generate_chart_on_keyword_v2(count_words)


def test_get_job_locations_from_db(dummy_request):
    """Test that job locations are collected from data."""
    from graph import get_job_locations_from_db
    loc_list = ['USA']
    new_lock = PyjobData(
        title='test_title',
        descrip='test description',
        loc='Seattle, WA, USA',
        job_type='backend',
        url='randome.com'
    )
    dummy_request.dbsession.add(new_lock)
    dummy_request.dbsession.commit()
    assert 'usa' in get_job_locations_from_db(loc_list)


def test_get_job_type_from_db(dummy_request):
    """Test that job types are collected from data."""
    from graph import get_job_types_from_db
    job_types = ['backend', 'AI']
    new_lock = PyjobData(
        title='test_title',
        descrip='test description',
        loc='Seattle, WA, USA',
        job_type='backend',
        url='randome.com'
    )
    dummy_request.dbsession.add(new_lock)
    dummy_request.dbsession.commit()
    assert 'backend' in get_job_types_from_db(job_types)


def test_dict_to_pie_chart_url():
    """Test that url with div tag is returned."""
    from graph import dict_to_pie_chart_tag
    mock_dict = {
        '1': 1,
        '2': 2,
        '3': 3
    }
    result = dict_to_pie_chart_tag(mock_dict)
    assert '<div>' in result
