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
with open(filepath, 'r', encoding='utf-8') as file:
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