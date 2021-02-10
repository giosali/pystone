import json
import math
import time

import requests

from .languages import Languages


class DeepL:
    api = "https://www2.deepl.com/jsonrpc"

    def __init__(self, text, source, target, s=None):
        self.text = text
        self.source = source
        self.target = target
        self.s = s

    def deepl(self) -> dict:
        """The central method to the DeepL class that establishes a common
        Session object, sets the language abbreviations for the DeepL API,
        retrieves a response from the DeepL API endpoint, splits the user
        text input into sentences through the DeepL API endpoint, organizes
        output to send to DeepL API endpoint, parses the final response
        from the Reverso API endpoint, and then returns the parsed response."""
        self.s = self.create_session()
        self.set_languages()
        response = self.split_sentences()
        splitted_texts = response["result"]["splitted_texts"][0]
        jobs = self.get_jobs(splitted_texts)
        response = self.get_deepl_translation_response(jobs)
        parsed_response = self.parse_deepl_translation_response(response)
        return parsed_response

    def create_session(self) -> requests.sessions.Session:
        """Creates a Session object."""
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4371.0 Safari/537.36"
        }
        s = requests.Session()
        s.headers.update(headers)
        return s

    def set_languages(self) -> None:
        """Sets appropriate language abbreviations for use for the DeepL API."""
        source = Languages(self.source)
        source_language = source.get_language()
        self.source = source.deepl_get_abbrv(source_language)
        target = Languages(self.target)
        target_language = target.get_language()
        self.target = target.deepl_get_abbrv(target_language)
        return

    def split_sentences(self) -> dict:
        """Intelligently splits user text input into sentences using the
        DeepL API endpoint."""
        payload = {
            "jsonrpc": "2.0",
            "method": "LMT_split_into_sentences",
            "params": {
                "texts": [self.text],
                "lang": {
                    "lang_user_selected": "auto",
                    "user_preferred_langs": []
                }
            }
        }
        payload = json.dumps(payload)
        with self.s.post(self.api, data=payload) as r:
            if r.ok:
                return r.json()
            else:
                r.raise_for_status()

    def get_jobs(self, texts) -> list:
        """Appropriately organizes user text input for data to be sent to
        the DeepL API endpoint."""
        num_texts = len(texts)
        jobs = []
        count = 0
        while count < num_texts:
            job = {
                "kind": "default",
                "raw_en_sentence": "",
                "raw_en_context_before": [],
                "raw_en_context_after": [],
                "preferred_num_beams": 4
            }
            if num_texts == 1:
                job["raw_en_sentence"] = texts[count]
                job["quality"] = "fast"
                jobs.append(job)
            elif num_texts - 1 == count:
                job["raw_en_sentence"] = texts[count]
                job["raw_en_context_before"] = [texts[i]
                                                for i in range(1 + count - 1)]
                job["preferred_num_beams"] = 1
                jobs.append(job)
            else:
                job["raw_en_sentence"] = texts[count]
                job["raw_en_context_before"] = [texts[i]
                                                for i in range(1 + count - 1)]
                job["raw_en_context_after"] = [texts[count + 1]]
                job["preferred_num_beams"] = 1
                jobs.append(job)
            count += 1
        return jobs

    def get_deepl_translation_response(self, jobs) -> dict:
        """Sends user text input to DeepL API endpoint."""
        payload = {
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": jobs,
                "lang": {
                    "user_preferred_langs": [
                        self.target, self.source
                    ],
                    "source_lang_user_selected": "auto",
                    "target_lang": self.target
                },
                "priority": -1,
                "commonJobParams": {},
                "timestamp": math.floor(time.time() * 1000)
            }
        }
        if "DE" not in payload["params"]["lang"]["user_preferred_langs"]:
            payload["params"]["lang"]["user_preferred_langs"].insert(
                0, "DE")
        if len(jobs) > 1:
            payload["params"]["priority"] = 1
        payload = json.dumps(payload)
        with self.s.post(self.api, data=payload) as r:
            if r.ok:
                return r.json()
            else:
                r.raise_for_status()

    def parse_deepl_translation_response(self, response) -> dict:
        """Parses the response from the DeepL API endpoint."""
        translations = response["result"]["translations"]
        if len(translations) > 1:
            postprocessed_sentences = [
                t["beams"][0]["postprocessed_sentence"] for t in translations]
            translation = " ".join(postprocessed_sentences)
            examples = []
        else:
            beams = translations[0]["beams"]
            postprocessed_sentences = [
                beam["postprocessed_sentence"] for beam in beams]
            translation = postprocessed_sentences.pop(0)
            examples = postprocessed_sentences
        info = {
            "translation": translation,
            "examples": examples
        }
        return info
