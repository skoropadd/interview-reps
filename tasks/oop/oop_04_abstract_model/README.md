# oop_04 · An abstract base class: Model

**Theory in three lines**
- An abstract base class describes an interface: "every model has `fit` and `predict`". You cannot create an object from it directly.
- You write it with `from abc import ABC, abstractmethod`, `class Model(ABC)`, and `@abstractmethod` above each method subclasses must provide.
- A subclass that leaves out an abstract method cannot be instantiated either: Python raises `TypeError`.

**Task.**
- `Model`: an abstract base class with abstract methods `fit(self, X, y)` and `predict(self, X)`. It also has a normal method `score(self, X, y)` that returns the mean absolute error of `predict(X)` against `y`.
- `MeanModel(Model)`: `fit` stores the mean of `y` and returns `self`; `predict` returns that mean once for every row of `X`.
- `Model()` must raise `TypeError`. So must a subclass that only implements `fit`.

This is the shape of a classic live-coding task: a concrete class implementing an abstract interface.
