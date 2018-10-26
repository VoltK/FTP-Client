from ftplib import FTP, all_errors
import socket, os


def help_msg():
    print('\t"dir" to list directory content')
    print('\t"download your_file" to download file from server')
    print('\t"upload your_file_path" to upload file to server')
    print('\t"delete your_file" to delete file on server')
    print('\t"cwd dirname" to change working directory')
    print('\t"mkd dirname" to create directory')
    print('\t"rmd dirname" to delete directory')
    print('\t"rename filename newfilename" to rename file')
    print('\t"exit" to exit from program')


def check_commands(func, *args):
        try:
            func(*args)
        except Exception as e:
            print(f"Command failed: {e}")


def get_file(ftp_, filename):
        ftp_.retrbinary("RETR " + filename, open(filename, 'wb').write)
        print(f"{filename} successfully downloaded")


def upload_file(ftp_, file_path):
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            ftp_.storbinary("STOR " + filename, f)
            print(f"{filename} successfully uploaded")


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


def main():
    hostname = input("> Enter your hostname: ")
    try:
        with FTP(hostname.strip()) as ftp:

            username = input("> Enter your username: ")
            password = input("> Enter your password: ")

            try:
                ftp.login(username.strip(), password.strip())
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
                        check_commands(get_file, ftp, argument1)

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
