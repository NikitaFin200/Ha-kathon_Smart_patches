## Test 5: Add initialization (Rust)

### Source file

```

fn increment() {
    count += 1;
}

```

### match:
```
...
fn increment(...) {
    >>>
    ...
```

### patch

```
let mut count = 0;

```

## Expected Result

```

fn increment() {
    let mut count = 0;
    count += 1;
}

```