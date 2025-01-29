# Add virtual


## Source file

```

class A {
  public:
    void func();
};

```


### match:
```
...
class A ... {
  ...
  >>> void func(...
}
```

### patch

```
virtual
```


## Result

```
class A {
  public:
    virtual void func();
};

```