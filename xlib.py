import datetime
import random
import re
import socket
import os

def rot13c(c):
    u = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    l = "abcdefghijklmnopqrstuvwxyz"
    p = None

    if c in u:
        p = u
    elif c in l:
        p = l

    if p is not None:
        return p[(p.index(c) + 13) % 26]
    else:
        return c

def rot13(s):
    return ''.join(rot13c(c) for c in s)

def mk_smtpdate(in_ft=None):
    try:
        if in_ft is None:
            t = datetime.datetime.now()
        else:
            t = datetime.datetime.fromtimestamp(in_ft.timestamp())

        utc_offset = datetime.timedelta(minutes=-datetime.datetime.now().astimezone().utcoffset().total_seconds() / 60)

        utc_offset_hours = abs(utc_offset.seconds) // 3600
        utc_offset_minutes = abs(utc_offset.seconds) % 60

        return "{}, {} {} {} {:02d}:{:02d}:{:02d} {}{:02d}{:02d}".format(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][t.weekday()],
            t.day, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][t.month - 1],
            t.year, t.hour, t.minute, t.second,
            '+' if utc_offset >= datetime.timedelta() else '-',
            utc_offset_hours, utc_offset_minutes
        )
    except Exception as e:
        print("Error occurred while generating SMTP Date:", e)
        return None

def xrand_init():
    try:
        random.seed(os.urandom(4))
    except Exception as e:
        print("Error occurred while initializing random generator:", e)

def xrand16():
    try:
        return random.randint(0, 65535)
    except Exception as e:
        print("Error occurred while generating random 16-bit integer:", e)
        return None

def xrand32():
    try:
        return random.getrandbits(32)
    except Exception as e:
        print("Error occurred while generating random 32-bit integer:", e)
        return None

def xstrstr(s, pat):
    try:
        match = re.search(pat, s)
        return match.group() if match else None
    except Exception as e:
        print("Error occurred while finding substring:", e)
        return None

def xstrrchr(s, ch):
    try:
        return s.rfind(ch)
    except Exception as e:
        print("Error occurred while finding last occurrence of character:", e)
        return None

def xstrchr(s, ch):
    try:
        return s.find(ch)
    except Exception as e:
        print("Error occurred while finding first occurrence of character:", e)
        return None

def xsystem(cmd, wait=True):
    try:
        if wait:
            return os.system(cmd)
        else:
            import subprocess
            subprocess.Popen(cmd, shell=True)
            return 0
    except Exception as e:
        print("Error occurred while running system command:", e)
        return 1

def xmemcmpi(p, q, length):
    try:
        return not p[:length].lower() == q[:length].lower()
    except Exception as e:
        print("Error occurred while comparing strings (case-insensitive):", e)
        return None

def xstrncmp(first, last, count):
    try:
        return 0 if first[:count] == last[:count] else 1
    except Exception as e:
        print("Error occurred while comparing strings (first n characters):", e)
        return None

def html_replace(s):
    try:
        found = 0
        pattern = r'&#[0-9]+;'

        def replace(match):
            nonlocal found
            found += 1
            code = int(match.group()[2:-1])
            return chr(code)

        result, _ = re.subn(pattern, replace, s)
        return result, found
    except Exception as e:
        print("Error occurred while replacing HTML entities:", e)
        return None, None

def html_replace2(s):
    try:
        found = 0
        pattern = r'%[0-9A-Fa-f]{2}'

        def replace(match):
            nonlocal found
            found += 1
            code = int(match.group()[1:], 16)
            return chr(code)

        result, _ = re.subn(pattern, replace, s)
        return result, found
    except Exception as e:
        print("Error occurred while replacing HTML entities:", e)
        return None, None

def is_online():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

def main():
    print("Welcome! This is a user-friendly version of the provided code.")
    print("You can interact with the functions defined in this script.")

    while True:
        print("\nPlease select an option:")
        print("1. ROT13 Encoding")
        print("2. Generate SMTP Date")
        print("3. Random 16-bit Integer")
        print("4. Random 32-bit Integer")
        print("5. Find Substring")
        print("6. Find Last Occurrence of Character")
        print("7. Find First Occurrence of Character")
        print("8. Run System Command")
        print("9. Compare Strings (case-insensitive)")
        print("10. Compare Strings (first n characters)")
        print("11. HTML Replace")
        print("12. HTML Replace 2")
        print("13. Check Online Status")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            text = input("Enter text to be ROT13 encoded: ")
            print("ROT13 Encoded Text:", rot13(text))
        elif choice == "2":
            smtp_date = mk_smtpdate()
            if smtp_date is not None:
                print("SMTP Date:", smtp_date)
        elif choice == "3":
            rand_16 = xrand16()
            if rand_16 is not None:
                print("Random 16-bit Integer:", rand_16)
        elif choice == "4":
            rand_32 = xrand32()
            if rand_32 is not None:
                print("Random 32-bit Integer:", rand_32)
        elif choice == "5":
            text = input("Enter the text: ")
            pattern = input("Enter the pattern to search: ")
            result = xstrstr(text, pattern)
            if result is not None:
                print("Pattern found at:", result if result else "Not found")
        elif choice == "6":
            text = input("Enter the text: ")
            ch = input("Enter the character to find: ")
            result = xstrrchr(text, ch)
            if result is not None:
                print("Last occurrence at:", result if result != -1 else "Not found")
        elif choice == "7":
            text = input("Enter the text: ")
            ch = input("Enter the character to find: ")
            result = xstrchr(text, ch)
            if result is not None:
                print("First occurrence at:", result if result != -1 else "Not found")
        elif choice == "8":
            cmd = input("Enter the command to run: ")
            wait = input("Wait for the command to finish? (Y/N): ").lower()
            wait = wait == "y" or wait == "yes"
            status = xsystem(cmd, wait)
            if status is not None:
                print("Command executed successfully." if status == 0 else "Command execution failed.")
        elif choice == "9":
            str1 = input("Enter the first string: ")
            str2 = input("Enter the second string: ")
            length = int(input("Enter the length of comparison: "))
            result = xmemcmpi(str1, str2, length)
            if result is not None:
                print("Strings are equal." if result == 0 else "Strings are not equal.")
        elif choice == "10":
            str1 = input("Enter the first string: ")
            str2 = input("Enter the second string: ")
            length = int(input("Enter the length of comparison: "))
            result = xstrncmp(str1, str2, length)
            if result is not None:
                print("Strings are equal." if result == 0 else "Strings are not equal.")
        elif choice == "11":
            text = input("Enter the HTML text: ")
            result, found = html_replace(text)
            if result is not None:
                print("Replaced {} HTML entities.".format(found))
                print("Modified HTML text:", result)
        elif choice == "12":
            text = input("Enter the HTML text: ")
            result, found = html_replace2(text)
            if result is not None:
                print("Replaced {} HTML entities.".format(found))
                print("Modified HTML text:", result)
        elif choice == "13":
            status = is_online()
            print("You are online." if status else "You are offline.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
