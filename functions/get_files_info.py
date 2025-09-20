import os


def get_files_info(working_directory, directory="."):
    try:
        relative_path = os.path.join(working_directory, directory)
        abs_path = os.path.abspath(relative_path)
        working = os.path.abspath(working_directory)

        if not abs_path.startswith(working):
            raise Exception()

        if not os.path.isdir(abs_path):
            raise NotADirectoryError
        
        contents = os.listdir(abs_path)
        results = []
        for content in contents:
            item_path = os.path.abspath(os.path.join(abs_path, content))
            file_size = os.path.getsize(item_path)
            is_dir = False
            
            if os.path.isdir(item_path):
                is_dir = True
            
            results.append(f"- {content}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return f"Results for '{directory}' directory:\n" + "\n".join(results)
    except NotADirectoryError:
        return f'Error: "{directory}" is not a directory' 

    except Exception as e:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    
