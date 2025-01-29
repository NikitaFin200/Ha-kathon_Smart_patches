# Add parameter

## Source file

```

class A : public B {
  public:
  int func(const std::string& s);
}

```


### match:
```
...
class A ... {
  ...
  int func(... >>>)
  ...
}
```

### patch

```
, int i
```


## Result

```

class A : public B {
  public:
  int func(const std::string& s, int i);
}

```