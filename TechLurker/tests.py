"""Test module for TechLurker."""
# def dummy_request(dbsession):
#     """Dummy request to simulate request."""
#     return testing.DummyRequest(dbsession=dbsession)
import pytest
from pyramid import testing
import transaction
from TechLurker.models import (
    RedditData, PyjobData, TechRepublicData, SecurityNewsData, get_tm_session,
)
from TechLurker.models.meta import Base
# from datetime import datetime
from webtest.app import AppError
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
# from faker import Faker
from TechLurker.views.default import home_view, results_view, about_view
import pdb


@pytest.fixture(scope='session')
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://postgres:potato@localhost:5432/test_tl'
    })
    config.include("TechLurker.models")
    config.include("TechLurker.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.

    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


def test_home_page(dummy_request):
    """Test index return list of journals."""
    response = home_view(dummy_request)
    assert response == {}


def test_about_page(dummy_request):
    """Test about page is loaded."""
    response = about_view(dummy_request)
    assert response == {}


@pytest.fixture(scope="session")
def testapp(request):
    """Initialte teh test app."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': 'postgres://postgres:potato@localhost:5432/test_tl'
        }  # points to a database
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('TechLurker.routes')
        config.include('TechLurker.models')
        config.scan()
        return config.make_wsgi_app()

    app = main()

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)  # builds the tables

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)
    return TestApp(app)


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
    results = generate_chart_on_keyword_v2(data, word_count, 'title')
    assert '<div>' in results


def test_chart_on_keyword_returns_type_error_if_no_data():
    """Test a type error returned if missing data."""
    from graph import generate_chart_on_keyword_v2
    from TechLurker.searching import count_words
    with pytest.raises(TypeError):
        generate_chart_on_keyword_v2(count_words, 'title')


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
    result = dict_to_pie_chart_tag(mock_dict, 'title')
    assert '<div>' in result


def test_post_to_home_404_no_category(testapp):
    """Post to home page should redirect to results."""
    try:
        testapp.post('/', {'category': None})
    except AppError as err:
        assert '404 Not Found' in err.args[0]


def test_get_bad_url_raise_404(testapp):
    """Post to home page should redirect to results."""
    try:
        testapp.get('/results/test')
    except AppError as err:
        assert '404 Not Found' in err.args[0]


def test_post_to_job_raise_404(testapp):
    """Post to results/jobs should return jobs as the result parameter."""
    try:
        testapp.post('/results/test', {})
    except AppError as err:
        assert '404 Not Found' in err.args[0]


def est_get_results_job_posts(testapp):
    """Post to results/jobs should redirect to results page."""
    response = testapp.get('/results/job_posts')
    assert 'python.org/jobs' in response.ubody


def test_get_results_programming_languages(testapp):
    """Get request to results/prgoraming_languages."""
    response = testapp.get('/results/programming_languages')
    assert 'Reddit' in response.ubody


def test_get_results_security(testapp):
    """Get request to results/security."""
    response = testapp.get('/results/security')
    assert 'trendmicro' in response.ubody


def test_get_results_programming_questions(testapp):
    """Get request to results/programming_questions."""
    response = testapp.get('/results/programming_questions')
    assert 'Reddit' in response.ubody


def test_get_results_webdev(testapp):
    """Get request to results/webdev."""
    response = testapp.get('/results/webdev')
    assert 'TechRepublic/webdev' in response.ubody


def test_get_results_job_posts_doesnt_have_incorrect(testapp):
    """Post to results/jobs should redirect to results page."""
    response = testapp.get('/results/job_posts')
    assert 'TechRepublic/webdev' not in response.ubody


def test_get_results_programming_languages_doesnt_have_incorrect(testapp):
    """Get request to results/prgoraming_languages."""
    response = testapp.get('/results/programming_languages')
    assert 'trendmicro' not in response.ubody


def test_get_results_security_doesnt_have_incorrect(testapp):
    """Get request to results/security."""
    response = testapp.get('/results/security')
    assert 'Reddit' not in response.ubody


def test_get_results_programming_questions_doesnt_have_incorrect(testapp):
    """Get request to results/programming_questions."""
    response = testapp.get('/results/programming_questions')
    assert 'TechRepublic/webdev' not in response.ubody


def test_get_results_webdev_doesnt_have_incorrect(testapp):
    """Get request to results/webdev."""
    response = testapp.get('/results/webdev')
    assert 'Reddit' not in response.ubody


def test_db_had_model_pyjob_title(dummy_request):
    """Pyjob data should have title stored correctly."""
    new_lock = PyjobData(
        title='test_title',
        descrip='test description',
        loc='Seattle, WA, USA',
        job_type='backend',
        url='randome.com'
    )
    dummy_request.dbsession.add(new_lock)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(PyjobData).all()
    assert response[0].title == 'test_title'


def test_db_had_model_pyjob_url(dummy_request):
    """Pyjob data should have url stored correctly."""
    new_lock = PyjobData(
        title='test_title',
        descrip='test description',
        loc='Seattle, WA, USA',
        job_type='backend',
        url='randome.com'
    )
    dummy_request.dbsession.add(new_lock)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(PyjobData).all()
    assert response[0].url == 'randome.com'


def test_db_stores_redditdata_title(dummy_request):
    """Redditdata data should have title stored correctly."""
    sample_reddit = RedditData(
        title='A_Post',
        content='This is a reddit post',
        score='100000000'
    )
    dummy_request.dbsession.add(sample_reddit)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(RedditData).all()
    assert response[0].title == 'A_Post'


def test_db_stores_redditdata_content(dummy_request):
    """Redditdata data should have content stored correctly."""
    sample_reddit = RedditData(
        title='A_Post',
        content='This is a reddit post',
        score='100000000'
    )
    dummy_request.dbsession.add(sample_reddit)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(RedditData).all()
    assert response[0].content == 'This is a reddit post'


def test_db_stores_securitydata_date(dummy_request):
    """Securitynewsdata should have date stored correctly."""
    sample_security = SecurityNewsData(
        title='Security Yo',
        articleContent='This is an article about cyber security',
        date='11/17/2017',
        url='www.security.com'
    )
    dummy_request.dbsession.add(sample_security)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(SecurityNewsData).all()
    assert response[0].date == '11/17/2017'


def test_db_stores_securitydata_title(dummy_request):
    """Securitynewsdata should have title stored correctly."""
    sample_security = SecurityNewsData(
        title='Security Yo',
        articleContent='This is an article about cyber security',
        date='11/17/2017',
        url='www.security.com'
    )
    dummy_request.dbsession.add(sample_security)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(SecurityNewsData).all()
    assert response[0].title == 'Security Yo'


def test_db_stores_techrepublicdata_from_forum(dummy_request):
    """Techrepublicdata should have from_forum stored correctly."""
    sample_techrepublic = TechRepublicData(
        title='tech newz',
        content='an awesome artile about something',
        votes='A lot, like more than one',
        from_forum='webdev'
    )
    dummy_request.dbsession.add(sample_techrepublic)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(TechRepublicData).all()
    assert response[0].from_forum == 'webdev'


def test_db_stores_techrepublicdata_title(dummy_request):
    """Techrepublicdata should have title stored correctly."""
    sample_techrepublic = TechRepublicData(
        title='tech newz',
        content='an awesome artile about something',
        votes='A lot, like more than one',
        from_forum='webdev'
    )
    dummy_request.dbsession.add(sample_techrepublic)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(TechRepublicData).all()
    assert response[0].title == 'tech newz'


def test_view_has_result_from_database_pyjobdata(dummy_request, testapp):
    """Pyjob data should have title stored correctly."""
    new_lock = PyjobData(
        title='test_title',
        descrip='test description',
        loc='Seattle, WA, USA',
        job_type='backend',
        url='randome.com'
    )
    dummy_request.dbsession.add(new_lock)
    dummy_request.dbsession.commit()
    response = testapp.get('/results/job_posts')
    assert 'python.org/jobs' in response.ubody


def test_view_has_result_from_database_redditdata_pl(dummy_request, testapp):
    """Redditdata data should have title stored correctly."""
    sample_reddit = RedditData(
        title='A_Post',
        content='This is a reddit post',
        score='100000000'
    )
    dummy_request.dbsession.add(sample_reddit)
    dummy_request.dbsession.commit()
    response = testapp.get('/results/programming_languages')
    assert 'Reddit' in response.ubody


def test_view_has_result_from_database_security(dummy_request, testapp):
    """Securitynewsdata should have date stored correctly."""
    sample_security = SecurityNewsData(
        title='Security Yo',
        articleContent='This is an article about cyber security',
        date='11/17/2017',
        url='www.security.com'
    )
    dummy_request.dbsession.add(sample_security)
    dummy_request.dbsession.commit()
    response = dummy_request.dbsession.query(SecurityNewsData).all()
    assert response[0].date == '11/17/2017'
    response = testapp.get('/results/security')
    assert 'trendmicro' in response.ubody


def test_view_has_result_from_database_redditdata_pq(dummy_request, testapp):
    """Redditdata data should have title stored correctly."""
    sample_reddit = RedditData(
        title='A_Post',
        content='This is a reddit post',
        score='100000000'
    )
    dummy_request.dbsession.add(sample_reddit)
    dummy_request.dbsession.commit()
    response = testapp.get('/results/programming_questions')
    assert 'Reddit' in response.ubody


def test_view_has_result_from_database_tr_webdev(dummy_request, testapp):
    """Techrepublicdata should have from_forum stored correctly."""
    sample_techrepublic = TechRepublicData(
        title='tech newz',
        content='an awesome artile about something',
        votes='A lot, like more than one',
        from_forum='webdev'
    )
    dummy_request.dbsession.add(sample_techrepublic)
    dummy_request.dbsession.commit()
    response = testapp.get('/results/webdev')
    assert 'TechRepublic/webdev' in response.ubody
