import zipfile
import os

def clear_console():
    if os.name == 'nt':  #FOR WINDOWS
        os.system('cls')
    else:  #FOR UNIX/LINUX/MACOS
        os.system('clear')

clear_console()

def count_files(directory):
    """
    COUNTS THE NUMBER OF FILES IN A DIRECTORY RECURSIVELY
    """
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def create_archive(archive_name, directories):
    """
    CREATES A ZIP ARCHIVE FROM A DIRECTORY
    """
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        total_files = sum(count_files(directory) for directory in directories) # COUNT ALL FILES IN ALL DIRECTORIES
        processed_files = 0

        try:
            for directory in directories:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file == '.DS_Store':
                            continue
                        full_path = os.path.join(root, file)
                        relative_path = os.path.relpath(full_path, directory)
                        zipf.write(full_path, arcname=relative_path)
                        processed_files += 1

                        #PROGRESS BAR
                        percent_complete = (processed_files / total_files) * 100
                        print("PROGRESS: [{:<50}] {:.2f}%".format('='*int(percent_complete/2), percent_complete), end='\r', flush=True)

            #ENSURES THE PROGRESS BAR IS 25% OF THE TOTAL LENGTH AT THE END
            print("\rADDING FILE {}/{} TO ARCHIVE (COMPLETED) [{}] 100.00%".format(total_files, total_files, '='*int(50*0.25)), ' ' * 20, flush=True)
        except Exception as e:
            print("\rERROR DURING ARCHIVING: {}".format(e))
            print("ADDING FILE {}/{} TO ARCHIVE (INCOMPLETE) [{}] {:.2f}%".format(processed_files, total_files, '='*int((processed_files/total_files)*50), (processed_files/total_files)*100), flush=True)

        print()  #PRINTS A NEWLINE AT THE END

def extract_archive(archive_name, target_directory):
    """
    EXTRACTS A ZIP ARCHIVE TO A DIRECTORY
    """
    try:
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            total_files = len(zipf.namelist())
            processed_files = 0

            #CREATE A DIRECTORY FOR EXTRACTION WITH THE SAME NAME AS THE ARCHIVE
            base_extraction_directory = os.path.join(target_directory, os.path.splitext(archive_name)[0])
            extraction_directory = base_extraction_directory
            i = 1
            while os.path.exists(extraction_directory):
                extraction_directory = "{}_{}".format(base_extraction_directory, i)
                i += 1
            os.makedirs(extraction_directory, exist_ok=True)

            for file in zipf.namelist():
                try:
                    #ADJUSTS THE TARGET DIRECTORY FOR EXTRACTION
                    zipf.extract(file, extraction_directory)
                    processed_files += 1
                    percent_complete = (processed_files / total_files) * 100
                    print("PROGRESS: [{:<50}] {:.2f}%".format('='*int(percent_complete/2), percent_complete), end='\r', flush=True)
                except Exception as e:
                    print("\rERROR DURING EXTRACTION: {}".format(e))
                    print("EXTRACTING FILE {}/{} (INCOMPLETE) [{}] {:.2f}%".format(processed_files, total_files, '='*int((processed_files/total_files)*50), (processed_files/total_files)*100), flush=True)

        print("\rEXTRACTING FILE {}/{} (COMPLETED) [{}] 100.00%".format(total_files, total_files, '='*int(50*0.25)), ' ' * 20, flush=True)
        print("\nEXTRACTION COMPLETED SUCCESSFULLY!")
    except Exception as e:
        print(f"\nERROR WHILE OPENING ARCHIVE: {e}")

if __name__ == "__main__":
    # LISTS ALL DIRECTORIES IN THE CURRENT DIRECTORY
    directories = [name for name in os.listdir('.') if os.path.isdir(name)]

    # IF THERE ARE NO DIRECTORIES, DISPLAYS AN ERROR MESSAGE AND EXITS
    if not directories:
        print("ERROR : NO DIRECTORIES FOUND.")
        exit(1)

    # DISPLAYS THE DIRECTORIES AND ASKS THE USER TO CHOOSE ONE OR MORE
    while True:
        print("PLEASE CHOOSE ONE OR MORE DIRECTORIES TO ZIP (SEPARATED BY SPACES):")
        for i, directory in enumerate(directories, start=1):
            print(f"{i}. {directory}")

        choices = input("ENTER THE NUMBERS OF THE DIRECTORIES (TAP 'EXIT' TO QUIT): ").lower().split()
        if '0' in choices or 'exit' in choices:
            print("OK, SCRIPT IS ENDING.")
            exit(0)

        try:
            choices = [int(i)-1 for i in choices]  #ADJUSTS THE INDICES
        except ValueError:
            clear_console()
            print("INVALID INPUT, PLEASE ENTER NUMBERS OR 'EXIT' TO QUIT.\n")
            continue

        if all(0 <= i < len(directories) for i in choices):
            chosen_directories = [directories[i] for i in choices]
            break
        else:
            clear_console()
            print(f"THERE ARE ONLY {len(directories)} SELECTABLE DIRECTORIES, PLEASE CHOOSE AGAIN.\n")

    archive_name = '_'.join(chosen_directories) + '.zip'

    # IF THE ARCHAIVE ALREADY EXISTS, ASKS THE USER IF THEY WANT TO EXTRACT IT
    if os.path.exists(archive_name):
        response = input(f"THE ARCHIVE '{archive_name}' ALREADY EXISTS. DO YOU WANT TO EXTRACT ALL ITEM HERE ? (YES/NO): ").lower()
        if response == 'y' or response == 'yes':
            extract_archive(archive_name, os.getcwd())
        else:
            print("OK, SCRIPT IS ENDING.")
            exit(0)
    else:
        # MOVED OUT OF THE FOR LOOP
        create_archive(archive_name, chosen_directories)