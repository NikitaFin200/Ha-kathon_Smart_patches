# Replace

## Source file

```

constexpr char kServiceUrl[] = "https://google.com/service/v2";

```


### match:
```
...
">>>https://google.com/service/v2<<<"
```

### patch

```
https://brave.com/service/v3
```


## Result

```

constexpr char kServiceUrl[] = "https://brave.com/service/v3";

```