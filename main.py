import dominate
from dominate.tags import div, h1, h2, h4, img, link, p, style, meta, a, footer, header
from dominate.util import raw
from datetime import datetime

import api

featured = api.get_featured()

doc = dominate.document(title="Cursory", lang="en") # TODO: Change to lang

with doc.head:
    # meta(charset="UTF-8")
    meta(name="viewport", content="width=device-width, initial-scale=1.0")
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
    with div():
        for story in featured["news"]:
            with div(cls="story"):
                # Image
                try:
                    with a(href=story["links"][0]["originalimage"]["source"]):
                        img(
                            src=story["links"][0]["thumbnail"]["source"],
                            cls="image",
                            alt=f"Image for {story['links'][0]['titles']['normalized']}"
                        )
                except KeyError:
                    pass

                # Headline
                h2(story["links"][0]["titles"]["normalized"])
                try:
                    h4(story["links"][0]["description"])
                except KeyError:
                    pass

                # Article
                article = story["story"]
                article = article.replace(
                    '"./', '"https://' + 'en' + ".wikipedia.org/wiki/" # TODO: Change to lang
                )
                p(raw(article))
                p(raw(story["links"][0]["extract_html"]))

    with footer():
        a("Source Code", cls="button", href="https://github.com/j-eo/cursory")
        a("About", cls="button")
        p(raw("<b>Text and images from Wikipedia.</b> " + f"Build time: {datetime.utcnow()} UTC."))
        p(raw("Made with &#10084; by <a href='https://itsjake.me/'>Jake Anto</a>."))

# Create a index.html with the content of the doc
with open("index.html", "w") as f:
    f.write(doc.render())
