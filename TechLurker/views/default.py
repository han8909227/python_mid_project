"""Configure the views for the page."""


from pyramid.view import view_config, view_defaults
import graph as gt
import pdb
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from TechLurker.models.mymodel import RedditData, SecurityNewsData, PyjobData
from TechLurker.searching import count_words as cw
from TechLurker.searching import parse_job_titles as parse


@view_defaults(renderer='../templates/home.jinja2')
class LurkerViews:
    """Class that creates view functions."""

    def __init__(self, request):
        """Create an instance of the class."""
        self.request = request

    @view_config(route_name='home')
    def home_view(self):
        """Create the home view."""
        if self.request.method == "POST":
            category = self.request.POST['category'].replace(' ', '_').lower()
            return HTTPFound(self.request.route_url('results', id=category))
        return {}

    @view_config(route_name='results', renderer='../templates/results.jinja2')
    def results_view(self):
        """Create the saved results view."""
        url_list = self.request.url.split('/')
        selected = url_list[-1]
        if selected == 'job_posts':
            words = ""
            raw_data = self.request.dbsession.query(RedditData).all()
            for data in raw_data:
                words = words + data.content
            pdb.set_trace()
            # loc_list = []
            # job_types = []
            # for data in raw_data:
            #     loc_list.append(data.loc)
            #     job_list = parse(data.job_type)
            #     job_types = job_types + job_list
            # # text = text.lower()
            # # word_count = cw(text)
            # dict = gt.get_job_locations_from_db(loc_list)
            # tag1 = gt.dict_to_pie_chart_tag(dict)
            # job_dict = gt.get_job_types_from_db(job_types)
            # tag2 = gt.dict_to_pie_chart_tag(job_dict)
            # return {'tag': tag1, 'tag2': tag2}
        elif selected == 'programming_languages':
            raw_data = self.request.dbsession.query(RedditData).all()
            text = ''
            for data in raw_data:
                text = text + ' ' + data.content
            text = text.lower()
            word_count = cw(text)
            tag = gt.generate_chart_on_keyword_v2(gt.languages, word_count)
            return {'tag': tag}
        elif selected == 'security':
            raw_data = self.request.dbsession.query(SecurityNewsData).all()
            text = ''
            for data in raw_data:
                text = text + ' ' + data.articleContent
            text = text.lower()
            word_count = cw(text)
            tag = gt.generate_chart_on_keyword_v2(gt.security, word_count)
            return {'tag': tag}
        elif selected == 'programming_questions':
            raw_data = self.request.dbsession.query(RedditData).all()
            top = gt.TopFive()
            text = ''
            for data in raw_data:
                text = text + ' ' + data.content
                top.add_new_post(data)
            pdb.set_trace()
            text = text.lower()
            word_count = cw(text)
            search_terms = ['algorithm', 'sequence', 'memory', 'search', 'efficient', 'functions', 'generate', 'syntax', 'optimize']
            tag = gt.generate_chart_on_keyword_v2(search_terms, word_count)
            del top.container[0]
            return {'tag': tag, 'top': top.container}
        return {}

    @view_config(route_name='about', renderer='../templates/about.jinja2')
    def about_view(self):
        """Create the about us view."""
        return {}
