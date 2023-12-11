import os, shutil
import gzip
class FileOperations:

    @staticmethod
    def makedirs(path):
        abs_path = os.path.abspath(path)
        os.makedirs(abs_path, exist_ok=True)

    @staticmethod
    def clean_directory(path):

        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            items = os.listdir(abs_path)
            for item in items:
                path = os.path.join(abs_path, item)
                if os.path.exists(path):
                    try:
                        if os.path.isdir(path):
                            shutil.rmtree(path)
                        elif os.path.isfile(path):
                            os.remove(path)
                    
                    except Exception as e:
                        print(f'clean up error {str(e)}')


    @staticmethod
    def get_file_from_path(path: str):
        head, tail = os.path.split(path)

        if tail:
            return tail
        
        return head


    @staticmethod
    def write_to_file(file_path: str, output):
        """
        Writes output to a file.

        Args:
            file_path (str): Path to the JSON file.
            output (str): output.
        """
        file_name = FileOperations.get_file_from_path(file_path)
        directory = file_path.replace(file_name, "")
        # Ensure the directory exists, create it if not
        FileOperations.makedirs(directory)

        with open(file_path, 'w') as file:
            file.write(output)
            
        return file_path
    
    @staticmethod    
    def gzip_file(input_file, output_file = None):
       
        output_file = f'{input_file}.gz'
        with open(input_file, 'rb') as f_in:
            with gzip.open(output_file, 'wb') as f_out:
                f_out.writelines(f_in)

        return output_file