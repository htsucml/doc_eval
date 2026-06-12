"""Print a lightweight environment report for the CPU-safe milestone."""

from __future__ import annotations

import importlib
import platform
import sys


def optional_version(module_name: str) -> str:
    try:
        module = importlib.import_module(module_name)
    except Exception:
        return "not-installed"
    return getattr(module, "__version__", "unknown")


def main() -> None:
    print(f"python={platform.python_version()}")
    print(f"platform={platform.platform()}")
    print(f"executable={sys.executable}")
    print(f"pytest={optional_version('pytest')}")
    print(f"torch={optional_version('torch')}")
    print("device=cpu")
    print("status=ok")


if __name__ == "__main__":
    main()

