import transaction

from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


