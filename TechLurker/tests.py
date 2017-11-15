"""Test module for TechLurker."""
# def dummy_request(dbsession):
#     """Dummy request to simulate request."""
#     return testing.DummyRequest(dbsession=dbsession)


def test_count_words_word_found():
    """Function should return number of times given word in text."""
    from TechLurker.searching import count_words
    sentance = "The test is a test to test the word test"
    word = 'test'
    assert count_words(sentance, word) == 4


def test_count_words_word_not_found():
    """Function should return number of times given word in text."""
    from TechLurker.searching import count_words
    sentance = "The test is a test to test the word test"
    word = 'strong'
    assert count_words(sentance, word) == 0


def test_count_words_with_numbers():
    """Can this function find numbers too?."""
    from TechLurker.searching import count_words
    sentance = "The number of the day is 4"
    word = '4'
    assert count_words(sentance, word) == 1
