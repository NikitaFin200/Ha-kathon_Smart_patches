# Add at the function begining


## Source file

```

void A::func() {
  std::cout << "Yeah, baby!";
}

```


### match:
```
...
void A::func(...) {
  >>>
  ...
```

### patch

```
std::cout << "John said: ";

```


## Result

```

void A::func() {
  std::cout << "John said: ";
  std::cout << "Yeah, baby!"
}

```