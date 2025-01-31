## Test 6: Add console log (TypeScript)

### Source file

```

function display() {
    console.log("Hello!");
}

```

### match:
```
...
function display(...) {
    >>>
    ...
```

### patch

```
console.log("[INFO]:");

```

## Expected Result

```

function display() {
    console.log("[INFO]:");
    console.log("Hello!");
}

```