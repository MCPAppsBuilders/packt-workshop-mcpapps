# Module 05 — Testing & Evaluation

Ce module couvre deux approches complémentaires pour tester un serveur MCP :

| Approche | Objectif | Outil |
|----------|----------|-------|
| **Tests unitaires** | Valider la logique métier des tools, resources et prompts | `pytest` |
| **Tests end-to-end** | Évaluer le serveur MCP dans un scénario agent réaliste | `mcp-eval` ([mcp-eval.ai](https://mcp-eval.ai/)) |

## Structure

```
05-testing-evaluation/
├── pyproject.toml              # Dépendances (pytest, mcpevals, mcp)
├── tests/
│   ├── conftest.py             # Fixtures partagées (client MCP)
│   ├── test_tools.py           # Tests unitaires des tools (add, subtract)
│   ├── test_resources.py       # Tests unitaires des resources
│   └── test_prompts.py         # Tests unitaires des prompts
└── evals/
    ├── mcp-eval.config.json    # Configuration mcp-eval
    └── test_server_eval.py     # Scénarios d'évaluation mcp-eval
```

## Pré-requis

```bash
cd modules/05-testing-evaluation
uv sync
```

## 1. Tests unitaires avec pytest

Les tests importent directement le serveur depuis `modules/02-architecture/mcp-server` et
utilisent le `ClientSession` MCP en in-memory (pas besoin de lancer le serveur).

```bash
uv run pytest tests/ -v
```

### Ce qui est testé

- **Tools** : `add(2, 3) == 5`, `subtract(10, 4) == 6`, cas négatifs, flottants
- **Resources** : lecture de `file://info.txt` et `file://config.json`, validation du contenu
- **Prompts** : le prompt `calculate` génère le texte attendu

## 2. Évaluation end-to-end avec mcp-eval

[mcp-eval](https://mcp-eval.ai/) connecte un agent LLM à votre serveur MCP réel et
vérifie que les tools sont correctement appelés et que les réponses sont pertinentes.

```bash
# Lancer le serveur MCP (dans un autre terminal)
cd ../02-architecture/mcp-server
uv run server.py

# Lancer les évaluations
cd ../../05-testing-evaluation
uv run mcp-eval run evals/
```

### Ce qui est évalué

- L'agent appelle bien le tool `add` quand on lui demande une addition
- L'agent appelle bien le tool `subtract` pour une soustraction
- Les réponses contiennent le résultat numérique correct
- Le temps de réponse reste sous un seuil acceptable
