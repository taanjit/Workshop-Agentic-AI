# Industrial Git Workflow & Branching Standards

> **Target Standard:** GitHub Flow & Conventional Commits (v1.0.0)  
> **Audience:** AI Engineers & Collaborators

---

## 1. Branch Strategy: GitHub Flow

In production engineering, the `main` branch is **protected**. Direct pushes to `main` are disabled in team settings. All code enters via **Feature Branches** and **Pull Requests (PRs)**.

```
main (protected) ──────────●──────────────────────────────●─────►
                           \                             /
feature/add-rag-tool        ●─────────●────────●────────● (Pull Request + Review)
```

### Branch Naming Conventions

Always prefix branch names with their functional intent:
- `feature/<name>` or `feat/<name>`: New capabilities or tools (e.g. `feat/leave-calculator-tool`).
- `fix/<name>`: Bug fixes (e.g. `fix/pii-phone-regex`).
- `docs/<name>`: Documentation and guide updates (e.g. `docs/api-spec`).
- `chore/<name>`: Maintenance, dependency updates (e.g. `chore/update-langchain`).
- `step-XX-<name>`: Workshop milestone checkpoints (e.g. `step-04-git-industrial-workflow`).

---

## 2. Conventional Commit Standards

Every commit message must follow the structured format:
```
<type>(<scope>): <short imperative description>

[optional body explaining WHY this change was made]
```

### Approved Commit Types

| Type | When to Use | Example |
|:---:|---|---|
| `feat` | Adding new features, tools, or models | `feat(agent): implement human-in-the-loop approval prompt` |
| `fix` | Resolving bugs or incorrect behaviors | `fix(guardrail): escape special regex characters in email filter` |
| `docs` | Modifying markdown documentation or guides | `docs(readme): add step navigation table for students` |
| `chore` | Scaffolding, dependency changes, git configs | `chore(pre-commit): add gitleaks security hook` |
| `test` | Adding or updating unit tests and golden sets | `test(eval): add 4 golden test cases for HR policies` |

---

## 3. Pull Request (PR) Checklist Before Merging

Before merging any code to production:
1. ✅ **All Pre-Commit Hooks Passed:** Zero secrets detected by Gitleaks.
2. ✅ **Automated Tests Passed:** `pytest -m "not slow"` executed with 0 failures.
3. ✅ **No Committed `.env`:** Verified using `git status` and `git check-ignore`.
4. ✅ **Peer Review Approved:** At least one senior engineer has approved the architectural diff.
