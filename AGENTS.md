# Repository Guidelines

## Language

- Use **MCI 845 Cluster** as the project name.
- Use English by default for repository metadata, document titles and headings, table headers, issue and pull request titles, release titles, branch names, filenames, code, and code comments.
- Write the body prose of project documentation in Simplified Chinese. Use English for `AGENTS.md` and other repository instruction files.

## Commits

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Write the subject, optional body, and any prose in footers in English. Use `type(scope): summary` with an optional scope. Write a short, imperative summary, such as `docs: add repository guidelines` or `fix(controller): correct slot numbering`. Mark breaking changes with `!` in the prefix or a `BREAKING CHANGE:` footer.

## Anti-Defensive Programming

- Implement the required behavior directly. Use the existing types, interfaces, and invariants to keep the normal path simple.
- Validate external input and enforce invariants at the boundary that owns them. Once a value has been validated, reuse that guarantee within the same trust boundary.
- Handle failures that the operation can actually encounter. Preserve the cause and enough context to diagnose it. Use fallbacks and retries when their behavior is defined and they can preserve a consistent state.
- Keep guards that protect hardware, data, or security and checks required by an interface. Tie each guard to a concrete failure mode. Avoid duplicate checks, speculative compatibility paths, blanket exception handlers, and silent defaults that hide faults.

## Anti-Defensive Writing

Lead with the claim, decision, or action. Use concrete facts and operating conditions. State material limitations once where they affect validity or use. Remove repeated caveats, speculative objections, and unnecessary negative contrasts.
