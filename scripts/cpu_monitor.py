import psutil
import time

print("\n🔍 CPU ve RAM Kullanimi Olculuyor (10 Saniye)... Lutfen bekleyin.\n")

cpu_usages = []
ram_usages = []

for i in range(10):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    cpu_usages.append(cpu)
    ram_usages.append(ram)
    print(f"[{i+1}/10] CPU: %{cpu:.1f} | RAM: %{ram:.1f}")

avg_cpu = sum(cpu_usages) / len(cpu_usages)
avg_ram = sum(ram_usages) / len(ram_usages)

print("\n" + "="*40)
print("📈 SISTEM KAYNAK KULLANIMI (ORTALAMA)")
print("="*40)
print(f"Ortalama CPU Yuku : %{avg_cpu:.2f}")
print(f"Ortalama RAM Yuku : %{avg_ram:.2f}")
print("="*40 + "\n")
