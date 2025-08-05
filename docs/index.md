# Please, for god's sake

Don't just create another 5-layer architecture without a spec of documentation.
If you do, you'll, unfortunately, be the *only one who can maintain it*. And it's
not going to last for long, as we can already see for ourselves while doing our
second major refactoring, which is just a fancy term for "rewriting our entire codebase".

# Write any notable thing

Even if it's something as obvious as difference between `core` and `infrastructure`,
not everybody can make sense of it, nor does everybody have a lot of time to figure
it out by themselves.

---

# `ui` - User Interface

There are two possible ways to use our application: 
- **Graphical** User Interface, which we deem as the default one
- **Command Line** Interface, which is great when it comes to scripting and automating
tasks (if for some reason you need *more* automation than is already available in CLMT)

For further information, see [link](ui/index.md).
