from __future__ import annotations

import pytest

from scripts.eval_model import load_adapter


def test_real_model_requires_explicit_gate() -> None:
    with pytest.raises(RuntimeError, match="gated"):
        load_adapter("smolvlm_500m", allow_real_models=False, runtime={"device": "cpu"})
