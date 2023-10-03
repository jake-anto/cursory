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
    style,
)
from dominate.util import raw

import api
import languages


def build(
    page_type: str = "news",
    lang: str = "en",
    green_club_badge: bool = False,
    minify: bool = True,
) -> None:
    """Build the HTML file for the given language.

    Parameters
    ----------
    page_type : str
        The type of page to build. Can be "news", "about" or "404".
    lang : str
        The language code to build the HTML file for.
    green_club_badge : bool
        Whether or not to show the 512KB Green Club badge.
    minify : bool
        Whether or not to minify the HTML file.

    Returns
    -------
    None
        Just builds the HTML file.
    """
    if page_type == "news":
        print(f"Building {lang}.html")
    else:
        print(f"Building {page_type}.html")

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
            with select(
                onchange="location = this.value;",
                aria_label="Language",
            ):
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
                # Hide the language selector if JavaScript is disabled
                style("select { display: none; }")

                # Language selector for browsers without JavaScript
                with div(cls="lang-selector-nojs"):
                    for language in languages.LANGS:
                        if language != "en":
                            a(
                                languages.LANG_NAMES[language],
                                href=f"/{language}",
                                cls="button",
                            )
                        else:
                            a("🇺🇸 English", href="/", cls="button")

        if page_type == "news":
            if featured is not None:
                with div():
                    for story in featured["news"]:
                        with div(cls="story"):
                            # Image
                            try:
                                with a(
                                    href=api.optimize_image(
                                        story["links"][0]["originalimage"]["source"],
                                        lang,
                                    )
                                ):
                                    img(
                                        src=api.optimize_image(
                                            story["links"][0]["thumbnail"]["source"],
                                            lang,
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

        elif page_type == "about":
            h2("About")
            raw(
                """<p>Cursory is an open-source minimalistic news reader that you can \
                use to read the most essential news from around the globe in 15+ \
                languages. It's powered by Wikipedia.</p>
                <h3>✨ Features</h3>
                <h4>🔒 Privacy-first</h4>
                <p>This website doesn't use ads, trackers, cookies, and analytics. We \
                don't want your data.</p>
                <h4>🚀 Lightning fast</h4>
                <p>Page size is usually under 100KiB (including images!), check for \
                yourself.</p>
                <h4>🌍 Supports 15+ languages</h4>
                <p>All thanks to Wikipedia.</p>"""
            )

        elif page_type == "404":
            h2("404 - Not Found")
            p(
                "This site is under active development. Try changing languages or "
                "check back later."
            )

        with footer():
            a("Source Code", cls="button", href="https://github.com/jake-anto/cursory")
            a("About", cls="button", href="/about")
            p(
                raw(
                    "<b>This page uses text from Wikipedia, which is released under "
                    "<a href='/wp_license.txt'>CC-BY-SA 4.0</a>.</b><br>"
                    + f"Build time: {datetime.utcnow()} UTC."
                )
            )
            if green_club_badge:
                a(
                    img(
                        src="/512kb_green.svg",
                        alt="512KB Club Green Team",
                        loading="lazy",
                        cls="badge",
                    ),
                    href="https://512kb.club/",
                )
            p(raw("Made with &#10084; by <a href='https://itsjake.me/'>Jake Anto</a>."))

    # Create a index.html with the content of the doc
    if page_type == "news":
        if lang == "en":
            filename = "site/index.html"
        else:
            filename = f"site/{lang}/index.html"
    elif page_type == "about":
        filename = "site/about.html"
    elif page_type == "404":
        filename = "site/404.html"

    output = doc.render()

    # Minify HTML
    if minify:
        try:
            # pylint: disable=no-member; minify_html is a valid module
            output = minify_html.minify(code=output, do_not_minify_doctype=True)
        except Exception as e:
            logging.warning("Failed to minify HTML: %s", e)

    # Write the file; use UTF-8
    with open(filename, "w", errors="ignore", encoding="utf-8") as f:
        f.write(output)
