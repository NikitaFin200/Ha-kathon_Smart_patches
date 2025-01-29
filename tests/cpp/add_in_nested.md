# Add in nested block


## Source file

```

void A::func() {
  if (x > 0) {
    for (int y = 0; y < x; ++y) {
      std::cout << y;
    }
  }
}

```


### match:
```
...
void A::func(...) {
  ...
  for (int y...) {
    >>>
```

### patch

```
std::cout << x;

```


## Result

```

void A::func() {
  if (x > 0) {
    for (int y = 0; y < x; ++y) {
      std::cout << x;
      std::cout << y;
    }
  }
}

```