import argparse
import cmd
import logging
import os
import platform

from playsound import playsound

from .deepl import DeepL
from .languages import Languages
from .reverso import Reverso


class Translate:
    def __init__(self, text=None, source=None, target=None, translation=None,
                 examples=None, alternatives=None):
        self.text = text
        self.source = source or "English"
        self.target = target
        self._translation = translation
        self._examples = examples
        self._alternatives = alternatives

    def translate(self) -> None:
        """Gets translation from Reverso."""
        if not self.text:
            return
        reverso = Reverso(self.text, self.source, self.target)
        parsed_response = reverso.reverso()
        self._translation = parsed_response["translation"]
        self._examples = parsed_response["target_examples"]
        self._alternatives = parsed_response["alternatives"]
        return

    def audio(self, text) -> bytes:
        """Gets audio from Reverso."""
        reverso = Reverso(text, self.source, self.target)
        audio = reverso.audio()
        return audio

    def deepl(self) -> None:
        """Gets translation from DeepL."""
        if not self.text:
            return
        deepl = DeepL(self.text, self.source, self.target)
        parsed_response = deepl.deepl()
        self._translation = parsed_response["translation"]
        self._examples = parsed_response["examples"]
        return

    @property
    def translation(self) -> str:
        return self._translation

    @translation.setter
    def translation(self, text) -> None:
        self._translation = text

    @property
    def examples(self) -> list:
        return self._examples

    @examples.setter
    def examples(self, array) -> None:
        self._examples = array

    @property
    def alternatives(self) -> list:
        return self._alternatives

    @alternatives.setter
    def alternatives(self, array) -> None:
        self._alternatives = array


class PyStone(cmd.Cmd):
    intro = "This is \033[38;5;14mpystone\033[0m, a command line interpreter for translation. Type \033[38;5;209mhelp\033[0m or \033[38;5;209m?\033[0m to view available commands."
    prompt = "(pystone) "

    DEBUG_FMT = "%(levelname)s - %(message)s"
    INFO_FMT = "%(message)s"

    def __init__(self, args, translation=None, alternatives=None,
                 examples=None, level=logging.INFO):
        super().__init__()
        self.translate = Translate(args.text, args.source, args.target)
        self.translation = translation
        self.alternatives = alternatives
        self.examples = examples
        # Logger setup:
        self.log = logging.getLogger(__name__)
        self.log.setLevel(level)
        if not self.log.handlers:
            formatter = logging.Formatter(fmt=(
                self.INFO_FMT if level == logging.INFO else self.DEBUG_FMT))
            sh = logging.StreamHandler()
            sh.setLevel(level)
            sh.setFormatter(fmt=formatter)
            self.log.addHandler(sh)

    def do_settings(self, arg) -> None:
        """Outputs the current session configuration to the console."""
        self.log.info(f"""
        Source language: {self.translate.source}
        Target language: {self.translate.target}
        Current text: {self.translate.text}
        Most recent translation: {self.translation}
        """)
        return

    def do_set(self, arg) -> None:
        """Expects 1 or 2 languages separated by spaces as input.
        If one argument is provided, the target language will be
        changed to the specified language. If two arguments are provided,
        both the source language and the target language will
        be changed (in that order)."""
        if not arg:
            return
        args = arg.split()
        num_args = len(args)
        if num_args == 1:
            self.translate.target = args[0].capitalize()
        elif num_args == 2:
            self.translate.source = args[0].capitalize()
            self.translate.target = args[1].capitalize()
        else:
            print("*** Maximum no. args: 2")

    def do_translate(self, arg) -> None:
        """Takes text from the source language to translate and prints
        the translation to the console from Reverso."""
        if not self._check_configuration():
            return
        if not arg and self.translation:
            return self._print_translation()
        self.translate.text = arg if arg else self.translate.text
        self.translate.translate()
        self.translation = self.translate.translation
        self.examples = self.translate.examples
        self.alternatives = self.translate.alternatives
        return self._print_translation()

    def do_examples(self, arg) -> None:
        """Prints examples alongside any translations, if available."""
        if self.examples:
            for e in self.examples:
                new_e = e.replace("<em>", "\033[38;5;39m").replace(
                    "</em>", "\033[0m")
                self.log.info(new_e)
        else:
            return

    def do_alternatives(self, arg) -> None:
        """Prints alternative translations, if available."""
        if self.alternatives:
            for a in self.alternatives:
                self.log.info(f"\033[38;5;141m{a}\033[0m")
        else:
            return

    def do_audio(self, arg) -> None:
        """Inputs a translation into a Reverso text-to-speech voice
        reader."""
        if self.translation:
            audio = self.translate.audio(self.translation)
            with open("pystone_audio.mp3", "wb") as f:
                f.write(audio)
            playsound("pystone_audio.mp3")
            os.unlink("pystone_audio.mp3")
        else:
            return

    def do_reverse(self, arg) -> None:
        """Swaps the source and target languages with each other."""
        self.translate.source, self.translate.target = self.translate.target, self.translate.source
        return

    def do_deepl(self, arg) -> None:
        """Takes text from the source language to translate and prints
        the translation to the console from Reverso."""
        if not self._check_configuration():
            return
        if not arg and self.translation:
            return self._print_translation()
        self.translate.text = arg if arg else self.translate.text
        self.translate.deepl()
        self.translation = self.translate._translation
        self.examples = self.translate._examples
        return self._print_translation()

    def do_exit(self, arg) -> bool:
        """Quits program."""
        return True

    def _check_configuration(self) -> int:
        """Confirms if user has specified both a source language and
        a target language."""
        if not self.translate.source or not self.translate.target:
            self.log.warning(
                "You are missing a \033[38;5;202mtarget language\033[0m. Please check your settings by typing and entering \033[38;5;209msettings\033[0m.")
            return 0
        else:
            return 1

    def _print_translation(self) -> None:
        """Prints current translation."""
        self.log.info(f"""
        {self.translate.text}

        \033[38;5;141m{self.translation}\033[0m
        """)
        return

    def debug(self, message) -> None:
        self.log.debug(message)

    def info(self, message) -> None:
        self.log.info(message)

    def warning(self, message) -> None:
        self.log.warning(message)

    def error(self, message) -> None:
        self.log.error(message)


def main() -> None:
    """Command line arguments configuration."""
    parser = argparse.ArgumentParser(description="Translation options")
    parser.add_argument("-s", "--source", type=str, help="the source language (default: English)",
                        default="English", required=False, metavar="LANGUAGE")
    parser.add_argument("-t", "--target", type=str,
                        help="the target language", required=False, metavar="LANGUAGE")
    parser.add_argument(
        "--text", type=str, help="the text to be translated", required=False, metavar="TEXT")
    if platform.system() == "Windows":
        os.system("color")
    PyStone(parser.parse_args()).cmdloop()


# If ran as a script, act as a command line interpreter for translation:
if __name__ == "__main__":
    main()
