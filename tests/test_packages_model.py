import pytest
from hsw import packages as pkgs


@pytest.fixture()
def packages():
    return pkgs.Packages()
    pass


def test_package_empty_len(packages):
    assert len(packages) == 0


def test_add_file_entry(packages):
    packages.add_package(path="c://temp/foo")
    assert len(packages) == 1


def test_set_and_retrieve_entry(packages):
    packages.add_package(path="c://temp/foo")
    assert len(packages) == 1
    spam = packages["c://temp/foo"]
    assert spam.path == "c://temp/foo"
    assert spam["pages"] == []


def test_alert_dup_added(packages):
    packages.add_package(path="c://temp/foo")
    with pytest.raises(FileExistsError):
        packages.add_package(path="c://temp/foo")