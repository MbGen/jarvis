import google.auth.exceptions
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleApp:
    """
    This class represents google base class for apps
    """
    required_scopes = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'scope') or not hasattr(cls, 'endpoint'):
            raise TypeError("Derived classes must have 'scope' and 'endpoint' attributes")
        cls.required_scopes.extend([cls.scope])

    def __init__(self, path_to_client_secret_json: str, save_token_to_file: str = 'token.json'):
        self.path_to_client_secret = path_to_client_secret_json
        self.token_file = save_token_to_file
        self.scopes = GoogleApp.required_scopes
        self.credentials = None

    def _write_token_file(self) -> None:
        with open(self.token_file, 'w') as file:
            file.write(self.credentials.to_json())

    def _credential_not_valid_or_expired(self) -> bool:
        if not self.credentials:
            return True

        try:
            return self.credentials.expired or not self.credentials.valid
        except google.auth.exceptions.DefaultCredentialsError:
            return True

    def _is_authenticated(self):
        return not self._credential_not_valid_or_expired()

    def _auth(self) -> None:
        flow = InstalledAppFlow.from_client_secrets_file(self.path_to_client_secret, self.scopes)
        self.credentials = flow.run_local_server(host="127.0.0.1", port=55777, open_browser=False)

    def auth(self) -> None:
        if os.path.exists(self.token_file):
            self.credentials = Credentials.from_authorized_user_file(self.token_file, scopes=self.scopes)
            return

        if self._credential_not_valid_or_expired():
            self._auth()
            self._write_token_file()


class GoogleMail(GoogleApp):
    endpoint = "https://keep.googleapis.com"
    scope = "https://www.googleapis.com/auth/keep"

    def __init__(self, path_to_client_secret_json: str, save_token_to_file: str = 'token.json'):
        super().__init__(path_to_client_secret_json, save_token_to_file)
        self.service = build('mail', 'v2')

    def get_my_notes(self):
        with self.service as service:
            return service.notes()