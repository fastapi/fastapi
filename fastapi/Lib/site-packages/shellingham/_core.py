SHELL_NAMES = (
    {"sh", "bash", "dash", "ash"}  # Bourne.
    | {"csh", "tcsh"}  # C.
    | {"ksh", "zsh", "fish"}  # Common alternatives.
    | {"cmd", "powershell", "pwsh"}  # Microsoft.
    | {"elvish", "xonsh"}  # More exotic.
)


class ShellDetectionFailure(EnvironmentError):
    pass
