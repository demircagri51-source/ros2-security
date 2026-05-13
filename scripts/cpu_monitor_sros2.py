import psutil
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

DURATION = 30  # 30 saniyelik test
INTERVAL = 0.5
SAMPLES = int(DURATION / INTERVAL)

cpu_data = []
ram_data = []
timestamps = []

print(f"🔍 [SROS2 AKTIF] Donanim Yuku (CPU/RAM) Olculuyor...")
print(f"⏱️ Hedeflenen Sure: {DURATION} saniye | Orneklem Sayisi (n): {SAMPLES}")
print("-" * 50)

# İlk çağrı ısınma içindir
psutil.cpu_percent(interval=None)
time.sleep(0.1)

start_time = time.time()

for i in range(SAMPLES):
    current_time = time.time() - start_time
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    
    cpu_data.append(cpu)
    ram_data.append(ram)
    timestamps.append(current_time)
    
    print(f"[{i+1}/{SAMPLES}] Zaman: {current_time:.1f}s | CPU: %{cpu:.1f} | RAM: %{ram:.1f}")
    time.sleep(INTERVAL)

print("-" * 50)
print("✅ Veri Toplama Tamamlandi. Istatistikler Hesaplaniyor...")

def print_stats(name, data):
    n = len(data)
    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)
    ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=stats.sem(data))
    
    print(f"\n📊 --- SROS2 {name} METRIKLERI ---")
    print(f"Ortalama (Mean)     : % {mean:.2f}")
    print(f"Medyan (Median)     : % {median:.2f}")
    print(f"Standart Sapma      : % {std_dev:.2f}")
    print(f"%95 Guven Araligi   : % {ci[0]:.2f} - {ci[1]:.2f}")

print_stats("CPU", cpu_data)
print_stats("RAM", ram_data)

plt.figure(figsize=(10, 5))
plt.plot(timestamps, cpu_data, label='CPU Kullanim (%)', color='crimson', linewidth=2)
plt.plot(timestamps, ram_data, label='RAM Kullanim (%)', color='darkblue', linewidth=2)

plt.title('SROS2 (Zirhli) Sistem Kaynak Kullanimi', fontsize=14, fontweight='bold')
plt.xlabel('Zaman (Saniye)', fontsize=12)
plt.ylabel('Kullanim Yuzdesi (%)', fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()

save_path = os.path.expanduser('~/a9_ws/docs/cpu_ram_sros2_plot.png')
plt.savefig(save_path, dpi=300)
print(f"\n📈 SROS2 CPU/RAM Grafigi kaydedildi: {save_path}")
