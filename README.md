# Release Note Create

`release-note-create` is a Cursor Agent Skill for producing release notes, changelogs, and version summaries from real git evidence.

The skill treats the current code as `HEAD`, inspects tags, commits, diffs, changed files, and previous release notes, then writes copy-ready Markdown release notes without relying on commit messages alone.

## Features

- Infers release ranges from reachable git tags and `HEAD`.
- Recommends the next patch version when the user does not provide one.
- Verifies release-note bullets against real diffs and changed files.
- Matches the language and style of existing release notes when possible.
- Uses mainstream changelog categories such as features, improvements, fixes, security, testing, and breaking changes.

## Installation

Install as a personal Cursor skill:

```bash
mkdir -p ~/.cursor/skills
git clone https://github.com/<owner>/release-note-create.git ~/.cursor/skills/release-note-create
```

Or copy this directory into a project skill path:

```text
.cursor/skills/release-note-create/
```

## Usage

Ask Cursor for release notes in natural language:

```text
Generate release notes
Write a changelog for v1.2.3
I want to publish v1.2.3, please write release notes
/release-note-create release v1.2.3
```

The skill will stop and ask for clarification when the release range, version jump, previous release note, or git evidence is ambiguous.

## Repository Layout

```text
.
├── release-note-create/
│   └── SKILL.md
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── scripts/
│   └── validate_skill.py
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
```

## Validation

Run the local validation script before publishing changes:

```bash
python3 scripts/validate_skill.py release-note-create/SKILL.md
```

The GitHub Actions workflow runs the same check on pushes and pull requests.

## Contributing

Contributions are welcome. Please read `CONTRIBUTING.md`, keep changes focused, and update `CHANGELOG.md` for user-visible behavior changes.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
