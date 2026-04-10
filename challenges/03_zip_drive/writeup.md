# ZIP Drive Write Up

## Why Scripting?
We can definitely extract all these files one by one, but that would be a nightmare. We could also use a Bash script in this case, though Python gives us versatility if the challenge were to switch up like in Jumper Cables.

## Intended Solution

### 1. Researching the Tool
We need a way to deal with zip files. Since we haven't covered it in the workshop, let's Google it. With a little effort, we discover the `zipfile` module in the Python standard library. We use the `ZipFile` class to open the archive and query its contents with `.namelist()`.

```python
import zipfile

with zipfile.ZipFile('my_important_file.zip', 'r') as zf:
    namelist = zf.namelist()
    print(namelist)
```

Running this will print out `['e2b34...19f.zip']`, showing us a seemingly random zip file hiding inside the first. Looks like this is gonna go on for a while...

### 2. Setting Up the Loop
Since we don't know exactly how many zip files are nested inside, we can set up a `while True:` loop. We'll open the current zip file, query `.namelist()` to determine the name of the file hiding inside, and then use `.extract(inner_file)` to pull it out. We can then set our pointer to the newly extracted file and repeat the process until we can't anymore.

```python
current_file = 'my_important_file.zip'

while True:
    with zipfile.ZipFile(current_file, 'r') as zf:
        namelist = zf.namelist()
        if not namelist:
            break
        
        # Get the first file in the archive
        inner_file = namelist[0]
        
        # Extract it to the current directory
        zf.extract(inner_file)
```

### 3. Cleanup and Break Logic
If we simply extract, our folder will quickly fill up with potentially thousands of `.zip` files. Let's delete the higher level zip files as we go to save space.

We also need to break our loop at some point. Let's check if the extracted file is not a zip and break in that case.

```python
    while True:
        # ... Extraction logic ...

        # Delete the parent of the file we just unzipped to keep things clean
        if layers_unzipped > 0:
            os.remove(current_file)

        # Set our current file and counter for the next iteration
        current_file = inner_file
        layers_unzipped += 1

        # Check if we extracted anything other than a zip file
        if not current_file.endswith('.zip'):
            print(f'Found a non-zip file at layer {layers_unzipped}: {current_file}')
            break
```

We can also add some error handling to break if we encounter any errors.

```python
        try:
            # ... Extraction logic ...
        except zipfile.BadZipFile:
            print(f'Found bad zip file at layer {layers_unzipped}.')
            break
        except Exception as e:
            print(f'An error occurred at layer {layers_unzipped}: {e}')
            break
```

When we run our final script against the provided `my_important_file.zip`, we get a final `flag.txt` file with the flag inside!

## Solution Script

```python
import zipfile
import os


def solve():
    current_file = 'my_important_file.zip'
    layers_unzipped = 0

    print(f'Starting extraction...')

    # Loop until we can't anymore
    while True:
        try:
            # Open the current zip archive
            with zipfile.ZipFile(current_file, 'r') as zf:
                # Get the first (and only) file in this specific archive level
                namelist = zf.namelist()

                if not namelist:
                    print(f'Archive at layer {layers_unzipped} was empty.')
                    break

                inner_file = namelist[0]

                # Extract it to the current directory
                zf.extract(inner_file)

            # Delete the parent of the file we just unzipped to keep things clean
            if layers_unzipped > 0:
                os.remove(current_file)

            # Set our current file and counter for the next iteration
            current_file = inner_file
            layers_unzipped += 1

            # Check if we extracted anything other than a zip file
            if not current_file.endswith('.zip'):
                print(f'Found a non-zip file at layer {layers_unzipped}: {current_file}')
                break

        except zipfile.BadZipFile:
            print(f'Found bad zip file at layer {layers_unzipped}.')
            break
        except Exception as e:
            print(f'An error occurred at layer {layers_unzipped}: {e}')
            break


if __name__ == '__main__':
    solve()
```
