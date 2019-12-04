import json
import langdetect
import web

urls = (
    "/", "Detect"
)


class Detect:
    """
    A (very simple) server class that handles requests
    """

    def GET(self):
        """Handle GET requests to the server.

        This method uses the langdetect module to analyze the language of the text.
        The text to analyze has to be passed using the GET parameter "text". The URL queried could be, for example:
        http://localhost:8080/?text=This%20is%20the%20text%20to%20analyze

        :return: Either a dict representing a language, or a list of such dicts if multiple possible languages are
            detected
        """
        out = []
        for lang in langdetect.detect_langs(web.input().text):
            out.append({
                "reliable": lang.prob > 0.9,
                "language": lang.lang,
                "prob": lang.prob
            })

        return json.dumps(out if len(out) > 1 else out[0])


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
