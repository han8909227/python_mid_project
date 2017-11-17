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


# @pytest.fixture
# def new_journal():
#     """Provide a fixture for one journal."""
#     new = MyModel(
#         id=1,
#         title=u'test journal',
#         body=u'test_body',
#         creation_date=datetime.now()
#     )
#     return new


def test_home_page(dummy_request):
    """Test index return list of journals."""
    response = home_view(dummy_request)
    assert response == {}


def test_about_page(dummy_request):
    """Test about page is loaded."""
    response = about_view(dummy_request)
    assert response == {}


# def test_detail_view_shows_journal_detail(dummy_request, new_journal):
#     """Test detail view show journal details."""
#     dummy_request.dbsession.add(new_journal)
#     dummy_request.dbsession.commit()
#     dummy_request.matchdict['id'] = 1
#     response = detail_view(dummy_request)
#     assert response['Journal'] == new_journal.to_dict()


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


# FAKE = Faker()
# JOURNALS = []
# for i in range(9):
#     journals = MyModel(
#         id=i,
#         title=FAKE.file_name(),
#         body=FAKE.paragraph(),
#         creation_date=FAKE.date_time()
#     )
#     JOURNALS.append(journals)


# @pytest.fixture(scope="session")
# def fill_the_db(testapp):
#     """Fill the db with fake journal entries."""
#     SessionFactory = testapp.app.registry["dbsession_factory"]
#     with transaction.manager:
#         dbsession = get_tm_session(SessionFactory, transaction.manager)
#         dbsession.add_all(JOURNALS)


# def test_home_route_has_table(testapp):
#     """Test route has table."""
#     response = testapp.get("/")
#     assert len(response.html.find_all('table')) == 1
#     assert len(response.html.find_all('tr')) == 1


# def test_home_route_with_journals_has_rows(testapp, fill_the_db):
#     """Test home route has rows."""
#     response = testapp.get("/")
#     assert len(response.html.find_all('tr')) == 10


# def test_detail_route_with_journal_detail(testapp, fill_the_db):
#     """Test if detail papge has proper response.."""
#     response = testapp.get("/journal/1")
#     assert 'ID: 1' in response.ubody


# @pytest.fixture
# def journal_info():
#     """Create a info dictionary for edit or create later."""
#     info = {
#         'title': 'testing',
#         'body': 'testing_body',
#         'creation_date': '2017-11-02'
#     }
#     return info


# @pytest.fixture
# def edit_info():
#     """Create a dict for editing purpose."""
#     info = {
#         'title': 'edited journal',
#         'body': 'I just changed the journal created in above test',
#         'creation_date': ''
#     }
#     return info


# def test_create_view_successful_post_redirects_home(testapp, journal_info):
#     """Test create view directs to same loc."""
#     response = testapp.post("/journal/new-entry", journal_info)
#     assert response.location == 'http://localhost/'


# def test_create_view_successful_post_actually_shows_home_page(testapp, journal_info):
#     """Test create view folow up with detail page."""
#     response = testapp.post("/journal/new-entry", journal_info)
#     next_page = response.follow()
#     assert "testing" in next_page.ubody


# def test_edit_method_successful_updates(testapp, edit_info):
#     """Test if content is updated successfully."""
#     response = testapp.post('/journal/1/edit-entry', edit_info)
#     next_page = response.follow()
#     assert 'edited journal' in next_page.ubody


# def test_edit_method_successful_updates_and_directs_detail_view(testapp, edit_info):
#     """Test after updating we get re-directed to detail view."""
#     response = testapp.post('/journal/1/edit-entry', edit_info)
#     assert response.location == 'http://localhost/journal/1'


# def test_edit_method_return_httpnotfound(testapp, edit_info):
#     """Assert if a http not found error(raised by apperror) is popped from invalid post req."""
#     with pytest.raises(AppError):
#         testapp.post('/journal/200/edit-entry', edit_info)


# def test_create_method_return_httpnotfound_with_no_var(testapp):
#     """Assert if a http not found error(raised by apperror) is popped from invalid post req."""
#     with pytest.raises(AppError):
#         testapp.post('/journal/new-entry', {})


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
