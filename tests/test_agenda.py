import json
from app.tools import agenda


def test_consultar_agenda_com_filtro(tmp_path, monkeypatch):
    agenda_path = tmp_path / "agenda.json"
    agenda_path.write_text(
        json.dumps(
            [
                {
                    "data": "2026-05-24",
                    "tipo": "prova",
                    "descricao": "Prova de IA",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(agenda, "AGENDA_PATH", agenda_path)

    resposta = agenda.consultar_agenda("2026-05-24")

    assert "Prova de IA" in resposta
    assert "2026-05-24" in resposta