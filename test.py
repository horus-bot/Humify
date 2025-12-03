# python
import types
import pytest
from third_layer import human_imperfection_layer
import third_layer

def test_returns_stripped_text(monkeypatch):
    # Arrange: fake response with surrounding whitespace
    fake_response = types.SimpleNamespace(text="  enhanced text  ")
    def fake_generate_content(model, contents, config):
        return fake_response
    monkeypatch.setattr(third_layer.client.models, "generate_content", fake_generate_content)

    # Act
    result = human_imperfection_layer("input text", {"foo": "bar"})

    # Assert
    assert result == "enhanced text"

def test_passes_prompt_and_config(monkeypatch):
    captured = {}
    def fake_generate_content(model, contents, config):
        captured['model'] = model
        captured['contents'] = contents
        captured['config'] = config
        return types.SimpleNamespace(text="ok")
    monkeypatch.setattr(third_layer.client.models, "generate_content", fake_generate_content)

    sample_text = "Please tweak this."
    sample_analysis = {"key_facts": ["A"], "forbidden_changes": []}

    result = human_imperfection_layer(sample_text, sample_analysis)

    # Verify return value from fake response
    assert result == "ok"

    # Verify model and config used
    assert captured['model'] == "gemini-2.0-flash"
    assert isinstance(captured['config'], dict)
    assert captured['config'].get("temperature") == 0.7

    # Verify prompt contents include the analysis and the text to enhance
    contents = captured['contents']
    assert "Text to enhance:" in contents
    assert sample_text in contents
    # analysis dict should appear in the prompt (as its Python repr)
    assert "key_facts" in contents or "forbidden_changes" in contents

def test_handles_empty_response_text(monkeypatch):
    fake_response = types.SimpleNamespace(text="")
    def fake_generate_content(model, contents, config):
        return fake_response
    monkeypatch.setattr(third_layer.client.models, "generate_content", fake_generate_content)

    result = human_imperfection_layer("anything", {})
    assert result == ""