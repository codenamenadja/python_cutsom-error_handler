# Python Custom module

## Error hanlder with logging

### 기초 사용법

- Expected Error

> 2번째 요소를 지정하면서 특정상황에 일으키는 예견된 에러

```python
raise ValueError("some message", "info")
raise PermissionError("some message", "warning")
raise FileNotFoundError("some message", "errror")
raise AttributeError("some message", "debug")
raise ConnectionRefusedError("some message", "critical")
raise ConnectionAbortedError("some message", "fatal")
```

- UnExpected Error

> 2번째 요소가 지정 되지 않는 실제 에러

```python
raise ValueError("message")
```
