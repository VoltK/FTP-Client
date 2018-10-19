from ftplib import FTP, error_perm, error_temp
import socket, os


def help_msg():
    print('\t"dir" to list directory content')
    print('\t"download your_file" to download file from server')
    print('\t"upload your_file_path" to upload file to server')
    print('\t"delete your_file" to delete file on server')
    print('\t"cwd dirname" to change working directory')
    print('\t"mkd dirname" to create directory')
    print('\t"rmd dirname" to delete directory')
    print('\t"exit" to exit from program')


def check_commands(command_, func, *args):
    if len(command_.split()) > 1:
        try:
            func(*args)
        except:
            print("Command failed")
    else:
        print('blank argument, try again with "your_command your_argument. Enter \"help\" for more details"')


def get_file(ftp_, command_):
        filename = command_.split()[1]
        ftp_.retrbinary("RETR " + filename, open(filename, 'wb').write)
        print(f"{filename} successfully downloaded")


def upload_file(ftp_, command_):
        file_path = command_.split()[1]
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            ftp_.storbinary("STOR " + filename, f)
            print(f"{filename} successfully uploaded")


def delete_file(ftp_, command_):
        ftp_.delete(command_.split()[1])
        print(f'{command_.split()[1]} successfully deleted')


def make_dir(ftp_, command_):
        ftp_.mkd(command_.split()[1])
        print(f"{command_.split()[1]} directory created")


def delete_dir(ftp_, command_):
        ftp_.rmd(command_.split()[1])
        print(f"{command_.split()[1]} directory deleted")


def change_wd(ftp_, command_):
        ftp_.cwd(command_.split()[1])
        print(f"working directory changed to {command_.split()[1]}")


def main():
    hostname = input("> Enter your hostname: ")
    try:
        with FTP(hostname) as ftp:

            username = input("> Enter your username: ")
            password = input("> Enter your password: ")

            try:
                ftp.login(username, password)
                command = ""
                while command != 'exit':
                    command = input("\n\tEnter command or \"help\"\n" + "> ")

                    if command == "dir":
                        print("Directory content: ")
                        ftp.dir()

                    elif command == 'pwd':
                        print(ftp.pwd())

                    elif command.split()[0] == "download":
                        check_commands(command, get_file, ftp, command)

                    elif command.split()[0] == "upload":
                        check_commands(command, upload_file, ftp, command)

                    elif command.split()[0] == "delete":
                        check_commands(command, delete_file, ftp, command)

                    elif command.split()[0] == "cwd":
                        check_commands(command, change_wd, ftp, command)

                    elif command.split()[0] == 'mkd':
                        check_commands(command, make_dir, ftp, command)

                    elif command.split()[0] == 'rmd':
                        check_commands(command, delete_dir, ftp, command)

                    elif command == 'help':
                        help_msg()
            except KeyboardInterrupt:
                print('Ctrl+C was pressed. Exiting...')

            except error_perm:
                print("530 Login authentication failed. Exiting...")

            except error_temp:
                print("421 Idle timeout (30 seconds): closing control connection. Exiting...")

            except:
                print('Error. Exiting...')

    except socket.gaierror:
        print("Failed to get address. Exiting...")

    except TimeoutError:
        print(f'Timeout error. Failed to connect to {hostname}')


if __name__ == '__main__':
    main()
