import requests
import sys

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("scryfall")

# Constants
API_BASE = "https://api.scryfall.com"
USER_AGENT = "MTG-mcp-app/1.0"


def make_request(url):
    """Make a GET request

    Args:
        url: URL for the request
    """
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"
    return format_scryfall_response(response)


def format_scryfall_response(response):
    """Format a scryfall response into a GPT readable string

    Args:
        response: request response
    """
    result = response.json()

    if result.get("object") == "error":
        return f"Error: {result.get('details')}"

    if "data" not in result:
        return "No data found in response"

    cards = []
    for card in result["data"]:

        card_info = f"""
{card['name']}:
Text: {card.get('oracle_text', 'N/A')}
Mana Cost: {card.get('mana_cost', 'N/A')}
Colors: {card.get('colors', 'N/A')}
Color Identity: {card.get('color_identity', 'N/A')}
Type: {card.get('type_line', 'N/A')}
Power: {card.get('power', 'N/A')}
Thoughness: {card.get('toughness', 'N/A')}
Rarity: {card.get('rarity', 'N/A')}
From the set: {card.get('set_name', 'N/A')}
Price USD: {card.get("prices").get("usd")}
Price EUR: {card.get("prices").get("eur")}
Foil version Price USD: {card.get("prices").get("usd_foil")}
Foil version Price EUR: {card.get("prices").get("eur_foil")}
"""
        cards.append(card_info)

    return "\n---\n".join(cards)


@mcp.tool()
def get_cards(card_name=None, card_color=None, card_type=None, card_text=None):
    """Get info about magic the gathering cards on scryfall by name.

    Args:
        card_name: Card name
        card_color: Color or colors of the card (w="white", u="blue", r="red", g="green", b="black", c="colorless")
        card_type: Type for the card to search
        card_text: Text on the textbox for the card to search
    """
    url = f"{API_BASE}/cards/search"
    query_parts = []

    if card_name:
        query_parts.append(f"name:\"{card_name}\"")
    if card_color:
        query_parts.append(f"c:{card_color}")
    if card_type:
        query_parts.append(f"t:{card_type}")
    if card_text:
        query_parts.append(f"o:\"{card_text}\"")

    if not query_parts:
        return "Error: No search parameters provided"

    query_string = " AND ".join(query_parts)

    encoded_query = requests.utils.quote(query_string)
    full_url = f"{url}?q={encoded_query}"

    return make_request(full_url)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(get_cards(card_name=sys.argv[1]))
    else:
        print("mcp server started")
        mcp.run(transport='stdio')
