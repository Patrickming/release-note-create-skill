---
name: release-note-create
description: Generates release notes, changelogs, version notes, and Markdown summaries from git tags, commits, diffs, and latest repository changes. Use when the user asks to publish a version, write release notes, create a changelog, or summarize release changes.
version: 1.0.0
---

# Release Note Create

Generate copy-ready Markdown release notes from real git evidence. Treat "latest code/current version" as `HEAD`, not as the latest tag, unless the user explicitly asks for a specific tag.

## Trigger Forms

Use this skill for both explicit slash-style calls and natural language release requests, including:

- `/release-note-create release v1.2.3`
- `I want to publish v1.2.3, please write release notes`
- `Generate release notes`
- `Write a changelog`
- `Prepare version notes`

If the user mentions publishing a version or asks for a release log, release note, changelog, or version note, apply this skill even when they do not type the skill name.

## Output Language

- If the user requests a language, use that language.
- Otherwise match the language of the previous release note.
- Otherwise match the dominant language of the repository docs.
- Otherwise default to English.
- Keep code identifiers, file paths, API paths, commands, model names, and symbols unchanged in backticks.

## Project Detection

Do not hardcode the project name. Infer it from the first reliable source:

1. Existing release notes or changelog title.
2. Package metadata such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `.csproj`, or similar.
3. README title.
4. Repository remote name.
5. Ask the user if the name is still ambiguous.

## Workflow

1. Identify the version range:
   - If the user gives explicit `from` / `to` refs, use them.
   - If no tag exists, stop and ask the user which earlier commit or ref should be used as the base.
   - Otherwise first check whether `HEAD` is exactly tagged. Use commit topology, not tag creation date, to choose the range.
   - If `HEAD` is exactly tagged, use the previous reachable tag as `<base>` and the exact tag as `<target>`.
   - If `HEAD` is ahead of the latest reachable tag, use the latest reachable tag as `<base>` and `HEAD` as `<target>`. Do not generate a release note for the latest tag in this case unless the user explicitly asked for that tag.
2. Decide the release version:
   - If the user gives a version, use it as the requested release version after validation.
   - If the user does not give a version, default to patch +1 from the latest reachable SemVer tag. Example: latest tag `v1.2.3` -> target version `v1.2.4`.
   - Preserve the tag prefix style from the latest tag (`v1.2.3` -> `v1.2.4`; `1.2.3` -> `1.2.4`).
   - If the requested version is more than patch +1, analyze whether the diff justifies the jump:
     - Patch jump, such as `v1.2.3` -> `v1.2.7`: usually suspicious unless the user has skipped releases or needs alignment.
     - Minor jump, such as `v1.2.3` -> `v1.3.0`: look for substantial features, user-facing workflow changes, schema changes, or compatibility concerns.
     - Major jump: look for breaking changes or large product/API shifts.
   - For suspicious or large version jumps, explain the recommended version and ask the user to confirm before generating with the requested version.
3. Gather evidence:
   - `git log --oneline --decorate <base>..<target>`
   - `git diff --stat <base>..<target>`
   - `git diff --name-status <base>..<target>`
   - Read the real changed code, not just commit messages. Commit messages are only clues.
   - Inspect diff hunks and relevant source, test, migration, docs, and config files changed in the range before writing any feature bullet.
4. Check whether generation is worthwhile:
   - Count commits in the range.
   - Review `git diff --shortstat <base>..<target>`.
   - If there are fewer than 3 commits, or the shortstat suggests only very small changes, stop and ask the user whether they still want a release note.
5. Find the previous release note for the base tag before writing:
   - Search `CHANGELOG.md`, `RELEASE.md`, `README.md`, `docs/`, GitHub releases, and release note files if they exist.
   - If GitHub CLI is available, check `gh release view <base>`.
   - If the user supplied the previous release note in the conversation, use that as a valid reference.
   - Use the previous release note as the style and structure reference together with the template below.
   - If no previous release note is found, stop and ask whether to proceed with the template only or wait for a reference.
