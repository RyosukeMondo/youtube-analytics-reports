#!/usr/bin/env python3
"""Add YouTube channel hyperlinks to the HTML report."""

import re
from urllib.parse import quote

# Map of channel names to their channel IDs (from BigQuery)
CHANNEL_IDS = {
    "DAIKOKU FILMS": "UChDlnkBcPipp_nQK-HtS_Tw",
    "TOMOKA and TENZIN": "UCPU0LbRqrhJfmW1PKsQJd7Q",
    "akiのひとりLife": "UCpQqg0BQIW6gqtsYif4IHjA",
    "junの温泉ホテル旅CH": "UC68-FXTol_ihKSe6nYiNKoQ",
    "なつみ / 暮らしのvlog": "UChKYQssp5NgUOpw8EeB6Tsw",
    "はぴりり旅日和": "UCcEe4c9_2IZBwtZzi3XSrQw",
    "旅おじさん": "UC5Vl49FmeU9Bxil0U4BDZng",
    "癒しの旅": "UCnNy9v7tB7Qr5bqLqXqQZ8A",  # Need to verify
    # Large channels for reference
    "くぼたび | 旅に生きるアラサー夫婦": "UCJg80GhmXKOkJdkoX6R2P-w",
    "パワースポット一人旅": "UCtrEHywHaoXNeVaeccF__MA",
    "わた旅": "UCaLPXMxtXyBvjKqMPz1ewrQ",
}

# Channels to link (even if we don't have the exact ID, we'll use search)
CHANNELS_TO_LINK = [
    "旅おじさん",
    "junの温泉ホテル旅CH",
    "癒しの旅",
    "DAIKOKU FILMS",
    "はぴりり旅日和",
    "TOMOKA and TENZIN",
    "なつみ / 暮らしのvlog",
    "akiのひとりLife",
    "ねこ旅",
    "まいのぶいろぐ",
    "かた夫婦",
    "ゆめつづカップル",
    "Lily's Life",
    "SLOW SQUAD INTERNATIONAL",
    "RyuTravel",
    "Kyushu Meshi",
    "きききのくらし",
    "旅するnami",
    "くぼたび | 旅に生きるアラサー夫婦",
    "パワースポット一人旅",
    "わた旅",
]


def get_youtube_url(channel_name: str) -> str:
    """Get YouTube URL for a channel."""
    if channel_name in CHANNEL_IDS:
        # Use direct channel URL if we have the ID
        return f"https://www.youtube.com/channel/{CHANNEL_IDS[channel_name]}"
    else:
        # Use search URL which will likely show the channel
        return f"https://www.youtube.com/results?search_query={quote(channel_name)}"


def add_links_to_html(html_content: str) -> str:
    """Add hyperlinks to channel names in HTML."""
    modified = html_content

    for channel_name in CHANNELS_TO_LINK:
        url = get_youtube_url(channel_name)

        # Pattern 1: <strong>channel_name</strong> (in tables)
        pattern1 = f"<strong>{re.escape(channel_name)}</strong>"
        replacement1 = f'<strong><a href="{url}" target="_blank" class="channel-link">{channel_name}</a></strong>'
        modified = modified.replace(pattern1, replacement1)

        # Pattern 2: <td>channel_name</td> (in plain table cells)
        pattern2 = f"<td>{re.escape(channel_name)}</td>"
        replacement2 = f'<td><a href="{url}" target="_blank" class="channel-link">{channel_name}</a></td>'
        modified = modified.replace(pattern2, replacement2)

    # Add CSS for channel links
    css_addition = """
        .channel-link {
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px dotted #667eea;
            transition: all 0.3s;
        }

        .channel-link:hover {
            color: #764ba2;
            border-bottom: 1px solid #764ba2;
        }

        /* Override link color in tables */
        table .channel-link {
            color: #667eea;
            font-weight: inherit;
        }
"""

    # Insert CSS before closing </style> tag
    modified = modified.replace("</style>", css_addition + "    </style>")

    return modified


def main():
    """Main function to process the HTML file."""
    input_file = "reports/ketobi-complete-analysis.html"

    # Read the HTML file
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Add links
    modified_html = add_links_to_html(html_content)

    # Write back
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(modified_html)

    print(f"✅ Added YouTube channel hyperlinks to {input_file}")
    print(f"📊 Processed {len(CHANNELS_TO_LINK)} channel names")


if __name__ == "__main__":
    main()
