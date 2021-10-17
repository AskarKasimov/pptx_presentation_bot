import ctypes
a = ["ddd", "aaa"]
print(ctypes.cast(id(a), ctypes.py_object).value)
a.append("ccc")
print(ctypes.cast(id(a), ctypes.py_object).value)
b = a
b.append("sec")
print(ctypes.cast(id(a), ctypes.py_object).value)
print(ctypes.cast(id(b), ctypes.py_object).value)
print(a)
print(b)