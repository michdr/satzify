import streamlit as st
from annotated_text import annotated_text
from spacy_streamlit import visualize_parser

from satzify import constants
from satzify.helpers import (
    get_annotated_text,
    get_doc,
    get_tokens_df,
    load_spacy_nlp_model, split_annotated_text
)

colors = dict()
st.set_page_config(page_title="satzify - simply annotate sentences")
text = st.text_area("Input text", value=constants.EXAMPLE_TEXT)
nlp = load_spacy_nlp_model()
tokens_df = get_tokens_df(text)

# Sidebar top part
with st.sidebar.beta_expander("What is satzify", expanded=False):
    st.markdown(constants.WHAT_IS_SATZIFY)
sb_header_cols = st.sidebar.beta_columns(2)
sb_header_cols[0].title("Language")
sb_header_cols[1].title(constants.LANGUAGE)


def display_sidebar_for_category(category: str, title: str):
    category_settings = constants.ANNOTATIONS.get(category)
    st.sidebar.title(title)
    sb_pos_cols = st.sidebar.beta_columns(2)
    for i, (k, v) in enumerate(category_settings.items()):
        colors[k] = sb_pos_cols[i % 2].color_picker(v["name"], v["color"])

    pos_names = [v["name"] for v in category_settings.values()]
    annotated_names = st.sidebar.multiselect(
        f"{category} to annotate", pos_names, default=pos_names
    )

    return colors, annotated_names


# POS
_colors, pos_annotated_names = display_sidebar_for_category("POS", "Parts of speech")
colors.update(_colors)

# CASES
_colors, cases_annotated_names = display_sidebar_for_category(
    "CASES", "Cases and genders"
)
colors.update(_colors)


# Main part - outputs
with st.beta_expander("Parts of speech annotations"):
    list_annotated_text = split_annotated_text(get_annotated_text("POS", text, pos_annotated_names, colors))
    for annotations in list_annotated_text:
        annotated_text(*annotations)

with st.beta_expander("Cases and genders annotations"):
    list_annotated_text = split_annotated_text(get_annotated_text("CASES", text, cases_annotated_names, colors))
    for annotations in list_annotated_text:
        annotated_text(*annotations)

with st.beta_expander("Text tokens table", expanded=False):
    st.dataframe(tokens_df)

with st.beta_expander("Visualise parser", expanded=False):
    visualize_parser(get_doc(text), title=None)
