import contextlib
import mock
import pytest


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


def test_chart_on_keyword_returns_chart():
    """Test that html is generated for the chart."""
    from graph import generate_chart_on_keyword_v2
    from TechLurker.searching import count_words
    data = ['a', 'b', 'c', 'a', 'a', 'b']
    results = generate_chart_on_keyword_v2(data, count_words)
    assert '<h1>' in results


def test_chart_on_keyword_returns_type_error_if_no_data():
    """Test a type error returned if missing data."""
    from graph import generate_chart_on_keyword_v2
    from TechLurker.searching import count_words
    with pytest.raises(TypeError):
        generate_chart_on_keyword_v2(count_words)
