---
layout: thought
title: "Documentation should be high-level"
subtitle: "Keep your documentation legible and sustainable"
category: post
topics: ["software engineering"]
name: "documentation-should-be-high-level"
published_date: "2017-09-09"
---

A few days ago, our team launched a new component. A week after launch, while
dealing with some ops tickets, we discovered that the detailed, extensive wiki
document for that component was already out-of-date.

This is a familiar story to any dev. Documentation is hard to keep accurate.
The knee-jerk reaction is to assess that the miss here was that we allowed the
documentation to become inaccurate. The knee-jerk reaction is wrong. It is not
feasible to maintain documentation if that documentation is too specific.

The solution is to change the philosophical approach to documentation. For
software systems of any reasonable complexity, the code is the only source of
truth for its behavior and its descriptive reality. Documentation ought to
answer the following questions, in basic non-technical english prose:

1. Why did we create this component? (prescriptive statement)
2. At a high-level, how does it solve its problem? (This answer should
absolutely not map anywhere near 1:1 to its implementation. It should be at an
extremely high-level.)
3. Going no deeper than a file/class level view, describe in a paragraph the
function of the most critical classes/files/modules in the code. This is as
specific as it should get, and this serves as a guide for an engineer to dive
into the code.

Again, documentation should never map 1:1 to anything more specific than a
class. Anything more specific than that, and it effectively has to change
whenever the code changes. If you're changing the function of tons of classes
and files, it is reasonable to expect that the documentation would necessarily
have to change in kind.

Writing documentation at a high-level helps to minimize the potential that your
documentation will become out-of-date and inaccurate. It is easier to
understand, too. Which is kind of the point. If someone wants to know the
objective truth exactly as it exists, the documentation is absolutely the wrong
place for that. That's what the code is for.

