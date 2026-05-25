from app.tools import tarefas


def test_fluxo_tarefas(tmp_path, monkeypatch):
    tarefas_path = tmp_path / "tarefas.json"
    monkeypatch.setattr(tarefas, "TAREFAS_PATH", tarefas_path)

    msg_add = tarefas.adicionar_tarefa("Estudar embeddings", "2026-05-25")
    assert "adicionada com sucesso" in msg_add

    msg_list = tarefas.listar_tarefas()
    assert "Estudar embeddings" in msg_list

    msg_done = tarefas.concluir_tarefa(id_tarefa=1)
    assert "marcada como concluída" in msg_done

    msg_list_after = tarefas.listar_tarefas()
    assert "Concluída" in msg_list_after