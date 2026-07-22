from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KANON = ROOT / "kanon"


def read(doc_id: str) -> str:
    return (KANON / f"{doc_id}.md").read_text(encoding="utf-8")


def test_frame_is_connected_across_norm_mechanism_index_and_process() -> None:
    s003 = read("S003")
    m043 = read("M043")
    i006 = read("I006")
    p008 = read("P008")

    assert "ukrytego założenia pytania" in s003
    assert "zawłaszczenie ramy interpretacyjnej" in m043.lower()
    assert "FRAME" in i006
    assert "FRAME / narzucona rama" in p008


def test_frame_subtypes_are_defined_and_routed() -> None:
    i006 = read("I006")
    p008 = read("P008")
    expected = {
        "ZAŁOŻENIE",
        "ETYKIETA",
        "MOTYW",
        "WINA",
        "PRESJA",
        "FAŁSZYWA_ALTERNATYWA",
        "MORALIZACJA",
    }

    for subtype in expected:
        assert subtype in i006
        assert subtype.lower().replace("_", " ") in p008.lower().replace("_", " ")


def test_frame_composite_result_is_not_an_eighth_subtype() -> None:
    m043 = read("M043")
    i006 = read("I006")
    p008 = read("P008")

    subtype_section = i006.split("## Podtypy FRAME", 1)[1].split("## Wynik złożony FRAME", 1)[0]
    assert "ZAWŁASZCZENIE_RAMY" not in subtype_section
    assert "wynik, nie podtyp" in i006
    assert "Jest skutkiem funkcjonalnym całej wypowiedzi" in m043
    assert "ocenić osobno wynik `ZAWŁASZCZENIE_RAMY`" in p008


def test_frame_does_not_automatically_mean_false_or_manipulative() -> None:
    m043 = read("M043")
    i006 = read("I006")
    p008 = read("P008")

    assert "nie rozstrzyga jeszcze, że rama jest fałszywa" in i006
    assert "nie oznacza automatycznie manipulacji ani fałszu" in p008
    assert "Rama może być uzasadniona" in m043
