"""Configure the views for the page."""


from pyramid.view import view_config, view_defaults
import graph as gt
import pdb
from pyramid.httpexceptions import HTTPNotFound, HTTPFound


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
            dict = gt.get_job_locations('TechLurker/python_jobs.json')
            tag1 = gt.dict_to_pie_chart_tag(dict)
            job_dict = gt.get_job_types('TechLurker/python_jobs.json')
            tag2 = gt.dict_to_pie_chart_tag(job_dict)
            return {'tag': tag1, 'tag2': tag2}
        if selected == 'programming_languages':
            tag = gt.generate_chart_on_keyword(gt.languages, 'reddit_questions.json', gt.wordcount_for_reddit)
            return {'tag': tag}
        if selected == 'security':
            tag = gt.generate_chart_on_keyword(['malware', 'phish', 'infection', 'hacking', 'breach'], 'security.json', gt.wordcount_for_reddit)
            return {'tag': tag}
        return {}

    @view_config(route_name='about', renderer='../templates/about.jinja2')
    def about_view(self):
        """Create the about us view."""
        return {}
