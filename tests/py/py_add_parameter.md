# Add parameter

## Source file

```

class A(B):
    def func(self, s):
        pass

```


### match:
```
...
class A(...) :
    ...
    def func(self, ...) :
        >>>
```

### patch

```
, i
```


## Result

```

class A(B):
    def func(self, s, i):
        pass


```