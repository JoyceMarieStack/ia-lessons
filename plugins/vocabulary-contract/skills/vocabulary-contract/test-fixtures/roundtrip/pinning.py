"""Schema pinning support.

Schema pinning locks a project to a specific base schema version so registry
updates cannot change validation results between runs.
"""


def resolve_schema_pinning(config):
    """Return the pinned version when schema pinning is enabled."""
    pin = config.get("schemaPinning")
    if pin is None:
        return None
    return str(pin)
