"""Style registry. Each style is a Python module with generate_cover() and generate_card()."""

_REGISTRY = {
    "paper": "styles.paper",
    "mono": "styles.mono",
    "stamp": "styles.stamp",
    "canvas": "styles.canvas",
    "blueprint": "styles.blueprint",
    "kraft": "styles.kraft",
    "block": "styles.block",
    "slab": "styles.slab",
    "slab-a": "styles.slab_a",
    "slab-b": "styles.slab_b",
    "slab-c": "styles.slab_c",
    "verdict": "styles.verdict",
}


def get_style(name: str):
    """Returns the style module by name."""
    if name not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY.keys()))
        raise ValueError(f"Unknown style: '{name}'. Available: {available}")

    import importlib
    return importlib.import_module(_REGISTRY[name])


def list_styles() -> list[str]:
    return sorted(_REGISTRY.keys())
