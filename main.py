import logging
from datetime import datetime

import dominate
import minify_html
from dominate.tags import (
    a,
    div,
    footer,
    h1,
    h2,
    h4,
    header,
    img,
    link,
    meta,
    noscript,
    option,
    p,
    select,
)
from dominate.util import raw

import api
import languages


def build(
    lang: str = "en", green_club_badge: bool = False, minify: bool = True
) -> None:
    """Build the HTML file for the given language.

    Parameters
    ----------
    lang : str
        The language code to build the HTML file for.
    green_club_badge : bool
        Whether or not to show the 512KB Green Club badge.

    Returns
    -------
    None
        Just builds the HTML file.
    """
    print(f"Building {lang}.html")

    featured = api.get_featured(lang=lang)

    doc = dominate.document(
        title=f"Cursory - {languages.LANG_NAMES[lang]} edition", lang=lang
    )

    with doc.head:
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        meta(name="charset", content="UTF-8")
        meta(
            name="description",
            content="A lightweight and minimalistic open-source app that delivers "
            "the most essential news from around the globe in 15+ languages. "
            "Powered by Wikipedia.",
        )
        link(
            rel="stylesheet",
            href="/simple.css",
        )
        link(rel="stylesheet", href="/style.css")
        link(rel="icon", type="image/png", sizes="32x32", href="/favicon-32.png")
        link(rel="icon", type="image/png", sizes="16x16", href="/favicon-16.png")

    with doc:
        with header():
            h1("Cursory")
            p("A cursory glance at current events.")
            # Language selector
            with select(onchange="location = this.value;", aria_label="Language"):
                # English redirects to index.html rather than en.html
                option("🇺🇸 English", value="/")
                for language in languages.LANGS:
                    if language != "en":
                        option(
                            languages.LANG_NAMES[language],
                            value=f"/{language}",
                            selected=language == lang,
                        )
            with noscript():
                for language in languages.LANGS:
                    if language != "en":
                        a(
                            languages.LANG_NAMES[language],
                            href=f"/{language}",
                            cls="button lang-button",
                        )
                    else:
                        a("🇺🇸 English", href="/", cls="button")

        if featured is not None:
            with div():
                for story in featured["news"]:
                    with div(cls="story"):
                        # Image
                        try:
                            with a(
                                href=api.optimize_image(
                                    story["links"][0]["originalimage"]["source"], lang
                                )
                            ):
                                img(
                                    src=api.optimize_image(
                                        story["links"][0]["thumbnail"]["source"], lang
                                    ),
                                    cls="image",
                                    alt=f"Image for {story['links'][0]['titles']['normalized']}",
                                )
                        except KeyError:
                            logging.warning(
                                "No image found for a story in %s.html.", lang
                            )

                        # Headline
                        try:
                            h2(story["links"][0]["titles"]["normalized"])
                        except IndexError:
                            logging.warning(
                                "No headline found for a story in %s.html.", lang
                            )

                        # Subtitle
                        try:
                            h4(story["links"][0]["description"])
                        except (KeyError, IndexError):
                            logging.warning(
                                "No subtitle found for a story in %s.html.", lang
                            )

                        # Article
                        article = story["story"]
                        article = article.replace(
                            '"./', '"https://' + lang + ".wikipedia.org/wiki/"
                        )
                        p(raw(article))
                        try:
                            p(raw(story["links"][0]["extract_html"]))
                            a(
                                "Continue reading...",
                                href=story["links"][0]["content_urls"]["desktop"][
                                    "page"
                                ],
                            )
                        except (KeyError, IndexError):
                            logging.warning(
                                "No article found for a story in %s.html.", lang
                            )
        else:
            p("There was an error fetching the news. Please try again later.")

        with footer():
            a("Source Code", cls="button", href="https://github.com/jake-anto/cursory")
            a("About", cls="button", href="/about")
            p(
                raw(
                    "<b>Text and images from Wikipedia.</b> "
                    + f"Build time: {datetime.utcnow()} UTC."
                )
            )
            if green_club_badge:
                a(
                    img(
                        src="/512kb_green.svg",
                        alt="512KB Club Green Team",
                        loading="lazy",
                    ),
                    href="https://512kb.club/",
                    cls="badge",
                )
            p(raw("Made with &#10084; by <a href='https://itsjake.me/'>Jake Anto</a>."))

    # Create a index.html with the content of the doc
    if lang == "en":
        filename = "site/index.html"
    else:
        filename = f"site/{lang}/index.html"

    output = doc.render()

    # Minify HTML
    if minify:
        try:
            output = minify_html.minify(code=output, do_not_minify_doctype=True)
        except Exception as e:
            logging.warning("Failed to minify HTML: %s", e)

    # Write the file; use UTF-8
    with open(filename, "w", errors="ignore", encoding="utf-8") as f:
        f.write(output)
