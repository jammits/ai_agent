import os

def write_file(working_directory, file_path, content):
    file_rel_path = os.path.join(working_directory,file_path)
    file_abs_path = os.path.abspath(file_rel_path)
    working_path = os.path.abspath(working_directory)

    try:
        if not file_abs_path.startswith(working_path):
            raise Exception()
        
        if not os.path.exists(file_abs_path):
            parent = os.path.dirname(file_abs_path)
            os.makedirs(parent, exist_ok=True)
            


        with open(file_abs_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    

    except FileExistsError:
        return f'Error: Target directory already exists.'
    except Exception:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

