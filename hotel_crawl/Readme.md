# Using top-sis
```bash
>>> from topsis import topsis
>>> a = [[7, 9, 9, 8], [8, 7, 8, 7], [9, 6, 8, 9], [6, 7, 8, 6]]
>>> w = [0.1, 0.4, 0.3, 0.2]
>>> I = [1, 1, 1, 0]
>>> decision = topsis(a, w, I)
```