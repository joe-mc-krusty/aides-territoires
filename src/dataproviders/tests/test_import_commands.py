import pytest

from dataproviders.management.commands.base import BaseImportCommand
from accounts.factories import UserFactory
from backers.factories import BackerFactory
from aids.factories import AidFactory
from aids.models import Aid


pytestmark = pytest.mark.django_db


class ImportStub(BaseImportCommand):
    """Stub implementation for testing purpose."""

    def __init__(self, *args, **kwargs):
        self.aids = kwargs.pop('aids')
        self.financer = kwargs.pop('financer')
        super().__init__(*args, **kwargs)

    def populate_cache(self, *args, **kwargs):
        self.author = UserFactory()

    def fetch_data(self):
        return self.aids

    def extract_name(self, line):
        return line.name

    def extract_financers(self, line):
        return [self.financer]

    def extract_import_uniqueid(self, line):
        return line.slug

    def extract_import_data_url(self, line):
        return 'https:///example.com/aid/{}'.format(line.id)

    def extract_import_share_licence(self, line):
        return Aid.IMPORT_LICENCES.unknown

    def extract_description(self, line):
        return line.description

    def extract_eligibility(self, line):
        return line.eligibility

    def extract_author_id(self, line):
        return self.author.id

    def extract_project_examples(self, line):
        return ''

    def extract_contact(self, line):
        return ''


def test_importing_new_aids():
    """The import commands create the aids from provided data."""

    financer = BackerFactory()
    # Use aid factory to gather valid aid data
    aids = AidFactory.build_batch(5)
    for aid in aids:
        aid.set_slug()

    stub = ImportStub(aids=aids, financer=financer)

    aids = Aid.objects.all()
    assert aids.count() == 0

    stub.handle()
    assert aids.count() == 5


def test_importing_existing_aids():
    """Import only update aids that already exist."""

    financer = BackerFactory()
    aids = AidFactory.build_batch(5)
    for aid in aids:
        aid.set_slug()

    # The first import task will save aid data to the db
    stub = ImportStub(aids=aids, financer=financer)
    stub.handle()

    aids = Aid.objects.all()
    assert aids.count() == 5

    # On the second run, since aid with those unique id already exist,
    # no new aid are created
    stub.handle()
    assert aids.count() == 5
