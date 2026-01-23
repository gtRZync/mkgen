import argparse
from typing import Any, Literal, Sequence

from makefile_generator.config import (
    C_COMPILERS,
    C_STANDARDS,
    CPP_COMPILERS,
    CPP_STANDARDS,
)

#FIXME: make the code better, add compilers/standars(cpp and c) for check when no lang, reduce duplicate...etc
# Normalize these : values.upper()
class LanguageAction(argparse.Action):
    def __call__(self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None
    ) -> None:
        lang = getattr(namespace, 'lang')
        if option_string in {'-std', '--standard'}:
            if not lang:
                if values.upper() not in C_STANDARDS and values.upper() not in CPP_STANDARDS: #type: ignore
                    parser.error(f'Invalid compiler standard: {values!r}')

            if values and lang:
                value = str(values)
                if self.__in_iterable(dest='standard', lang=lang, value=value):
                    setattr(namespace, self.dest, value)
                    return
                else:
                    parser.error(f'Invalid compiler standard: {value!r}')

        elif option_string in {'-c', '--compiler'}:
            if not lang:
                if values not in C_COMPILERS and values not in CPP_COMPILERS: #type: ignore
                    parser.error(f'Invalid compiler: {values!r}')

            if values and lang:
                value = str(values)
                if self.__in_iterable(dest='compiler', lang=lang, value=value):
                    setattr(namespace, self.dest, value)
                    return
                else:
                    parser.error(f'Invalid compiler: {value!r}')

        setattr(namespace, self.dest, values)

    def __in_iterable(self, *, dest: Literal['compiler', 'standard'], lang: str, value: str) -> bool:
        normalized_map = {
            'compiler' : {
                'c' : {s for s in C_COMPILERS},
                'c++' : {s for s in CPP_COMPILERS}
            },
            'standard' : {
                'c' : {s.lower() for s in C_STANDARDS},
                'c++' : {s.lower() for s in CPP_STANDARDS}
            }
        }
        if value.lower() not in normalized_map[dest][lang.lower()]:
            return False
        return True
