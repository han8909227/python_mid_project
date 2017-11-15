"""Routes config."""


def includeme(config):
    """All routes for the app."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('results', '/results/{id:\w+}')
    config.add_route('about', '/about')
