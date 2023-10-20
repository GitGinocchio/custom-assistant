import json,os

"""
class dict(object)
 |  dict() -> new empty dictionary
 |  dict(mapping) -> new dictionary initialized from a mapping object's
 |      (key, value) pairs
 |  dict(iterable) -> new dictionary initialized as if via:
 |      d = {}
 |      for k, v in iterable:
 |          d[k] = v
 |  dict(**kwargs) -> new dictionary initialized with the name=value pairs
 |      in the keyword argument list.  For example:  dict(one=1, two=2)
 |
 |  Methods defined here:
 |
 |  __contains__(self, key, /)
 |      True if the dictionary has the specified key, else False.
 |
 |  __delitem__(self, key, /)
 |      Delete self[key].
 |
 |  __eq__(self, value, /)
 |      Return self==value.
 |
 |  __ge__(self, value, /)
 |      Return self>=value.
 |
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |
 |  __getitem__(...)
 |      x.__getitem__(y) <==> x[y]
 |
 |  __gt__(self, value, /)
 |      Return self>value.
 |
 |  __init__(self, /, *args, **kwargs)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  __ior__(self, value, /)
 |      Return self|=value.
 |
 |  __iter__(self, /)
 |      Implement iter(self).
 |
 |  __le__(self, value, /)
 |      Return self<=value.
 |
 |  __len__(self, /)
 |      Return len(self).
 |
 |  __lt__(self, value, /)
 |      Return self<value.
 |
 |  __ne__(self, value, /)
 |      Return self!=value.
 |
 |  __or__(self, value, /)
 |      Return self|value.
 |
 |  __repr__(self, /)
 |      Return repr(self).
 |
 |  __reversed__(self, /)
 |      Return a reverse iterator over the dict keys.
 |
 |  __ror__(self, value, /)
 |      Return value|self.
 |
 |  __setitem__(self, key, value, /)
 |      Set self[key] to value.
 |
 |  __sizeof__(...)
 |      D.__sizeof__() -> size of D in memory, in bytes
 |
 |  clear(...)
 |      D.clear() -> None.  Remove all items from D.
 |
 |  copy(...)
 |      D.copy() -> a shallow copy of D
 |
 |  get(self, key, default=None, /)
 |      Return the value for key if key is in the dictionary, else default.
 |
 |  items(...)
 |      D.items() -> a set-like object providing a view on D's items
 |
 |  keys(...)
 |      D.keys() -> a set-like object providing a view on D's keys
 |
 |  pop(...)
 |      D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
 |
 |      If the key is not found, return the default if given; otherwise,
 |      raise a KeyError.
 |
 |  popitem(self, /)
 |      Remove and return a (key, value) pair as a 2-tuple.
 |
 |      Pairs are returned in LIFO (last-in, first-out) order.
 |      Raises KeyError if the dict is empty.
 |
 |  setdefault(self, key, default=None, /)
 |      Insert key with a value of default if key is not in the dictionary.
 |
 |      Return the value for key if key is in the dictionary, else default.
 |
 |  update(...)
 |      D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
 |      If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
 |  Data and other attributes defined here:
 |
 |  __hash__ = None
"""



class jsonfile:
    def __init__(self,fp : str = None,*,indent : int = 3,encoding : str = 'utf-8',autosave : bool = True):
        assert fp.endswith('.json'),'fp must be a json file and end with ".json"'
        self.fp = fp
        self.indent = indent
        self.encoding = encoding
        self.autosave = autosave
        if os.path.exists(self.fp):
            with open(self.fp, 'r', encoding=encoding) as jsf: self.content = json.load(jsf)
        else: 
            self.content = {}
            if self.autosave: self.save()

    def __str__(self):
        return str(self.content)

    def __len__(self):
        return len(self.content)

    def __contains__(self, __k):
        return __k in self.content

    def __getitem__(self, __k):
        if __k in self.content: return self.content[__k]
        else: raise KeyError(f"Key '{__k}' not found in JSON data.")

    def __setitem__(self, __k, __v):
        self.content[__k] = __v
        if self.autosave:self.save()

    def __delitem__(self, __k):
        if __k in self.content:
            del self.content[__k]
            if self.autosave:self.save()
        else:
            raise KeyError(f"Key '{__k}' not found in '{self.fp}'.")

    def __iter__(self):
        return iter(self.content)

    def __next__(self):
        raise StopIteration

    def keys(self):
        return self.content.keys()

    def set(self, keys, value):
        current = self.content
        for key in keys[:-1]:
            if isinstance(current, dict):
                current = current.setdefault(key, {})
            elif isinstance(current, list):
                try:
                    key = int(key)
                    current = current[key]
                except (ValueError, IndexError):
                    return
        if isinstance(current, dict):
            current[keys[-1]] = value
            if self.autosave:
                self.save()
        elif isinstance(current, list):
            try:
                key = int(keys[-1])
                current[key] = value
                if self.autosave:
                    self.save()
            except (ValueError, IndexError):
                pass

    def clear(self):
        self.content = {}
        if self.autosave: self.save()

    def loads(data : str | bytes):
        return json.loads(data)

    def dumps(data : dict):
        return json.dumps(data)

    def save(self,content : dict = None):
        with open(self.fp, 'w',encoding=self.encoding) as jsf: json.dump(content if content is not None else self.content,jsf,indent=self.indent,ensure_ascii=True)
