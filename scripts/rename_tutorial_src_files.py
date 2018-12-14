#%%
from pathlib import Path
from string import digits


#%%
directory = Path("./docs/tutorial/src")
output_directory = Path("./docs/tutorial/out")
output_directory.mkdir(exist_ok=True)
files = sorted([Path(f) for f in directory.iterdir()])
for i, f in enumerate(files):
    f: Path
    index = str(i + 1).zfill(2)
    new_name = output_directory / f"tutorial{index}.py"
    print(new_name)
    f.rename(new_name)
