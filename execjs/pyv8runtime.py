class PyV8Runtime:
    def __init__(self):
        try:
            import PyV8
        except ImportError:
            self._is_available = False
        else:
            self._is_available = True

    @property
    def name(self):
        return "PyV8"

    def exec_(self, source):
        return self.Context().exec_(source)

    def eval(self, source):
        return self.Context().eval(source)

    def compile(self, source):
        return self.Context(source)

    def is_available(self):
        return self._is_available

    class Context:
        def __init__(self, source=""):
            self._source = source

        def exec_(self, source):
            source = '''\
            (function() {{
                {0};
                {1};
            }})()'''.format(
                encode_unicode_codepoints(self._source),
                encode_unicode_codepoints(source)
            )
            source = str(source)

            import PyV8
            import contextlib
            #backward compatibility
            with contextlib.nested(PyV8.JSContext(), PyV8.JSEngine()) as (ctxt, engine):
                js_errors = (PyV8.JSError, IndexError, ReferenceError, SyntaxError, TypeError)
                try:
                    script = engine.compile(source)
                except js_errors as e:
                    raise RuntimeError(e)
                try:
                    value = script.run()
                except js_errors as e:
                    raise ProgramError(e)
                return self.convert(value)

        def eval(self, source):
            return self.exec_('return ' + encode_unicode_codepoints(source))

        def call(self, identifier, *args):
            args = json.dumps(args)
            return self.eval("{identifier}.apply(this, {args})".format(identifier=identifier, args=args))

        @classmethod
        def convert(cls, obj):
            from PyV8 import _PyV8
            if isinstance(obj, bytes):
                return obj.decode('utf8')
            if isinstance(obj, _PyV8.JSArray):
                return [cls.convert(v) for v in obj]
            elif isinstance(obj, _PyV8.JSFunction):
                return None
            elif isinstance(obj, _PyV8.JSObject):
                ret = {}
                for k in obj.keys():
                    v = cls.convert(obj[k])
                    if v is not None:
                        ret[cls.convert(k)] = v
                return ret
            else:
                return obj



