#!/usr/bin/env python3
"""Preferred Model D entry point — accounting window is end-2021 → end-2025.

Delegates to ``model_from_2021.py`` (Models A–D + artifacts). Kept so older
docs that say ``python scripts/model_d.py`` still work.
"""
from model_from_2021 import main

if __name__ == "__main__":
    main()
