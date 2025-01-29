# Add at the function end


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
  ...
  >>>
}
```

### patch

```
std::cout << std::endl;

```


## Result

```

void A::func() {
  std::cout << "Yeah, baby!";
  std::cout << std::endl;
}

```