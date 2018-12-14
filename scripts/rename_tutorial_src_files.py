#%%
from pathlib import Path, PurePath
from string import digits


#%%
directory = Path("./docs/tutorial/src")
dirs = sorted([Path(f) for f in directory.iterdir()])
d: PurePath
sufix = "__out__"
for d in dirs:
    if d.name.endswith(sufix):
        continue
    output_dir_name = d.name + "__out__"
    output_directory = directory / output_dir_name
    output_directory.mkdir(exist_ok=True)
    files = sorted([Path(f) for f in d.iterdir()])
    for i, f in enumerate(files):
        index = str(i + 1).zfill(3)
        new_name = output_directory / f"tutorial{index}.py"
        print(new_name)
        f.rename(new_name)

for d in dirs:
    current_dir = Path(str(d) + sufix)
    print(current_dir)
    current_dir.rename(d)


#%%
