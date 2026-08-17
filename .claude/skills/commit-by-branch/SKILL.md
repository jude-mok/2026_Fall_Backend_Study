---
name: commit-by-branch
description: Enforce this repository's branch-aware English Git commit convention. Use whenever an agent prepares, suggests, creates, amends, rebases, squashes, or validates a commit message in this repository. Allow only Remove, Rename, Docs, Refactor, Fix, and Feat with the exact current branch name as the scope, and require the summary to be written in English.
---

# Commit by Branch

Apply the following subject format to every commit:

```text
<Type>(<current-branch-name>): <summary>
```

Use the current branch name exactly as returned by:

```bash
git branch --show-current
```

Stop and report the problem when the command returns an empty value because HEAD is detached. Do not invent, shorten, normalize, or translate the branch name.

## Allowed types

Use only these case-sensitive types:

- `Remove`: Delete code, files, features, or dependencies.
- `Rename`: Rename or move files, symbols, endpoints, or other identifiers without materially changing behavior.
- `Docs`: Change only documentation, comments, examples, or learning materials.
- `Refactor`: Restructure implementation without changing externally observable behavior.
- `Fix`: Correct a defect or unintended behavior.
- `Feat`: Add or extend externally observable functionality.

Never use any other prefix, including `Chore`, `Test`, `Style`, `Build`, `CI`, `Perf`, or `Revert`. When a change does not fit one allowed type, choose the allowed type that describes its primary intent. Split the work into separate commits when it has multiple independent intents.

## Workflow

1. Confirm that the user has authorized creating or rewriting a commit. Do not treat this skill as commit authorization.
2. Run `git status --short`, `git diff`, and `git diff --cached` to understand the worktree and staged changes.
3. Read the exact current branch name with `git branch --show-current`.
4. Stage only files that belong to the requested logical change. Preserve unrelated user changes.
5. Select exactly one allowed type from the primary intent of the staged diff.
6. Write a concise English summary after `: `. Use an imperative verb, state what changed, and do not end the subject with a period.
7. Review `git diff --cached` immediately before committing.
8. Commit using the complete subject, for example:

   ```bash
   git commit -m "Feat(feature/login): Add JWT login support"
   ```

9. Verify the created subject with `git log -1 --pretty=%s` and report it to the user.

## Validation

A valid subject must satisfy all of these rules:

- Start with exactly one of `Remove`, `Rename`, `Docs`, `Refactor`, `Fix`, or `Feat`.
- Follow the type immediately with `(` and the exact current branch name.
- Follow the closing `)` immediately with `: `.
- Include a non-empty English summary after `: `.
- Contain no emoji or text before the type.

Valid examples on branch `feature/login`:

```text
Feat(feature/login): Add JWT login support
Fix(feature/login): Correct expired token refresh handling
Docs(feature/login): Add login API usage examples
Refactor(feature/login): Move token validation into the service
Rename(feature/login): Rename AuthDto to LoginRequest
Remove(feature/login): Remove unused session authentication code
```

Invalid examples:

```text
feat(feature/login): Add JWT login support
Chore(feature/login): Clean up configuration
Fix(login): Correct token validation
Fix(feature/login) Correct token validation
Feat(feature/login): JWT 로그인 기능 추가
```
