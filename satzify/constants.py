WHAT_IS_SATZIFY = (
    "Satzify is a simple tool to help with analysing sentences in a given language. "
    "It helps with visualising and highlighting the different parts "
    "of a sentence according to the selected categories and parts to annotate. "
    "Initially and predominantly it has been created to be used for German, and that's where the name is derived from. "
)

LANGUAGE = "🇩🇪"

SPACY_MODEL = "de_core_news_sm"

EXAMPLE_TEXT = "Besser ein Spatz in der Hand, als eine Taube auf dem Dach."

POS = dict(
    NOUN=dict(name="Noun", color="#afa"),
    PRON=dict(name="Pronoun", color="#fea"),
    VERB=dict(name="Verb", color="#8ef"),
    ADJ=dict(name="Adjective", color="#faa"),
    ADV=dict(name="Adverb", color="#d94"),
    ADP=dict(name="Adposition", color="#ccc"),
)

CASES = dict(
    NOM=dict(name="Nominativ", color="#afa"),
    ACC=dict(name="Akkusativ", color="#fea"),
    DAT=dict(name="Dativ", color="#8ef"),
    GEN=dict(name="Genetiv", color="#faa"),
)

ANNOTATIONS = dict(POS=POS, CASES=CASES)
