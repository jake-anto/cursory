from datetime import datetime

import dominate
from dominate.tags import (a, div, footer, h1, h2, h4, header, img, link, meta,
                           option, p, select, style)
from dominate.util import raw

import api
import languages


def build(lang="en") -> None:
    """Build the HTML file for the given language."""
    featured = api.get_featured(lang=lang)

    doc = dominate.document(title="Cursory", lang=lang)

    with doc.head:
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        meta(name="charset", content="UTF-8")
        meta(name="description", content="Cursory: a sleek and speedy app that delivers the most essential news from around the globe in 15+ languages. It's powered by Wikipedia and is open-source.")
        link(
            rel="stylesheet",
            href="https://cdn.simplecss.org/simple.min.css",
        )
        link(
            rel="stylesheet",
            href="/style.css"
        )

    with doc:
        with header():
            h1("Cursory")
            p("A cursory glance at current events.")
            # Language selector
            with select(onchange="location = this.value;"):
                # English redirects to index.html rather than en.html
                option("🇺🇸 English", value="/")
                for language in languages.LANGS:
                    if language != "en":
                        option(
                            languages.LANG_NAMES[language],
                            value=f"/{language}",
                            selected=language == lang,
                        )

        if featured is not None:
            with div():
                for story in featured["news"]:
                    with div(cls="story"):
                        # Image
                        try:
                            with a(href=story["links"][0]["originalimage"]["source"]):
                                img(
                                    src=api.optimize_image(
                                        story["links"][0]["thumbnail"]["source"], lang),
                                    cls="image",
                                    alt=f"Image for {story['links'][0]['titles']['normalized']}",
                                )
                        except KeyError:
                            pass

                        # Headline
                        try:
                            h2(story["links"][0]["titles"]["normalized"])
                        except IndexError:
                            pass

                        # Subtitle
                        try:
                            h4(story["links"][0]["description"])
                        except (KeyError, IndexError):
                            pass

                        # Article
                        article = story["story"]
                        article = article.replace(
                            '"./', '"https://' + lang + ".wikipedia.org/wiki/"
                        )
                        p(raw(article))
                        try:
                            p(raw(story["links"][0]["extract_html"]))
                            a("Continue reading...",
                              href=story["links"][0]["content_urls"]["desktop"]["page"])
                        except (KeyError, IndexError):
                            pass
        else:
            p("There was an error fetching the news. Please try again later.")

        with footer():
            a("Source Code", cls="button", href="https://github.com/j-eo/cursory")
            a("About", cls="button")
            p(
                raw(
                    "<b>Text and images from Wikipedia.</b> "
                    + f"Build time: {datetime.utcnow()} UTC."
                )
            )
            p(raw("Made with &#10084; by <a href='https://itsjake.me/'>Jake Anto</a>."))

    # Create a index.html with the content of the doc
    print(f"Building {lang}.html")

    if lang == "en":
        filename = "site/index.html"
    else:
        filename = f"site/{lang}/index.html"

    # Write the file; use UTF-8
    with open(filename, "w", errors="ignore", encoding="utf-8") as f:
        f.write(doc.render())
