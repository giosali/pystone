import re
import unicodedata

from .constants import LANGUAGES


class Languages:
    def __init__(self, language):
        self.language = self.asciify(language)

    def get_language(self) -> str:
        """Gets lowercase English version of language"""
        if self.language in LANGUAGES:
            return self.language
        else:
            patterns = [
                (r"(^ara\w*)", "arabic"),
                (r"(^ch?i\w*)", "chinese"),
                (r"(^(?:dut|ni?e(?:d|e)?|h?ola?|flem?)\w*)", "dutch"),
                (r"(^(?:e|a|i)ng\w*)", "english"),
                (r"(^fr\w*)", "french"),
                (r"(^(?:al(?:l?e?m?)|dui|ted|nie|ger)\w*)", "german"),
                (r"(^h?(?:i|e)br?\w*)", "hebrew"),
                (r"(^(?:ita|wos)\w*)", "italian"),
                (r"(^(?:j|gi)ap\w*)", "japanese"),
                (r"(^(?:po+l|l(?:us|eh))\w*)", "polish"),
                (r"(^por\w*)", "portuguese"),
                (r"(^r(?:o|u)(?:m|e|u)\w*)", "romanian"),
                (r"(^r(?:u|o)s\w*)", "russian"),
                (r"(^(?:hi|e|i)?sz?p\w*)", "spanish"),
                (r"(^tur\w*)", "turkish"), ]
            for p, l in patterns:
                match = re.search(p, self.language)
                if match:
                    return l

    def deepl_get_abbrv(self, language) -> str:
        """Gets language abbreviation for DeepL"""
        abbrv = LANGUAGES[language]["deepl"]
        return abbrv

    def reverso_get_abbrv(self, language) -> str:
        """Gets language abbreviation for Reverso"""
        abbrv = LANGUAGES[language]["reverso"]
        return abbrv

    def reverso_get_voice_name(self, language) -> str:
        voice_name = LANGUAGES[language]["reverso_voice"]
        return voice_name

    @staticmethod
    def asciify(text) -> str:
        """Remove accent marks from input"""
        text = unicodedata.normalize("NFD", text)
        asciified_text = text.encode("ascii", "ignore").decode("utf-8")
        return asciified_text.lower()
