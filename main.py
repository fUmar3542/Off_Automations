import os
import time
import subprocess
import pyautogui
import pyperclip
import csv


threads = []
lines = []


def open_jps_in_jprofiler(file_path):
    # Replace with the actual path to your JProfiler executable
    jprofiler_path = r"C:\Users\mfarooq14\AppData\Local\jprofiler14\bin\jprofiler.exe"

    # Open the .jps file with JProfiler
    subprocess.Popen([jprofiler_path, file_path])


def write_data(data):
    check = False
    try:
        # Write the results to a new CSV file
        with open('blocked_threads.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
            check = True
    except Exception as ex:
        print(ex)
        with open('errors.txt', 'a') as file:
            file.write(str(ex))
    finally:
        return check


def check_threads(p_x, p_y):
    try:
        pyautogui.hotkey('ctrl', 'c')
        line = pyperclip.paste()
        pyperclip.copy('')
        pyautogui.click(p_x, p_y)
        # Read owning
        pyautogui.click(1700, 850)
        # Simulate Ctrl+A (select all) and Ctrl+C (copy)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        # Get the copied text from the clipboard
        owning = pyperclip.paste()
        pyperclip.copy('')
        if owning:
            # Read waiting
            pyautogui.click(350, 850)
            # Simulate Ctrl+A (select all) and Ctrl+C (copy)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')
            # Get the copied text from the clipboard
            waiting = pyperclip.paste()
            pyperclip.copy('')
            if waiting:
                global threads, lines
                th = [waiting, owning]
                if th not in threads:
                    threads.append(th)
                    lines.append(line)
                    # print("------------------------------------------------------------------------------")
                    # print(line)
                    # print(th)
                    check = write_data(th + (line.split(",")))
                    if not check:
                        with open('errors.txt', 'a') as file:
                            file.write("There is some error occurred during writing to output file")
                        return
    except Exception as ex:
        print(ex)
        with open('errors.txt', 'a') as file:
            file.write(str(ex))
    finally:
        return


def click_read_aloud():
    try:
        # Monitor & Locks
        read_aloud_button_coordinates = (100, 650)
        pyautogui.click(read_aloud_button_coordinates)
        time.sleep(0.5)
        # Monitor History
        read_aloud_button_coordinates = (100, 530)
        pyautogui.click(read_aloud_button_coordinates)
        time.sleep(0.5)
        # Block Only
        pyautogui.click(225, 125)
        time.sleep(0.5)
        pyautogui.click(200, 160)
        pyautogui.click(200, 220)
        time.sleep(0.5)
        # Monitor Class
        read_aloud_button_coordinates = (700, 170)
        pyautogui.click(read_aloud_button_coordinates)
        time.sleep(0.5)

        # Write the results to a new CSV file
        with open('blocked_threads.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Waiting Thread", "Owning Thread", "Time", "Duration", "Type", "Monitor ID", "Monitor Class", "Waiting Thread", "Owning Thread"])

        # Get the current cursor position
        x, y = 700, 180
        pyautogui.click(x, y)
        index = 1

        while True and index < 300:
            try:
                pyautogui.click(x, y)
                # Get the current cursor position
                x, y = pyautogui.position()
                if index % 31 == 0:
                    x, y = 700, 180
                    pyautogui.click(x, y)                # Before
                    pyautogui.hotkey('ctrl', 'c')
                    z = pyperclip.paste()
                    pyperclip.copy('')
                    pyautogui.scroll(-1195)                 # Scroll
                    pyautogui.click(x, y)                   # After
                    pyautogui.hotkey('ctrl', 'c')
                    t = pyperclip.paste()
                    pyperclip.copy('')
                    if t == z:
                        break
                else:
                    check_threads(x, y)
                    y += 17
            except:
                pass
            finally:
                index = index + 1
    except Exception as ex:
        with open('errors.txt', 'a') as file:
            file.write(str(ex))
        print(ex)
    finally:
        return


def main():
    try:
        # Path to your PDF file
        file_path = r'C:\Users\mfarooq14\PycharmProjects\Find_Redundant_Q\input.jps'

        # Open the PDF in Microsoft Edge
        open_jps_in_jprofiler(file_path)

        time.sleep(9)

        click_read_aloud()
        # Replace 'YourAppName' with the actual name or process name of the application you want to close
        app_name = 'jprofiler'

        # Close the application
        os.system(f'taskkill /f /im {app_name}.exe')
    except Exception as ex:
        print(ex)
        with open('errors.txt', 'a') as file:
            file.write(str(ex))


main()