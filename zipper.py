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

def create_archive(archive_name, directory):
    """
    CREATES A ZIP ARCHIVE FROM A DIRECTORY
    """
    total_files = count_files(directory)
    processed_files = 0

    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == '.DS_Store':
                    continue
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, os.path.dirname(directory))
                zipf.write(full_path, arcname=os.path.basename(file))
                processed_files += 1
                print(f"\r{' '*80}", end='') #CLEAR THE LINE
                print(f"\rADDING FILE {processed_files}/{total_files} TO ARCHIVE ({processed_files/total_files*100:.2f}% COMPLETED) | {file}", end='')

    print(f"\rADDING FILE {total_files}/{total_files} TO ARCHIVE (100.00% COMPLETED) | ")

def extract_archive(archive_name, target_directory):
    """
    EXTRACTS A ZIP ARCHIVE TO A DIRECTORY
    """
    try:
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            total_files = len(zipf.namelist())
            processed_files = 0
            for file in zipf.namelist():
                zipf.extract(file, target_directory)
                processed_files += 1
                print(f"\r{' '*80}", end='') #CLEAR THE LINE
                print(f"\rEXTRACTING FILE {processed_files}/{total_files} ({processed_files/total_files*100:.2f}% COMPLETED) | {file}", end='')

        print(f"\rEXTRACTING FILE {total_files}/{total_files} (100.00% COMPLETED)")
        print("\nEXTRACTION COMPLETED SUCCESSFULLY!")
    except Exception as e:
        print(f"\nERROR WHILE EXTRACTING ARCHIVE: {e}")

if __name__ == "__main__":
    # LISTS ALL DIRECTORIES IN THE CURRENT DIRECTORY
    directories = [name for name in os.listdir('.') if os.path.isdir(name)]

    # IF THERE ARE NO DIRECTORIES, DISPLAYS AN ERROR MESSAGE AND EXITS
    if not directories:
        print("ERROR : NO DIRECTORIES FOUND.")
        exit(1)

    # DISPLAYS THE DIRECTORIES AND ASKS THE USER TO CHOOSE ONE OR MORE
    while True:
        print("PLEASE CHOOSE ONE OR MORE DISRECTORIES TO ZIP (SEPARATED BY SPACES):")
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
        for directory in chosen_directories:
            create_archive(archive_name, directory)
