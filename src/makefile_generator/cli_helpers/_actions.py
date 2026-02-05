import argparse
from typing import Any, Sequence

from makefile_generator.config import PROFILES


class LanguageAction(argparse.Action):
    def __call__(self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None
    ) -> None:
        lang = getattr(namespace, 'lang')
        if not lang:
            normalized_value = values.lower() #type: ignore
            if normalized_value not in PROFILES['c'][self.dest] and normalized_value not in PROFILES['c++'][self.dest]:
                parser.error(f'Invalid {self.dest[:-1]}: {values!r}')

        if values and lang:
            value = str(values)
            normalized_lang = lang.lower()
            if value.lower() in PROFILES[normalized_lang][self.dest]:
                setattr(namespace, self.dest, value)
                return
            else:
                parser.error(f'Invalid {self.dest[:-1]} {values!r} for {lang.upper()!r}')

        setattr(namespace, self.dest, values)
