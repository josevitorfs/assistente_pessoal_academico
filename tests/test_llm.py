import importlib
from types import SimpleNamespace


def test_ask_gemma_retorna_resposta(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.com")
    monkeypatch.setenv("MODEL_NAME", "google/gemma-3-12b-it")

    from app.llm import client as llm_client
    importlib.reload(llm_client)

    fake_response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="OK"))]
    )

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda **kwargs: fake_response
            )
        )
    )

    monkeypatch.setattr(llm_client, "client", fake_client)

    assert llm_client.ask_gemma("Diga OK") == "OK"


def test_ask_gemma_trata_erro(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.com")
    monkeypatch.setenv("MODEL_NAME", "google/gemma-3-12b-it")

    from app.llm import client as llm_client
    importlib.reload(llm_client)

    def fake_raise(**kwargs):
        raise RuntimeError("falha controlada")

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=fake_raise
            )
        )
    )

    monkeypatch.setattr(llm_client, "client", fake_client)

    resposta = llm_client.ask_gemma("Teste")

    assert "Erro ao acessar LLM" in resposta