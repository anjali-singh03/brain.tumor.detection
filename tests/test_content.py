"""
test_content.py
Tests for the content dictionaries (DATA and CASES) and class configuration.
"""
import pytest
from src.config import CLASSES
from src.content import DATA, CASES

# Required keys in every DATA entry
REQUIRED_DATA_KEYS = {"title", "emoji", "overview", "causes", "symptoms",
                      "treatment", "precautions", "specialists",
                      "see_doctor", "questions"}

# Required keys in every CASES entry
REQUIRED_CASES_KEYS = {"patient", "happened", "doctors", "outcome", "links"}


# ---------------------------------------------------------------------------
# Class-order integrity
# ---------------------------------------------------------------------------

def test_class_order_consistency():
    # Model relies on exact order: glioma, meningioma, notumor, pituitary
    assert CLASSES == ["glioma", "meningioma", "notumor", "pituitary"], \
        "Class order is changed, model predictions will be wrong!"


def test_no_duplicate_classes():
    assert len(CLASSES) == len(set(CLASSES)), "CLASSES contains duplicates."


# ---------------------------------------------------------------------------
# Dictionary completeness — every class must have an entry
# ---------------------------------------------------------------------------

def test_content_dictionaries_complete():
    for c in CLASSES:
        assert c in DATA, f"Class {c} is missing from DATA dictionary"
        assert c in CASES, f"Class {c} is missing from CASES dictionary"


def test_data_has_no_extra_keys():
    """DATA must not contain keys for classes outside CLASSES."""
    for key in DATA:
        assert key in CLASSES, f"DATA has unexpected key: {key!r}"


def test_cases_has_no_extra_keys():
    """CASES must not contain keys for classes outside CLASSES."""
    for key in CASES:
        assert key in CLASSES, f"CASES has unexpected key: {key!r}"


# ---------------------------------------------------------------------------
# DATA entry structure
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("class_key", CLASSES)
def test_data_entry_has_required_keys(class_key):
    missing = REQUIRED_DATA_KEYS - DATA[class_key].keys()
    assert not missing, f"DATA[{class_key!r}] is missing keys: {missing}"


@pytest.mark.parametrize("class_key", CLASSES)
def test_data_list_fields_are_nonempty(class_key):
    """List-type fields must have at least one entry."""
    list_fields = ["causes", "symptoms", "treatment", "precautions",
                   "see_doctor", "questions"]
    entry = DATA[class_key]
    for field in list_fields:
        assert len(entry[field]) > 0, \
            f"DATA[{class_key!r}][{field!r}] must not be empty."


@pytest.mark.parametrize("class_key", CLASSES)
def test_data_string_fields_are_nonempty(class_key):
    """String-type fields must not be blank."""
    string_fields = ["title", "emoji", "overview", "specialists"]
    entry = DATA[class_key]
    for field in string_fields:
        assert entry[field].strip(), \
            f"DATA[{class_key!r}][{field!r}] must not be blank."


@pytest.mark.parametrize("class_key", CLASSES)
def test_data_titles_are_unique(class_key):
    """Every class must have a distinct display title."""
    titles = [DATA[c]["title"] for c in CLASSES]
    assert len(titles) == len(set(titles)), "DATA titles are not unique."


# ---------------------------------------------------------------------------
# CASES entry structure
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("class_key", CLASSES)
def test_cases_entry_has_required_keys(class_key):
    missing = REQUIRED_CASES_KEYS - CASES[class_key].keys()
    assert not missing, f"CASES[{class_key!r}] is missing keys: {missing}"


@pytest.mark.parametrize("class_key", CLASSES)
def test_cases_string_fields_are_nonempty(class_key):
    string_fields = ["patient", "happened", "doctors", "outcome"]
    entry = CASES[class_key]
    for field in string_fields:
        assert entry[field].strip(), \
            f"CASES[{class_key!r}][{field!r}] must not be blank."


@pytest.mark.parametrize("class_key", CLASSES)
def test_cases_links_are_tuples_of_two(class_key):
    """Each link must be a (name, url) pair."""
    for link in CASES[class_key]["links"]:
        assert len(link) == 2, \
            f"CASES[{class_key!r}]['links'] contains an item that is not a (name, url) pair: {link!r}"


@pytest.mark.parametrize("class_key", CLASSES)
def test_cases_links_urls_start_with_http(class_key):
    for name, url in CASES[class_key]["links"]:
        assert url.startswith("http"), \
            f"CASES[{class_key!r}] link URL {url!r} does not start with 'http'."
