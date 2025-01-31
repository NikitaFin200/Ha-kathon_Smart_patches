## Test 4: Add logging (Python)

### Source file

```

def log():
    print("Logging data...")

```

### match:
```
...
def log(...):
    >>>
    ...
```

### patch

```
print("[INFO]: ")

```

## Expected Result

```

def log():
    print("[INFO]: ")
    print("Logging data...")

```