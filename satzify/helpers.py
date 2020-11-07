from itertools import count, groupby
from typing import Any, Dict, List, Tuple, Union

import pandas as pd
import spacy
from spacy.tokens.doc import Doc
from spacy_streamlit.visualizer import TOKEN_ATTRS
from streamlit import cache as st_cache

from . import constants


@st_cache(allow_output_mutation=True)
def load_spacy_nlp_model() -> spacy.language.Language:
    return spacy.load(constants.SPACY_MODEL)


def _doc_text(doc: Doc) -> str:
    # a workaround to use st_cache for get_doc
    return doc.text  # type: ignore


@st_cache(hash_funcs={Doc: _doc_text})
def get_doc(text: str) -> spacy.tokens.Doc:
    nlp = load_spacy_nlp_model()
    return nlp(text)


def get_tokens_df(text: str) -> pd.DataFrame:
    doc = get_doc(text)
    return _get_tokens_df(doc)


def _get_tokens_df(
    doc: Doc,
    attrs: List[str] = TOKEN_ATTRS,
) -> pd.DataFrame:
    data = [[str(getattr(token, attr)) for attr in attrs] for token in doc]
    df = pd.DataFrame(data, columns=attrs)
    return df


def annotated_names_to_keys(
    annotate_settings: Dict[str, dict], annotated_names: List[str]
) -> List[str]:
    return [k for k, v in annotate_settings.items() if v.get("name") in annotated_names]


def get_pos_annotation(
    text: str,
    annotated_keys: List[str],
    annotations_settings: Dict,
    colors: Dict[str, str],
    row: pd.Series,
    idx: int,
    next_idx: int,
) -> Union[Tuple[str, Any, str], str]:
    pos = row.get("pos_")
    if pos in annotated_keys:
        return text[idx:next_idx], annotations_settings[pos]["name"], colors[pos]
    else:
        return text[idx:next_idx]


def get_cases_annotation(
    text: str,
    annotated_keys: List[str],
    _: Dict,
    colors: Dict[str, str],
    row: pd.Series,
    idx: int,
    next_idx: int,
) -> Union[Tuple[str, Any, str], str]:
    morph = row.get("morph")
    if not morph:
        return text[idx:next_idx]

    morph_parts = {
        mor_p.split("=")[0]: mor_p.split("=")[1] for mor_p in morph.split("|")
    }
    case = morph_parts.get("Case")
    gender = morph_parts.get("Gender")
    if not case or not isinstance(case, str) or not case.upper() in annotated_keys:
        return text[idx:next_idx]

    cur_annotation = case + (f"+{gender[0]}" if gender else "")
    return text[idx:next_idx], cur_annotation, colors[case.upper()]


ANNOTATION_FUNCTIONS = dict(POS=get_pos_annotation, CASES=get_cases_annotation)


def merge_same_annotation_texts(annotations: list) -> list:
    groups = groupby(
        annotations, key=lambda x: x[1] if isinstance(x, tuple) else count()  # type: ignore
    )  # group only tuples, strings - never group
    merged_annotations_lists = [list(g) for k, g in groups]
    merged_annotations: List[Union[str, Tuple]] = list()
    for mal in merged_annotations_lists:
        if not mal:
            continue
        if isinstance(mal[0], str):
            merged_annotations.append(mal[0])
        else:
            merged_text = [item[0] for item in mal]
            merged_annotations.append((merged_text, mal[0][1], mal[0][2]))

    return merged_annotations


def get_annotated_text(
    what_to_annotate: str, text: str, annotated_names: List[str], colors: Dict[str, str]
) -> list:
    annotations_settings = constants.ANNOTATIONS[what_to_annotate]
    annotation_function = ANNOTATION_FUNCTIONS[what_to_annotate]
    annotations = list()
    tokens_df = get_tokens_df(text)
    n_rows = tokens_df.shape[0]
    annotated_keys = annotated_names_to_keys(annotations_settings, annotated_names)
    for index, row in tokens_df.iterrows():
        idx = int(row.get("idx"))
        next_idx = int(
            tokens_df.iloc[index + 1].idx if (index + 1) < n_rows else len(text)
        )
        annotation = annotation_function(
            text, annotated_keys, annotations_settings, colors, row, idx, next_idx
        )
        annotations.append(annotation)
    return merge_same_annotation_texts(annotations)


def split_annotated_text(annotated_text: list, delimiter: str = "\n") -> list:
    return [
        list(group)
        for k, group in groupby(annotated_text, lambda x: x == delimiter)  # type: ignore
        if not k
    ]
