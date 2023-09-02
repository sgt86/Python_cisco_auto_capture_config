import paramiko
from netmiko import ConnectHandler

# Minta username dan password dari pengguna
username = input("Masukkan username: ")
password = input("Masukkan password: ")

# Baca alamat IP router dari file ipaddress.txt
with open("ip_address.txt", "r") as file:
    ip_addresses = file.read().splitlines()

# Iterasi melalui daftar alamat IP router
for ip_address in ip_addresses:
    try:
        # Konfigurasi koneksi SSH menggunakan Paramiko
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip_address, username=username, password=password)

        # Menggunakan Netmiko untuk mengelola koneksi SSH
        device = {
            "device_type": "cisco_ios",
            "ip": ip_address,
            "username": username,
            "password": password,
        }
        net_connect = ConnectHandler(**device)

        # Mengumpulkan data sh run, sh inventory, dan sh version
        sh_run_output = net_connect.send_command("show running-config")
        sh_inventory_output = net_connect.send_command("show inventory")
        sh_version_output = net_connect.send_command("show version")

        # Mengambil hostname dari sh version
        hostname = net_connect.find_prompt()[:-1]

        # Menyimpan hasil dalam file teks dengan nama hostname.txt
        with open(f"{hostname}.txt", "w") as output_file:
            output_file.write(f"Hostname: {hostname}\n\n")
            output_file.write("=== Show Running Configuration ===\n")
            output_file.write(sh_run_output)
            output_file.write("\n\n=== Show Inventory ===\n")
            output_file.write(sh_inventory_output)
            output_file.write("\n\n=== Show Version ===\n")
            output_file.write(sh_version_output)

        print(f"Data dari {hostname} telah dikumpulkan dan disimpan dalam {hostname}.txt")
    except Exception as e:
        print(f"Gagal mengumpulkan data dari {ip_address}: {str(e)}")
    finally:
        # Tutup koneksi SSH
        ssh_client.close()
