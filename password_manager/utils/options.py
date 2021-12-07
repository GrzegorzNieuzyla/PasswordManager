from PyQt5.QtCore import QSettings

from password_manager.utils.password_generator import GenerationOptions


def get_last_file() -> str:
    options = QSettings("PasswordManager", "PasswordManager")
    return options.value("last_file", "", str)


def set_last_file(file: str) -> None:
    options = QSettings("PasswordManager", "PasswordManager")
    options.setValue("last_file", file)
    del options  # save options to file


def set_generation_options(options_: GenerationOptions) -> None:
    options = QSettings("PasswordManager", "PasswordManager")
    options.setValue("uppercase", options_.uppercase)
    options.setValue("special", options_.special)
    options.setValue("lowercase", options_.lowercase)
    options.setValue("numbers", options_.numbers)
    options.setValue("custom", options_.custom)
    options.setValue("length", options_.length)
    del options  # save options to file


def get_generation_options() -> GenerationOptions:
    options = QSettings("PasswordManager", "PasswordManager")
    options_ = GenerationOptions(
        options.value("special", True, bool),
        options.value("numbers", True, bool),
        options.value("uppercase", True, bool),
        options.value("lowercase", True, bool),
        options.value("custom", "", str),
        options.value("length", 25, int))
    return options_
