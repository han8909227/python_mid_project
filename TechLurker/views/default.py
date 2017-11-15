"""Configure the views for the page."""


from pyramid.view import view_config, view_defaults
import graph as gt
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from TechLurker.models.mymodel import RedditData, SecurityNewsData, PyjobData
from TechLurker.searching import count_words as cw
from TechLurker.searching import parse_job_titles as parse


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """Create the home view."""
    if request.method == "POST":
        category = request.POST['category'].replace(' ', '_').lower()
        return HTTPFound(request.route_url('results', id=category))
    return {}


@view_config(route_name='results', renderer='../templates/results.jinja2')
def results_view(request):
    """Create the saved results view."""
    url_list = request.url.split('/')
    selected = url_list[-1]
    if selected == 'job_posts':
        raw_data = request.dbsession.query(PyjobData).all()
        loc_list = []
        job_types = []
        for data in raw_data:
            loc_list.append(data.loc)
            job_list = parse(data.job_type)
            job_types = job_types + job_list
        # text = text.lower()
        # word_count = cw(text)
        dict = gt.get_job_locations_from_db(loc_list)
        tag1 = gt.dict_to_pie_chart_tag(dict)
        job_dict = gt.get_job_types_from_db(job_types)
        tag2 = gt.dict_to_pie_chart_tag(job_dict)
        return {'tag': tag1, 'tag2': tag2}
    elif selected == 'programming_languages':
        raw_data = request.dbsession.query(RedditData).all()
        text = ''
        for data in raw_data:
            text = text + ' ' + data.content
        text = text.lower()
        word_count = cw(text)
        tag = gt.generate_chart_on_keyword_v2(gt.languages, word_count)
        return {'tag': tag}
    elif selected == 'security':
        raw_data = request.dbsession.query(SecurityNewsData).all()
        text = ''
        for data in raw_data:
            text = text + ' ' + data.articleContent
        text = text.lower()
        word_count = cw(text)
        tag = gt.generate_chart_on_keyword_v2(gt.security, word_count)
        return {'tag': tag}
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Create the about us view."""
    return {}
