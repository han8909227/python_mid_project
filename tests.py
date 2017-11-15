
# def dummy_request(dbsession):
#     """Dummy request to simulate request."""
#     return testing.DummyRequest(dbsession=dbsession)


def test_count_words_word_found():
    """Function should return number of times given word in text."""
    from TechLurker.searching import count_words
    sentance = "The test is a test to test the word test"
    word = 'test'
    assert count_words(sentance, word) == 4
