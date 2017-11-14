"""Configure the views for the page."""


from pyramid.view import view_config, view_defaults
import graph_test as gt
import pdb
from pyramid.compat import escape


@view_defaults(renderer='../templates/home.jinja2')
class LurkerViews:
    """Class that creates view functions."""

    def __init__(self, request):
        """Create an instance of the class."""
        self.request = request

    @view_config(route_name='home')
    def home_view(self):
        """Create the home view."""
        return {}

    @view_config(route_name='results', renderer='../templates/results.jinja2')
    def results_view(self):
        """Create the new results view."""
        dict = gt.get_job_locations('TechLurker/python_jobs.json')
        tag = gt.dict_to_pie_chart_tag(dict)
        result = escape(tag)
        return {'tag': result}
        # return {}

    @view_config(route_name='saved_results', renderer='../templates/results.jinja2')
    def saved_results_view(self):
        """Create the saved results view."""
        return {}

    @view_config(route_name='about', renderer='../templates/about.jinja2')
    def about_view(self):
        """Create the about us view."""
        return {}
