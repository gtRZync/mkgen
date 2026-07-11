import argparse
from pathlib import Path
from typing import Any, Sequence

from makefile_generator.config import PROFILES


class LanguageAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None
    ) -> None:
        language = getattr(namespace, 'language')
        if not language:
            normalized_value = values.lower() #pyright: ignore
            if normalized_value not in PROFILES['c'][self.dest] and normalized_value not in PROFILES['c++'][self.dest]:
                parser.error(f'Invalid {self.dest[:-1]}: {values!r}')

        if values and language:
            value = str(values)
            normalized_lang = language.lower()
            if value.lower() in PROFILES[normalized_lang][self.dest]:
                setattr(namespace, self.dest, value)
                return
            else:
                parser.error(f'Invalid {self.dest[:-1]} {values!r} for {language.upper()!r}')

        setattr(namespace, self.dest, values)


class RootAction(argparse.Action):
    def __call__(
        self, 
        parser: argparse.ArgumentParser, 
        namespace: argparse.Namespace, 
        values: str | Sequence[Any] | None, 
        option_string: str | None = None
        ) -> None:
        if values:
            value = Path(values).resolve() #pyright: ignore
            setattr(namespace, self.dest, value)
            return

        setattr(namespace, self.dest, values)
        
class JobsAction(argparse.Action):
    def __call__(
        self, 
        parser: argparse.ArgumentParser, 
        namespace: argparse.Namespace, 
        values: str | Sequence[Any] | None, 
        option_string: str | None = None
        ) -> None:
        if isinstance(values, str):
            try:
                int(values)
                if int(values) > 0:
                    setattr(namespace, self.dest, values)
                    return
                else:
                    raise ValueError()
            except ValueError:
                parser.error(f'the {option_string!r} option requires a positive integer argument')
        
        setattr(namespace, self.dest, values)
            