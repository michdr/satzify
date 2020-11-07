import pandas.api.types as ptypes
import pytest

from satzify import constants
from satzify.helpers import (annotated_names_to_keys, get_annotated_text,
                             get_tokens_df, split_annotated_text)


@pytest.fixture
def texts():
    return (
        "Alles hat ein Ende, nur die Wurst hat zwei.",
        "Also morgen ist ja genau genommen schon heute.",
        "Das Jahr ist wieder irgendwie so schnell vergangen.",
        "Ich war nur kurz was zu trinken holen und als ich zurückkam, wart ihr irgendwie weg.",
        """
        Was wir alles nicht wissen wollen! Und was wir nicht alles wissen wollen!
        Das möchte ich gar nicht wissen. Und wenn man es dann doch weiß, weil der andere sein Wissen einfach nicht für sich behalten konnte, dann können wir ja nichts dafür, wir wollten es ja gar nicht wissen. Und eine Klatschtante sind wir dann auch nicht.
        """,
    )


@pytest.fixture
def cases():
    return constants.CASES


@pytest.fixture
def pos():
    return constants.POS


@pytest.fixture
def colors():
    cases_and_pos_settings = {**constants.CASES, **constants.POS}
    colors = {k: v["color"] for k, v in cases_and_pos_settings.items()}
    return colors


@pytest.fixture
def example_text():
    return "Alles hat ein Ende, nur die Wurst hat zwei."


@pytest.fixture
def example_pos_annotations(example_text):
    return [
        (["Alles "], "Pronoun", "#fea"),
        (["hat "], "Verb", "#8ef"),
        "ein ",
        (["Ende"], "Noun", "#afa"),
        ", ",
        (["nur "], "Adverb", "#d94"),
        "die ",
        (["Wurst "], "Noun", "#afa"),
        (["hat "], "Verb", "#8ef"),
        "zwei",
        ".",
    ]


@pytest.fixture
def example_cases_annotations(example_text):
    return [
        (["Alles "], "Nom+N", "#afa"),
        "hat ",
        (["ein ", "Ende"], "Acc+N", "#fea"),
        ", ",
        "nur ",
        (["die ", "Wurst "], "Nom+F", "#afa"),
        "hat ",
        "zwei",
        ".",
    ]


def test_get_tokens_df(texts):
    for text in texts:
        tokens_df = get_tokens_df(text)
        assert ptypes.is_numeric_dtype(tokens_df["idx"].apply(int))
        assert ptypes.is_string_dtype(tokens_df["text"])
        assert ptypes.is_string_dtype(tokens_df["morph"])
        assert ptypes.is_string_dtype(tokens_df["pos_"])
        morphs = tokens_df[tokens_df["morph"] != ""]["morph"].to_list()
        for morph in morphs:
            parts = morph.split("|")
            # ensure that each and every part of a morph has a key=value structure, i.e. Case=Nom
            assert all(len(part.split("=")) == 2 for part in parts)


def test_annotated_names_to_keys(pos):
    annotated_names = ["Noun", "Verb", "Adposition"]
    keys = annotated_names_to_keys(pos, annotated_names)
    assert keys == ["NOUN", "VERB", "ADP"]


def test_pos_annotations(pos, colors, example_text, example_pos_annotations):
    pos_annotated_names = [v["name"] for v in pos.values()]
    annotations = get_annotated_text("POS", example_text, pos_annotated_names, colors)
    assert annotations == example_pos_annotations


def test_cases_annotations(cases, colors, example_text, example_cases_annotations):
    pos_annotated_names = [v["name"] for v in cases.values()]
    annotations = get_annotated_text("CASES", example_text, pos_annotated_names, colors)
    assert annotations == example_cases_annotations


def test_split_annotated_text(example_pos_annotations, example_cases_annotations):
    combined_annotations = example_pos_annotations + ["\n"] + example_cases_annotations
    list_annotated_text = split_annotated_text(combined_annotations)
    assert len(list_annotated_text) == 2
    assert list_annotated_text[0] == example_pos_annotations
    assert list_annotated_text[1] == example_cases_annotations
