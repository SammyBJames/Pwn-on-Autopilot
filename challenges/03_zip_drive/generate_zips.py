import zipfile
import os
import uuid


def generate():
    # Final output file starts here
    flag_content = 'bsides{g4ry_1s_4_m4st3r_0f_z1pp1ng_xd}'
    current_file = 'flag.txt'
    
    with open(current_file, 'w') as f:
        f.write(flag_content)
        
    print('Generating 300 nested zip files...')
    
    # Iterate backwards so my_important_file is the outermost zip
    for i in range(300, 0, -1):
        # The outermost zip gets a clean name
        if i == 1:
            next_file = 'my_important_file.zip'
        else:
            # Everything inside gets a randomized hex name
            next_file = f'{uuid.uuid4().hex}.zip'
            
        with zipfile.ZipFile(next_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(current_file)
            
        # Delete the previous file so we only have the top level zip
        os.remove(current_file)
        
        # Advance the pointer
        current_file = next_file

    print(f'Successfully generated. Root file is: {current_file}')


if __name__ == '__main__':
    generate()
