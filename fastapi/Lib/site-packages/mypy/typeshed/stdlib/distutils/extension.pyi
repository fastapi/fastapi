class Extension:
    name: str
    sources: list[str]
    include_dirs: list[str]
    define_macros: list[tuple[str, str | None]]
    undef_macros: list[str]
    library_dirs: list[str]
    libraries: list[str]
    runtime_library_dirs: list[str]
    extra_objects: list[str]
    extra_compile_args: list[str]
    extra_link_args: list[str]
    export_symbols: list[str]
    swig_opts: list[str]
    depends: list[str]
    language: str | None
    optional: bool | None
    def __init__(
        self,
        name: str,
        sources: list[str],
        include_dirs: list[str] | None = None,
        define_macros: list[tuple[str, str | None]] | None = None,
        undef_macros: list[str] | None = None,
        library_dirs: list[str] | None = None,
        libraries: list[str] | None = None,
        runtime_library_dirs: list[str] | None = None,
        extra_objects: list[str] | None = None,
        extra_compile_args: list[str] | None = None,
        extra_link_args: list[str] | None = None,
        export_symbols: list[str] | None = None,
        swig_opts: list[str] | None = None,
        depends: list[str] | None = None,
        language: str | None = None,
        optional: bool | None = None,
    ) -> None: ...
