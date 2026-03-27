"""Style registry. Each style is a Python module with generate_cover() and generate_card()."""


def get_style(name: str):
    """Returns the style module by name."""
    if name == "paper":
        from styles import paper
        return paper
    raise ValueError(f"Unknown style: '{name}'. Available: paper")


def list_styles() -> list[str]:
    return ["paper"]
