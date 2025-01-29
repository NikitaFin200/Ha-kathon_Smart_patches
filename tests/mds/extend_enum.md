# Extend enum


## Source file

```

enum class Reasons {
  kNone = 0,
  kGeneralFail,
  kNotConnected,
  kTimeout,
  kCount = kTimeout + 1,
}


```


### match:
```
...
enum class Reasons {
  ...
  >>>
  kMax = ...
```

### patch

```
kVerificationFailed,

```

### match:
```
...
enum class Reasons {
  ...
  kMax = >>>kTimeout<<<
```

### patch

```
kVerificationFailed

```


## Result

```

enum class Reasons {
  kNone = 0,
  kGeneralFail,
  kNotConnected,
  kTimeout,
  kVerificationFailed,
  kMax = kVerificationFailed + 1,
}


```