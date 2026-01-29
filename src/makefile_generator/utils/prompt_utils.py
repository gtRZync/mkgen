from typing import Any, Dict, Sequence, TypeAlias

import questionary

DEFAULT_STYLE = questionary.Style.from_dict({
    # Prompt
    "question": "bold fg:#89b4fa",
    "instruction": "fg:#6c7086",
    "answer": "bold fg:#a6e3a1",

    # Lists (select / checkbox)
    'pointer': 'fg:#673ab7 bold',
    'highlighted': 'fg:#673ab7 bold',
    "selected": "fg:#a6e3a1",
    "separator": "fg:#6c7086",

    # Validation
    "error": "bold fg:#f38ba8",
})

str_lower: TypeAlias = str

def questionary_select(
    prompt: str,
    choices: Sequence[str | questionary.Choice | Dict[str, Any]],
    choices_upper: bool = True,
    style: questionary.Style | None = DEFAULT_STYLE
) -> str_lower:
    choice:str = questionary.select(
        prompt,
        {c.upper() for c in choices} if choices_upper else choices,
        style=style,
        use_jk_keys=False,
        use_search_filter=True
    ).unsafe_ask()
    return choice.lower()
