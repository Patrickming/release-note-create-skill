# Contributing

Thank you for considering a contribution to `release-note-create`.

## Development Workflow

1. Open an issue for behavior changes, unclear requirements, or larger improvements.
2. Keep pull requests focused on one user-visible change or one maintenance task.
3. Update `release-note-create/SKILL.md` when the skill behavior changes.
4. Update `README.md` and `CHANGELOG.md` when users need to know about the change.
5. Run validation before submitting:

```bash
python3 scripts/validate_skill.py release-note-create/SKILL.md
```

## Skill Authoring Guidelines

- Keep `release-note-create/SKILL.md` concise and under 500 lines when possible.
- Make the `description` specific and written in third person.
- Include both what the skill does and when Cursor should apply it.
- Prefer evidence-based instructions over vague advice.
- Avoid time-sensitive wording that will become stale.
- Keep referenced files one level deep from `release-note-create/SKILL.md`.

## Commit Messages

Use concise, conventional-style commit messages when practical:

```text
feat: add release note skill
docs: clarify installation steps
ci: validate skill metadata
fix: tighten release range rules
```

## Community Standards

By participating, you agree to follow `CODE_OF_CONDUCT.md`.

Do not report security vulnerabilities in public issues. Follow `SECURITY.md` instead.