6. Classify changes by user-facing outcome, not by commit order.
7. Produce Markdown using the language decision above and the template below.
8. Call out uncertainty instead of inventing details. Use concise wording and preserve technical names in backticks.

## Evidence Requirements

Do not generate from commit messages alone.

For every major bullet, verify at least one of these:

- A changed source file proves the feature or behavior.
- A test file proves the intended behavior or regression coverage.
- A migration, schema, config, script, or docs change proves upgrade impact.
- A route/controller/service/component diff proves the named API or UI path exists.

Use commit messages only to decide where to look. If a commit claims a feature but the diff does not support it, treat it as uncertain and ask or omit it.

When reviewing the diff:

- Open representative changed files for each claimed feature area.
- Read migrations and schema changes directly.
- Read tests to understand edge cases and user-facing behavior.
- Read docs only as supporting context, not as primary proof.
- Prefer concrete file/API/model names from the diff over generic wording.

## Stop and Ask Rules

Stop before generating and ask or inform the user when:

- No usable tag or base ref can be found.
- The requested release version is a suspicious jump from the latest tag and needs confirmation.
- The range has fewer than 3 commits.
- The diff is too small to justify a full release note, such as only metadata, formatting, comments, or tiny documentation edits.
- Git commands fail, the repository is not available, refs are ambiguous, or the working tree state prevents reliable comparison.
- The previous release note cannot be found.
- The evidence conflicts, for example commits mention a feature but changed files do not support it.
- The agent has only commit messages and has not inspected real changed files.

For any error, do not silently continue. Explain what failed, include the relevant command or missing input, and ask the user how to proceed when a decision is needed.

## Output Rules

- The final release note content must be in one standalone fenced code block with the `markdown` info string.
- Put only the release note Markdown inside that code block. Do not include analysis, caveats, greetings, or follow-up suggestions inside it.
- Any explanation, uncertainty, or question must appear outside the code block, before or after the standalone Markdown block.
- If the user asks for a file-ready result, make the fenced `markdown` block directly copyable as the complete file content.
- Title format: `# <Project Name> <Version>`.
- Use these top-level sections when applicable:
  - `## Highlights`
  - `## New Features`
  - `## Improvements`
  - `## Bug Fixes`
  - `## Deprecated`
  - `## Removed`
  - `## Security`
  - `## Testing`
  - `## Breaking Changes`
  - `## Full Changelog`
- Omit empty sections unless the user explicitly asks to keep them.
- Group large features under `###` headings.
- Bullets should explain product impact first, then implementation evidence.
- Use bold labels at the start of detail bullets when useful, for example `- **API**: ...`.
- Put file names, routes, API paths, commands, models, fields, and symbols in backticks.
- Mention migrations, new APIs, storage changes, behavior changes, and required upgrade commands under `Breaking Changes`.
- The `Full Changelog` section should include commit range, commit count, file count, additions, and deletions when available.
- This template is product release-note oriented. It maps to mainstream changelog categories as: `New Features` = `Added`, `Improvements` = `Changed`, `Bug Fixes` = `Fixed`, plus optional `Deprecated / Removed` and `Security`.
- If the user asks for a strict `CHANGELOG.md`, use Keep a Changelog headings instead: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

## Suggested Commands

Use shell commands only for git and project scripts; prefer file tools for reading files.

```bash
git describe --tags --exact-match HEAD
git describe --tags --abbrev=0 HEAD
git describe --tags --abbrev=0 <exact-target-tag>^
git rev-list --count <base>..<target>
git log --oneline --decorate <base>..<target>
git diff --stat <base>..<target>
git diff --shortstat <base>..<target>
git diff --name-status <base>..<target>
git diff -- <changed-file>
gh release view <base>
```

If project files mention releases, inspect the release note closest to `<base>` before drafting the new one.

