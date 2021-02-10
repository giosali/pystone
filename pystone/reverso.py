import base64
import json

import requests

from .languages import Languages


class Reverso:
    api = "https://api.reverso.net/translate/v1/translation"
    voice_url = "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName={}?inputText={}"

    def __init__(self, text, source, target, s=None):
        self.text = text
        self.source = source
        self.target = target
        self.s = s

    def reverso(self) -> dict:
        """The central method to the Reverso class that establishes a common
        Session object, sets the language abbreviations for the Reverso API,
        retrieves a response from the Reverso API endpoint, parses the
        response from the Reverso API endpoint, and then returns the parsed
        response."""
        self.s = self.create_session()
        self.set_languages()
        response = self.get_reverso_translation_response()
        parsed_response = self.parse_reverso_translation_response(response)
        return parsed_response

    def create_session(self) -> requests.sessions.Session:
        """Creates a Session object."""
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/json; charset=utf-8",
            "host": "api.reverso.net",
            "origin": "https://www.reverso.net",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4371.0 Safari/537.36"
        }
        s = requests.Session()
        s.headers.update(headers)
        return s

    def set_languages(self) -> None:
        """Sets appropriate language abbreviations for use for the Reverso API."""
        source = Languages(self.source)
        source_language = source.get_language()
        self.source = source.reverso_get_abbrv(source_language)
        target = Languages(self.target)
        target_language = target.get_language()
        self.target = target.reverso_get_abbrv(target_language)
        return

    def get_reverso_translation_response(self) -> dict:
        """Sends source text to the Reverso API endpoint."""
        payload = {
            "input": self.text,
            "from": self.source,
            "to": self.target,
            "format": "text",
            "options": {
                "origin": "reversodesktop",
                "sentenceSplitter": True,
                "contextResults": True,
                "languageDetection": False
            }
        }
        payload = json.dumps(payload)
        with self.s.post(self.api, data=payload) as r:
            if r.ok:
                return r.json()
            else:
                r.raise_for_status()

    def parse_reverso_translation_response(self, response) -> dict:
        """Parses the response from the Reverso API endpoint."""
        input_ = response["input"]
        context_results = response["contextResults"]
        if context_results:
            results = context_results["results"]
            if len(results) == 1:
                translation = response["translation"]
                alternatives = None
            else:
                translations = [result["translation"] for result in results]
                translation = [translations.pop(0)]
                alternatives = translations
            source_examples = results[0]["sourceExamples"]
            target_examples = results[0]["targetExamples"]
        else:
            translation = response["translation"]
            source_examples, target_examples, alternatives = None, None, None
        input_text = " ".join(input_)
        translation_text = " ".join(translation)
        info = {
            "input": input_text,
            "translation": translation_text,
            "source_examples": source_examples,
            "target_examples": target_examples,
            "alternatives": alternatives
        }
        return info

    def audio(self):
        self.s = self.create_session()
        self.update_session_audio()
        voice_name = self.get_reverso_voice()
        input_text = self.base64_translation()
        content = self.get_reverso_translation_audio(voice_name, input_text)
        return content

    def update_session_audio(self) -> None:
        audio_headers = {
            "accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5",
            "host": "voice.reverso.net"
        }
        self.s.headers.update(audio_headers)
        return

    def base64_translation(self) -> str:
        encoded_text = self.text.encode()
        b64_encoded_translation = base64.b64encode(encoded_text)
        b64_decoded_translation = b64_encoded_translation.decode()
        return b64_decoded_translation

    def get_reverso_voice(self) -> str:
        target = Languages(self.target)
        target_language = target.get_language()
        voice_name = target.reverso_get_voice_name(target_language)
        return voice_name

    def get_reverso_translation_audio(self, voice, text) -> bytes:
        with self.s.get(self.voice_url.format(voice, text)) as r:
            if r.ok:
                return r.content
            else:
                r.raise_for_status()
