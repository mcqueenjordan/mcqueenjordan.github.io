---
layout: thought
title: "Indent With Intent"
subtitle: "None"
name: "indent-with-intent"
published_date: "2019-07-02"
category: post
topics: ['coding style']
---

```
OperatingSystem determine_operating_system(string uname) {
  if (uname.contains("Darwin")) {
    return OperatingSystem.MacOS;
  } else if (uname.contains("Linux")) {
    return OperatingSystem.Linux;
  } else {
    return OperatingSystem.Unknown;
  }
}
```

> Nit: you can remove the final `else`.

A common code review comment. But does it hold up to scrutiny? Is the code
better if we remove that `else`? Let's take a look at what this code looks like
after applying the suggestion.

```
OperatingSystem determine_operating_system(string uname) {
  if (uname.contains("Darwin")) {
    return OperatingSystem.MacOS;
  } else if (uname.contains("Linux")) {
    return OperatingSystem.Linux;
  }
  return OperatingSystem.Unknown;
}
```

By omitting the final `else`, we've broken the structural alignment of our
similar logic. Indentation is a visual manifestation of logical structure.
Things that are alike logically and structurally should reflect that visually.

This function is effectively a tri-branch conditional return. And the code
should show that as explicitly as possible. The `else` logically groups the
code and encodes that meaning into it via structure. There's a [cargo
cult](/thought/cargo-cult-programming) against using `else` anywhere. Don't
fall for that trap.

If you're still not convinced, consider this. Would you write a switch statement
like this?

```
switch(color) {
  case "red":
    return Color.Red;
  case "blue":
    return Color.Blue;
}
return Color.Unknown;
```

Or would you write it like this?

```
switch(color) {
  case "red":
    return Color.Red;
  case "blue":
    return Color.Blue;
  default:
    return Color.Unknown;
}
```

Indentation has meaning. `else` is a keyword for a reason. Structure your
programs with intention.

