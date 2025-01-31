## Test 1: Add logging (C++)

### Source file

```

void Logger::log() {
  std::cout << "Logging data...";
}

```

### match:
```
...
void Logger::log(...) {
  >>>
  ...
```

### patch

```
std::cout << "[INFO]: ";

```

## Expected Result

```

void Logger::log() {
  std::cout << "[INFO]: ";
  std::cout << "Logging data...";
}

```