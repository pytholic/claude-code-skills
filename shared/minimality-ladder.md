<!-- BEGIN shared: minimality-ladder -->
Before writing code, stop at the first rung that holds:

1. Does this need to exist? → no: don't build it
2. Already in this codebase? → reuse, don't rewrite
3. Stdlib does it? → use it
4. Native platform feature? → use it
5. Installed dependency? → use it
6. One line? → one line
7. Only then: the minimum that works

Walk the ladder *after* understanding the problem, not instead of it — read the code the
change touches and trace the real flow before picking a rung. Lazy about the solution,
never about reading.

**Never traded away, at any rung:** trust-boundary validation, data-loss handling,
security, accessibility. Code ends up small because it's necessary, not golfed.
<!-- END shared: minimality-ladder -->
