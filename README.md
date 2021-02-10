<img src="https://raw.githubusercontent.com/GBS3/pystone/main/media/pystone.png" align="right" width="125">

# pystone

![PyPI Version](https://img.shields.io/pypi/v/pystone?style=flat-square) ![Python Version](https://img.shields.io/pypi/pyversions/pystone?style=flat-square) ![License](https://img.shields.io/pypi/l/pystone?style=flat-square)

A command line tool written in Python for translating text through Reverso.


* [pystone](#pystone)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Command Line Arguments](#command-line-arguments)
    * [Documented Commands](#documented-commands)
      * [settings](#settings)
      * [set](#set)
        * [Flexibility](#flexibility)
      * [translate](#translate)
      * [examples](#examples)
      * [alternatives](#alternatives)
      * [audio](#audio)
      * [reverse](#reverse)
      * [exit](#exit)
      * [help](#help)
      * [deepl](#deepl)
  * [Supported Languages](#supported-languages)
  * [Limits](#limits)

## Requirements

To be able to use `pystone`, you will need at least Python 3.6 or higher. This tool makes use of the [requests](https://github.com/psf/requests) and [playsound](https://github.com/TaylorSMarks/playsound) packages.


## Installation

To install `pystone`, run the following in your terminal:

```
$ pip install pystone
```

## Usage

In order to use `pystone`, simply type and enter it in your terminal:

```
$ pystone
```

This will activate a command line interpreter that mimics a *session* and allows for quick <kbd>tab</kbd> completions, which in turn optimizes ease of use. It will remember your current source and target languages and will allow you to modify them within the same session. If you want to translate a piece of text into a variety of languages, you can do that without having to repeatedly enter the same text and/or command line arguments.

### Command Line Arguments

On that note, I should explain that there are command line arguments that you *can* use but they're completely optional.

Here they are:

```
Translation options

optional arguments:
    -h, --help                                  show this help message and exit
    -s LANGUAGE, --source LANGUAGE              the source language (default: English)
    -t LANGUAGE, --target LANGUAGE              the target language
    --text TEXT                                 the text to be translated
```

Example:

```
pystone --target Spanish
```

I don't expect these commands to be used very often but they're there in case a user preemptively knows which languages they want to translate between or happens to have a specific text in mind.

### Documented Commands

Once the interpreter has been activated, there are several commands that are at your disposal:

```
Documented commands (type help <topic>):
========================================
alternatives  audio  deepl  examples  exit  help  reverse  set  settings  translate
```

#### settings

`settings` accepts no arguments and outputs your current configuration to the console:

```
    Source language: English
    Target language: None
    Current text: None
    Most recent translation: None
```

#### set

`set` accepts at most two space-separated arguments and manages your source and target languages. If only one argument is provided, your target language will be set to that language. If two arguments are provided, both your source language and target language will respectively be set to those languages:

```
(pystone) set Spanish # target language -> Spanish

# ==================
# or
# ==================

(pystone) set German French # source language -> German, target language -> French
```

##### Flexibility

The `set` command is incredibly flexible in that the languages don't need to be specified in English or capitalized and will accept letters with accent marks:

```
(pystone) set Anglais español
```

It will even attempt to determine the languages if you input short abbreviations (*at least 3 characters are recommended for each language*):

```
(pystone) set fra spa # source language -> French, target language -> Spanish
```

#### translate

`translate` accepts text as input and outputs a translation of the text to your target language:

```
(pystone) translate What time is it?

    What time is it?

    ¿Qué hora es?
```

#### examples

`examples` accepts no arguments and either outputs example sentences using your translation (if there are any available) or outputs nothing:

```
(pystone) examples

¿Qué hora es? - Las dos.
¿Qué hora es? son cinco para las diez.
¿Qué hora es? - Las nueve.
¿Qué hora es? - Las tres y media.
¿Qué hora es? Pulse para actualizarla.
¡Dolokhov! ¿Qué hora es?
¿Qué hora es? -Las cuatro.
¿No tiene reloj? - ¿Qué hora es? ...le lanza un puñetazo contundente.
Discúlpeme. ¿Qué hora es?
¿Qué hora es? eh, creo que es, mediodía.
```

#### alternatives

`alternatives` accepts no arguments and either outputs other translations that could be more accurate (if there are any available) or outputs nothing:

```
(pystone) alternatives

¿Qué hora es ahora?
¿QUÉ TIEMPO ES ESTE?
qué hora es!
la hora que es?
¿qué horas son?
```

#### audio

`audio` accepts no arguments and outputs audio of a text-to-speech voice reader reading your translation:

```
(pystone) audio

# 🎶¿Qué hora es?🎶
```

#### reverse

`reverse` accepts no arguments and swaps the languages for the source language and target language with each other:

```
(pystone) reverse

# source language gets set to target language
# target language gets set to source language
```

#### exit

`exit` accepts no arguments and quits the program.

#### help

`help` accepts at most one argument. If no arguments are provided, the available commands will be printed to the console. If an argument is provided and that argument is the name of a command, a short description of the command will be printed to the console:

```
(pystone) help set

Expects 1 or 2 languages separated by spaces as input.
        If one argument is provided, the target language will be
        changed to the specified language. If two arguments are provided,
        both the source language and the target language will
        be changed (in that order).
```

#### deepl

*WARNING: this command is currently in experimental mode and I do **NOT** recommend using it without a VPN or a proxy*. *Once I deem it usable/safe, this warning will be removed but there is still much testing to be done*.

*NOTE: translating **to** English or Portugese is not currently supported.*

`deepl` works like `translate`. It accepts text as input and outputs a translation from DeepL of the text to your target language.


## Supported Languages

A table consisting of the currently supported languages:

| Language   | Reverso | DeepL |
| :------:   | :-----: | :---: |
| Arabic     | ✔ | ❌ |
| Chinese    | ✔ | ✔ |
| Dutch      | ✔ | ✔ |
| English    | ✔ | ✔ |
| French     | ✔ | ✔ |
| German     | ✔ | ✔ |
| Hebrew     | ✔ | ❌ |
| Italian    | ✔ | ✔ |
| Japanese   | ✔ | ✔ |
| Polish     | ✔ | ✔ |
| Portuguese | ✔ | ✔ |
| Romanian   | ✔ | ❌ |
| Russian    | ✔ | ✔ |
| Spanish    | ✔ | ✔ |
| Turkish    | ✔ | ❌ |


## Limits

Reverso only allows text with a maximum of 800 characters. For the audio portion, only around the first 150 characters will be read aloud.