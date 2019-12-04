from client_layout import Ui_mainWindow
from PyQt5.QtWidgets import QMainWindow
import requests


class Controller(QMainWindow):
    """
    The PyQt controller class, responsible for processing GUI events.

    This class subclasses QMainWindow to work with the client_layout.py file (which was created from a .ui file using pyuic5).
    Without subclassing QMainWindow, this class wouldn't have access to the GUI components (such as buttons, input
    fields etc.)
    """

    output = """
    reliable: <strong>{{reliable}}</strong><br>
    language: <strong>{{language}}</strong><br>
    probability: <strong>{{probability}}</strong><br>
    """

    def __init__(self):
        """
        Initialize the controller
        """
        super().__init__()

        self.view = Ui_mainWindow()  # Instantiate the view class
        self.view.setupUi(self)  # Set up the UI

    def check_language(self) -> None:
        """Check the language of the text input.

        This method queries the server (server.py) running on localhost:8080 and passes the text to analyze as a GET
        parameter. The result is then parsed and displayed in the GUI window.
        """

        try:
            resp = requests.get("http://localhost:8080", params={"text": self.view.input.toPlainText()}).json()
        except requests.RequestException:
            self.view.statusbar.showMessage("An error occured while requesting the language data", 5000)
            return

        if isinstance(resp, list):
            output = f"<p>{len(resp)} different possible language detected.</p><br>"

            for lang in resp:
                output += f"""
                    <strong>{'reliable' if lang['reliable'] else 'not reliable'}</strong><br>
                    language: <strong>{lang['language']}</strong><br>
                    probability: <strong>{lang['prob'] * 100:.2f} %</strong><br><br>
                    """

        elif isinstance(resp, dict):
            output = f"""
                <strong>{'reliable' if resp['reliable'] else 'not reliable'}</strong><br>
                language: <strong>{resp['language']}</strong><br>
                probability: <strong>{resp['prob'] * 100:.2f} %</strong><br>
                """
        else:
            raise TypeError(f"Object returned by requests.get().json() should be a dict or a list, was a {type(resp)}")

        self.view.output.setHtml(output)
