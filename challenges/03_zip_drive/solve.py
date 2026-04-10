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
