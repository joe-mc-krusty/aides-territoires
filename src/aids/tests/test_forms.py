"""Test methods aid related forms."""

import pytest
from django.contrib.admin.sites import AdminSite

from aids.models import Aid
from aids.admin import AidAdmin
from aids.forms import AidSearchForm
from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def aid_form_class():
    """Generates a valid form class.

    Since `AidFormAdmin` is an admin form, is is declared without the usual
    `model` and `fields` configuration parameters. That's why it has to be
    instanciated that way.
    """

    site = AdminSite()
    admin = AidAdmin(Aid, site)
    form_class = admin.get_form(None)
    return form_class


@pytest.fixture
def aid_form_data(user, backer):
    """Returns valid data to create an Aid object."""

    return {
        'name': 'Test aid',
        'author': user.id,
        'backers': [backer.id],
        'description': 'My aid description',
        'eligibility': 'Aid eligibility info',
        'application_perimeter': 'france',
        'mobilization_steps': ['preop'],
        'targeted_audiances': ['department'],
        'aid_types': ['grant', 'loan'],
        'destinations': ['supply'],
        'publication_status': 'open',
        'status': 'published',
    }


@pytest.fixture
def aids(user, backer):
    """Generates a few aids and return the corresponding queryset."""

    AidFactory(
        author=user,
        backers=[backer],
        is_funding=True,
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        application_perimeter='europe')
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=True,
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        application_perimeter='france')
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=True,
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        application_perimeter='mainland')
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=True,
        submission_deadline='2018-01-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        application_perimeter='overseas')
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=False,
        submission_deadline='2018-05-01',
        mobilization_steps=['preop'],
        aid_types=['grant', 'loan'],
        application_perimeter='region',
        application_region='01')  # Guadeloupe
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=False,
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        application_perimeter='region',
        application_region='02')  # Martinique
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=False,
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        application_perimeter='region',
        application_region='28')  # Normandie
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=False,
        submission_deadline='2018-05-01',
        mobilization_steps=['preop', 'op'],
        aid_types=['grant', 'loan'],
        application_perimeter='region',
        application_region='76')  # Occitanie
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=False,
        submission_deadline='2018-09-01',
        mobilization_steps=['preop', 'op', 'postop'],
        aid_types=['loan'],
        application_perimeter='department',
        application_department='972')  # Martinique
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=False,
        submission_deadline='2018-09-01',
        mobilization_steps=['op', 'postop'],
        aid_types=['loan'],
        application_perimeter='department',
        application_department='973')  # Guyane
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=False,
        submission_deadline='2018-09-01',
        mobilization_steps=['op', 'postop'],
        aid_types=[],
        application_perimeter='department',
        application_department='27')  # Eure
    AidFactory(
        author=user,
        backers=[backer],
        is_funding=False,
        submission_deadline='2018-09-01',
        mobilization_steps=['postop'],
        aid_types=['networking', 'return_fund'],
        application_perimeter='department',
        application_department='34')  # Hérault

    qs = Aid.objects.all().order_by('id')
    return qs


def test_form_default(aid_form_class, aid_form_data):
    """Test the form with default values."""

    form = aid_form_class(aid_form_data)
    assert form.is_valid()


def test_form_filter_mobilization_step(aids):
    form = AidSearchForm({'mobilization_step': ['preop']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 9
    for aid in qs:
        assert 'preop' in aid.mobilization_steps

    form = AidSearchForm({'mobilization_step': ['op']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 6
    for aid in qs:
        assert 'op' in aid.mobilization_steps

    form = AidSearchForm({'mobilization_step': ['postop']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 4
    for aid in qs:
        assert 'postop' in aid.mobilization_steps

    form = AidSearchForm({'mobilization_step': ['preop', 'postop']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 12
    for aid in qs:
        assert any((
            'preop' in aid.mobilization_steps,
            'postop' in aid.mobilization_steps))


def test_form_filter_by_types(aids):
    form = AidSearchForm({'aid_types': ['grant']})
    qs = form.filter_queryset(aids)
    assert qs.count() == 8
    for aid in qs:
        assert 'grant' in aid.aid_types

    form = AidSearchForm({'aid_types': ['grant', 'networking']})
    qs = form.filter_queryset(aids)
    for aid in qs:
        print(aid.aid_types)
    assert qs.count() == 9
    for aid in qs:
        assert 'grant' in aid.aid_types or 'networking' in aid.aid_types


def test_form_filter_by_deadline(aids):
    form = AidSearchForm({'apply_before': '2018-12-01'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 12

    form = AidSearchForm({'apply_before': '2018-08-01'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 8

    form = AidSearchForm({'apply_before': '2018-04-01'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 4

    form = AidSearchForm({'apply_before': '2018-01-01'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 0

    form = AidSearchForm({'apply_before': '2017-12-31'})
    qs = form.filter_queryset(aids)
    assert qs.count() == 0
