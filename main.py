from datetime import datetime

import dominate
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
    option,
    p,
    select,
    style,
)
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
        link(
            rel="stylesheet",
            href="https://cdn.simplecss.org/simple.min.css",
        )
        style(
            """
                h2 {
                    margin-bottom: 0;
                }

                h4 {
                    margin-top: 0;
                }

                .image {
                    width: 200px;
                    max-height: 300px;
                    float: right;
                    overflow: hidden;
                    margin: 10px;
                }

                @media only screen and (max-width: 600px) {
                    .image {
                        float: none;
                        margin: 0 auto;
                        display: block;
                        width: auto;
                    }
                }
            """
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
                            value=f"{language}",
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
                                    src=story["links"][0]["thumbnail"]["source"],
                                    cls="image",
                                    alt=f"Image for {story['links'][0]['titles']['normalized']}",
                                )
                        except Exception:
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
        filename = "index.html"
    else:
        filename = f"{lang}.html"

    # Write the file; use UTF-8
    with open(filename, "w", errors="ignore", encoding="utf-8") as f:
        f.write(doc.render())
