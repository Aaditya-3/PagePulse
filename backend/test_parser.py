import pytest

from parser import parse_html, DEFAULT_TITLE, DEFAULT_META_DESCRIPTION


def test_parse_html_happy_path():
    html = """
    <html>
        <head>
            <title>Google</title>
            <meta name="description" content="Search Engine">
        </head>
        <body>
            <h1>Hello</h1>
            <h1>World</h1>

            <img src="a.png">
            <img src="b.png" alt="logo">

            This is a sample webpage for testing.
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] == "Google"
    assert result["meta_description"] == "Search Engine"
    assert result["h1_count"] == 2
    assert result["images_missing_alt"] == 1
    assert result["word_count"] > 0


def test_parse_html_missing_title():
    html = """
    <html>
        <body>
            <h1>Hello</h1>
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] == DEFAULT_TITLE
    assert result["h1_count"] == 1
    assert result["meta_description"] == DEFAULT_META_DESCRIPTION


def test_parse_html_missing_meta_description():
    html = """
    <html>
        <head>
            <title>Example</title>
        </head>

        <body>
            <img src="a.png">
            <img src="b.png">
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] == "Example"
    assert result["meta_description"] == DEFAULT_META_DESCRIPTION
    assert result["images_missing_alt"] == 2