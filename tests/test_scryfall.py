from unittest.mock import patch

from mcp_server.scryfall import format_scryfall_cards, get_cards


def test_format_scryfall_cards_single_card():
    cards = [{
        "name": "Lightning Bolt",
        "oracle_text": "Lightning Bolt deals 3 damage to any target.",
        "mana_cost": "{R}",
        "colors": ["R"],
        "color_identity": ["R"],
        "type_line": "Instant",
        "power": None,
        "toughness": None,
        "rarity": "common",
        "set_name": "Magic 2010",
        "prices": {
            "usd": "1.00",
            "eur": "0.85",
            "usd_foil": "3.00",
            "eur_foil": "2.50",
        }
    }]
    output = format_scryfall_cards(cards)

    assert "Lightning Bolt" in output
    assert "Mana Cost: {R}" in output
    assert "Type: Instant" in output
    assert "Price USD: 1.00" in output
    assert "Foil version Price EUR: 2.50" in output


def test_format_scryfall_cards_empty_prices():
    cards = [{
        "name": "Nameless Card",
        "oracle_text": None,
        "mana_cost": None,
        "colors": None,
        "color_identity": None,
        "type_line": None,
        "power": None,
        "toughness": None,
        "rarity": None,
        "set_name": None,
        "prices": None,
    }]
    output = format_scryfall_cards(cards)

    assert "Nameless Card" in output
    assert "Price USD: N/A" in output


@patch("mcp_server.scryfall.make_request")
def test_get_cards_query_building(mock_make_request):
    get_cards(card_name="Shock", card_color="r", card_type="instant", card_text="damage")
    args = mock_make_request.call_args[0][0]

    assert "name%3A%22Shock%22" in args  # name:"Shock"
    assert "c%3Ar" in args              # c:r
    assert "t%3Ainstant" in args        # t:instant
    assert "o%3A%22damage%22" in args   # o:"damage"


@patch("mcp_server.scryfall.make_request")
def test_get_cards_no_query(mock_make_request):
    result = get_cards()
    assert result.startswith("Error:")
    mock_make_request.assert_not_called()
