# Implementation notes

Out-of-scope findings recorded during work on other changes. Nothing here has been acted on.

_All three entries recorded before 3.0.0 were resolved by `collapse-to-authored-tree` and removed:
the `todo`-not-in-the-generated-tool-inventory note (agents no longer declare a tool list at all),
the four single-cased SQL-to-RCE deny patterns (the deny map was dropped with opencode; the upstream
gap is recorded in `docs/roles/operator.md`), and the missing rule that retrieved content is data
rather than instructions (now stated in all nine prompts)._
