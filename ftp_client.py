from ftplib import FTP, all_errors
import socket, os, getpass


def help_msg():
    print('\t"dir" to list directory content')
    print('\t"download your_file" to download file from server')
    print('\t"upload your_file_path" to upload file to server')
    print('\t"delete your_file" to delete file on server')
    print('\t"cwd dirname" to change working directory')
    print('\t"mkd dirname" to create directory')
    print('\t"rmd dirname" to delete directory')
    print('\t"rename filename newfilename" to rename file')
    print('\t"relogin" if accidentally lost connection')
    print('\t"exit" to exit from program')



def check_commands(func, *args):
        try:
            func(*args)
        except Exception as e:
            print(f"Command failed: {e}")

def isdir(ftp_, filename):
    try:
        ftp_.cwd(filename)
        ftp_.cwd("..")
        return True
    except:

        return False

def get_data(ftp_, path):
    if isdir(ftp_, path):
        print("It will only download files from specified directory.")
        os.makedirs(path, exist_ok=True)

        ftp_.cwd(path)
        items = [item for item in ftp_.nlst() if item != "." and item != ".."]

        for item in items:
            if not isdir(ftp_, item):
                get_file(ftp_, item, folder=path)
        ftp_.cwd("..")

    else:
        os.makedirs("Downloads", exist_ok=True)
        get_file(ftp_, path)

def get_file(ftp_, file, folder=None):
    if folder is not None:
        folder = folder
    else:
        folder = "Downloads"
    try:
        ftp_.retrbinary("RETR " + file, open(os.path.join(folder, file), 'wb').write)
        print(f"{file} successfully downloaded")
    except Exception as e:
        print("Error. Failed to download", e)

def upload_file(ftp_, path):
        if os.path.isdir(path):
            directory = os.path.basename(path)
            make_dir(ftp_, directory)
            ftp_.cwd(directory)
            for item in os.listdir(path):
                file_path = os.path.join(path, item)
                if os.path.isfile(file_path):
                    uploader(ftp_, item, open(file_path, 'rb'))
            ftp_.cwd("..")

        else:
            filename = os.path.basename(path)
            uploader(ftp_, filename, open(path, 'rb'))

def uploader(ftp_, file, f):
        ftp_.storbinary("STOR " + file, f)
        print(f"{file} successfully uploaded")
        f.close()

def delete_file(ftp_, filename):
        ftp_.delete(filename)
        print(f'{filename} successfully deleted')

def make_dir(ftp_, dir_name):
        ftp_.mkd(dir_name)
        print(f"{dir_name} directory created")


def rename_file(ftp_, file, renamed):
    ftp_.rename(file, renamed)
    print(f"{file} file was renamed to {renamed}")


def delete_dir(ftp_, dir_name):
        ftp_.rmd(dir_name)
        print(f"{dir_name} directory deleted")


def change_wd(ftp_, dir_name):
        ftp_.cwd(dir_name)
        print(f"working directory changed to {dir_name}")

def login(ftp_):
    username = input("> Enter your username: ")
    # don't show pass when typing it
    password = getpass.getpass("> Enter your password(It won't show up): ")
    ftp_.login(username.strip(), password.strip())

def main():
    hostname = input("> Enter your hostname: ")
    try:
        with FTP(hostname.strip()) as ftp:

            try:
                login(ftp)

                command = ""
                while command != 'exit':
                    command = input("\n\tEnter command or \"help\"\n" + "> ")

                    # parse command line
                    if len(command.split()) == 3:
                        command, argument1, argument2 = command.split()
                    elif len(command.split()) == 2:
                        command, argument1 = command.split()

                    # check command and run functions
                    if command == "dir":
                        print("Directory content: ")
                        ftp.dir()

                    elif command == 'pwd':
                        print(ftp.pwd())

                    elif command == "download":
                        check_commands(get_data, ftp, argument1)

                    elif command == "upload":
                        check_commands(upload_file, ftp, argument1)

                    elif command == "delete":
                        check_commands(delete_file, ftp, argument1)

                    elif command == "cwd":
                        check_commands(change_wd, ftp, argument1)

                    elif command == 'mkd':
                        check_commands(make_dir, ftp, argument1)

                    elif command == 'rmd':
                        check_commands(delete_dir, ftp, argument1)

                    elif command == 'rename':
                        check_commands(rename_file, ftp, argument1, argument2)

                    elif command == 'help':
                        help_msg()

            except KeyboardInterrupt:
                print('Ctrl+C was pressed. Exiting...')

            except all_errors as e:
                print(f"FTP Error: {e}")

            except:
                print(f'Error. Exiting...')

    except socket.gaierror:
        print("Failed to get address. Exiting...")

    except TimeoutError:
        print(f'Timeout error. Failed to connect to {hostname}')

if __name__ == '__main__':
    main()
