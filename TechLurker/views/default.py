"""Configure the views for the page."""


from pyramid.view import view_config, view_defaults
import graph as gt
import pdb
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from TechLurker.models.mymodel import RedditData, SecurityNewsData, PyjobData, TechRepublicData
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
            raw_data = self.request.dbsession.query(PyjobData).all()
            job_titles = []
            loc_list = []
            job_types = []
            for data in raw_data:
                loc_list.append(data.loc)
                job_list = parse(data.job_type)
                job_types = job_types + job_list
                job_titles.append(data.title)
            dict = gt.get_job_locations_from_db(loc_list)
            tag1 = gt.dict_to_pie_chart_tag(dict, "Programming Jobs by Country")
            job_dict = gt.get_job_types_from_db(job_types)
            tag2 = gt.dict_to_pie_chart_tag(job_dict, "Programming Job Types")
            return {'tag': tag1, 'tag2': tag2, 'result': 'job', 'url': 'https://www.python.org/jobs/', 'site_name': 'python.org/jobs', 'data': job_titles}

        elif selected == 'programming_languages':
            raw_data = self.request.dbsession.query(RedditData).all()
            text = ''
            return_val = []
            for data in raw_data:
                text = text + ' ' + data.content
                return_val.append((data.title, data.score))
            text = text.lower()
            word_count = cw(text)
            tag = gt.generate_chart_on_keyword_v2(gt.languages, word_count, 'Language Popularity')
            tag2 = gt.generate_pie_chart_on_keyword(gt.languages, word_count, "Language Popularity")
            return {'tag': tag,
                    'tag2': tag2,
                    'result': 'language',
                    'url': 'https://www.reddit.com/r/learnprogramming/',
                    'site_name': 'Reddit',
                    'data': return_val}

        elif selected == 'security':
            raw_data = self.request.dbsession.query(SecurityNewsData).all()
            text = ''
            raw_security_data = []
            for data in raw_data:
                text = text + ' ' + data.articleContent
                raw_security_data.append((data.title, data.url))
            text = text.lower()
            raw_data = self.request.dbsession.query(TechRepublicData).all()
            security_data = ''
            for post in raw_data:
                if post.from_forum == "security":
                    security_data = security_data + post.content + ' '
            security_text = security_data.lower()
            text = text + ' ' + security_text
            word_count = cw(text)
            tag = gt.generate_chart_on_keyword_v2(gt.security, word_count, 'security')
            tag2 = gt.generate_pie_chart_on_keyword(gt.security, word_count, "security")
            return {'tag': tag, 'tag2': tag2, 'result': 'security', 'url': 'https://www.trendmicro.com/vinfo/us/security/news/all/page/2', 'site_name': 'trendmicro.com', 'data': raw_security_data}

        elif selected == 'programming_questions':
            raw_data = self.request.dbsession.query(RedditData).all()
            text = ''
            question_data = []
            for data in raw_data:
                text = text + ' ' + data.content
                question_data.append((data.title, data.score))
            text = text.lower()
            word_count = cw(text)
            search_terms = ['algorithm', 'sequence', 'memory', 'search', 'efficient', 'functions', 'generate', 'syntax', 'optimize']
            tag = gt.generate_chart_on_keyword_v2(search_terms, word_count, 'Most asked programming questions')
            tag2 = gt.generate_pie_chart_on_keyword(search_terms, word_count, "Most asked programming questions")
            return {'tag': tag, 'tag2': tag2, 'result': 'questions', 'url': 'https://www.reddit.com/r/learnprogramming/', 'site_name': 'Reddit', 'data': question_data}

        elif selected == 'webdev':
            raw_data = self.request.dbsession.query(TechRepublicData).all()
            web_data = ''
            raw_web_data = []
            for post in raw_data:
                if post.from_forum == "web_development":
                    web_data = web_data + post.content + ' '
                    raw_web_data.append(post.title)
            text = web_data.lower()
            word_count = cw(web_data)
            search_terms = ['development', 'application', 'website', 'database', 'server', 'wordpress', 'javascript', 'node', 'hosting', 'search']
            tag = gt.generate_chart_on_keyword_v2(search_terms, word_count, 'Trending terms in web development')
            tag2 = gt.generate_pie_chart_on_keyword(search_terms, word_count, "Trending terms in web development")
            return {'tag': tag, 'tag2': tag2, 'result': 'webdev', 'url': "https://www.techrepublic.com/forums/web-development/", 'site_name': 'TechRepublic/webdev', 'data': raw_web_data}
        return {}

    @view_config(route_name='about', renderer='../templates/about.jinja2')
    def about_view(self):
        """Create the about us view."""
        return {}