Use this decision algorithm when refs are not explicit:

```text
latest_reachable_tag = git describe --tags --abbrev=0 HEAD
exact_head_tag = git describe --tags --exact-match HEAD

if exact_head_tag exists:
  target = exact_head_tag
  base = previous reachable tag before target
else:
  base = latest_reachable_tag
  target = HEAD
  version = patch +1 from latest_reachable_tag unless user supplied a version
```

## Range Decision Examples

- `HEAD` is `v1.2.3`: draft `v1.2.3` from `<previous-tag>..v1.2.3`.
- `HEAD` has commits after `v1.2.3` and the user gives no version: draft `v1.2.4` from `v1.2.3..HEAD`.
- User asks "release `v1.2.4`": draft `v1.2.4` from `v1.2.3..HEAD` when `HEAD` is ahead of `v1.2.3`.
- User asks "release `v1.2.7`" while latest tag is `v1.2.3`: analyze the diff, recommend `v1.2.4` if it looks like a normal patch release, and ask whether to keep `v1.2.7`.
- User asks "release `v1.3.0`" while latest tag is `v1.2.3`: analyze whether the diff contains enough feature or compatibility impact for a minor release, then ask for confirmation if uncertain.
- User asks "generate release note for `v1.2.3`": draft `v1.2.3` from `<previous-tag>..v1.2.3`, even if `HEAD` is newer, and mention that newer commits are excluded.
- User asks "latest/current release note": use `HEAD` as target, not the latest tag, when `HEAD` is ahead.

## Classification Guide

| Section | Put Here |
| --- | --- |
| `New Features` | New user-visible workflows, APIs, pages, models, integrations, import/export capabilities |
| `Improvements` | Performance, UX polish, accessibility, developer experience, refactors with visible benefits |
| `Bug Fixes` | Corrected broken behavior, layout issues, edge cases, failed flows |
| `Deprecated` | Features, APIs, options, or behaviors planned for removal |
| `Removed` | Features, APIs, options, or behaviors removed in this release |
| `Security` | Security fixes, auth changes, sensitive data handling, dependency updates for vulnerabilities |
| `Testing` | New or materially updated tests, e2e coverage, test utilities |
| `Breaking Changes` | Migrations, incompatible schema changes, required commands, storage/layout changes, changed product semantics |

## Markdown Template

```markdown
# <Project Name> <Version>

## Highlights

- Short user-facing summary of the most important change.

## New Features

### Feature Area

- **UI / API / Backend / CLI / Config**: Describe user value and key implementation evidence.
- **Data / Storage / Workflow**: Describe new structures or behavior.

## Improvements

### Improvement Area

- **Component or module**: Describe what improved and why it matters.

## Bug Fixes

- **Module**: Describe the broken behavior and the fixed outcome.

## Deprecated

- **Module**: Describe what is deprecated and the replacement path.

## Removed

- **Module**: Describe what was removed and the replacement path.

## Security

- **Module**: Describe the security-relevant fix or upgrade reason.

## Testing

- **Added / Updated**: Test files or coverage areas.

## Breaking Changes

- **Required upgrade steps**: Commands or manual actions required.
- **Schema / API changes**: Models, fields, endpoints, config, or storage changes.
- **Behavior changes**: Important semantic changes.

## Full Changelog

`<base>...<target>` — **N commits**，**N files changed**，**+N / −N**
```

## Quality Checklist

Before returning the release note:

- Confirm the release note body is isolated in a single copyable `markdown` fenced code block.
- Verify every named feature has evidence in commits or changed files.
- Verify every major bullet against real diff hunks or changed files, not just commit messages.
- Merge duplicate bullets caused by multiple commits touching the same feature.
- Keep wording product-oriented and readable for non-implementers.
- Do not overstate compatibility. If migration or storage behavior changed, list it.
- Include test coverage only when there is evidence.
- If command output is missing or a range is ambiguous, state the gap clearly.
