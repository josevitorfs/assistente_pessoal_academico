from app.llm.client import ask_gemma


def test_gemma():

    resposta = ask_gemma(
        "Diga apenas OK"
    )

    assert "OK" in resposta