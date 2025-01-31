# Add at the function begining


## Source file

```

print(fun1(a,b))

```


### match:
```
...
print( ... >>> )
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