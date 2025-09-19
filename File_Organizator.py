from pathlib import Path
import shutil

class fileOrganizator:
    def __init__(self,user_name):
        self.home_dir = Path.home()

        self.resource_dir = self.home_dir / "Downloads"

        self.target_dirs = {
            "Document":self.home_dir/ "Filtered" / "Document",
            "Photo":self.home_dir/ "Filtered" / "Photo",
            "Video":self.home_dir/ "Filtered" / "Video",
            "Music":self.home_dir/ "Filtered" / "Music",
            "Code":self.home_dir/ "Filtered" / "Code",
            "Archive":self.home_dir / "Filtered" / "Archive",
            "Executable":self.home_dir / "Filtered" / "Executable"
        }

        self.extensions = {
            'Document': [
                '.pdf', '.docx', '.doc', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx',
                '.md', '.tex', '.csv', '.tsv', '.log', '.json', '.xml', '.ahk'
            ],
            'Photo': [
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.heic', '.ico',
                '.raw', '.cr2', '.nef', '.orf'
            ],
            'Video': [
                '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.m4v',
                '.3gp', '.mts', '.vob'
            ],
            'Music': [
                '.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg', '.wma', '.alac', '.aiff', '.pcm'
            ],
            'Code': [
                '.py', '.js', '.html', '.css', '.json', '.xml', '.csv', '.java', '.c', '.cpp', '.h',
                '.hpp', '.cs', '.ts', '.tsx', '.jsx', '.sh', '.bat', '.ps1', '.php', '.rb', '.go',
                '.rs', '.swift', '.kt', '.kts', '.m', '.scala'
            ],
            'Archive': [
                '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg','.inf'
            ],
            'Executable': [
                '.exe', '.msi', '.bat', '.cmd', '.apk', '.app'
            ]
        }


    def make_dirs(self):
        for path_dir in self.target_dirs.values():
            path_dir.mkdir(parents=True,exist_ok=True)
            print(f"Directory is ready: {path_dir}")

    def find_file_extension(self,file_extension):
        file_extension = file_extension.lower()
        for type, extensions in self.extensions.items():
            if file_extension in extensions:
                return type
        return None
    
    
    def create_unique_name(self,target_path):
        if not target_path.exists():
            return target_path
        
        counter = 1
        while True: 
            new_name = f"{target_path.stem}({counter}){target_path.suffix}"
            new_path = target_path.parent / new_name

            if not new_path.exists():
                return new_path
            counter += 1

    def organize_files(self):
        if not self.resource_dir.exists():
            print(f"Resource directory is not existsÇ {self.resource_dir}")
            return


        print(f"Using this directory: {self.resource_dir}")
        self.make_dirs()
        print("="*50)

        
        move_files = []

        for file in self.resource_dir.iterdir():
            if file.is_file():
                file_type = self.find_file_extension(file.suffix)
                if file_type:
                    move_files.append((file,file_type))

        print(f"{len(move_files)} files will move")

        for file, file_type in move_files:
            target_dir = self.target_dirs[file_type]
            target_path = target_dir / file.name

            unique_target = self.create_unique_name(target_path)

            try:
                shutil.move(str(file),str(unique_target))
            except Exception as e:
                print(f"Error - {file.name} - {e}")

if __name__ == "__main__":
    user_name = str(input("Enter user directory name: "))

    organizator = fileOrganizator(user_name)

    answer = input("\n❓Are you sure (n/y): ").lower()
    
    if answer == 'y':
        organizator.organize_files()
    else: 
        print("Permission denied")