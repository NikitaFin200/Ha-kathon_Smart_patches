# Add at the function end


## Source file

```

class A:
    def func(self):
        print("Yeah, baby!")

```


### match:
```
...
def func(self):
  ...
  >>>
```

### patch

```
print()

```


## Result

```

class A:
    def func(self):
        print("Yeah, baby!")
        print()

```