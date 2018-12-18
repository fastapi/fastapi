#%%
from pathlib import Path, PurePath
from string import digits

directory = Path("./docs/tutorial/src")
skip_names = {"bigger_applications"}
skip_dirs = {directory / name for name in skip_names}
dirs = sorted([Path(f) for f in directory.iterdir() if f not in skip_dirs])
d: PurePath
sufix = "__out__"
for d in dirs:
    if d.name.endswith(sufix):
        continue
    output_dir_name = d.name + "__out__"
    output_directory = directory / output_dir_name
    output_directory.mkdir(exist_ok=True)
    files = sorted([Path(f) for f in d.iterdir()])
    f: PurePath
    for i, f in enumerate(files):
        index = str(i + 1).zfill(3)
        if f.name != "__init__.py" and f.name.endswith(".py"):
            new_name = output_directory / f"tutorial{index}.py"
        else:
            new_name = output_directory / f.name
        print(new_name)
        f.rename(new_name)

for d in dirs:
    current_dir = Path(str(d) + sufix)
    print(current_dir)
    current_dir.rename(d)


#%%
