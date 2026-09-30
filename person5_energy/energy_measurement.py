import csv
import sys
import subprocess
import time
from pathlib import Path

ENERGY_COUNTER = r"\Energy Meter(RAPL_Package0_PKG)\Energy"
OUTPUT_CSV = Path(__file__).parent / "energy_results.csv"


def read_energy():
    result = subprocess.run(
        [
            r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            "-NoProfile",
            "-Command",
            f"(Get-Counter '{ENERGY_COUNTER}').CounterSamples[0].CookedValue",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def write_result(experiment, execution_time, power, energy):
    fieldnames = [
        "experiment",
        "execution_time_seconds",
        "average_power_watts",
        "energy_joules",
        "measurement_type",
        "measurement_method",
    ]

    rows = []
    if OUTPUT_CSV.exists():
        with OUTPUT_CSV.open("r", newline="") as f:
            rows = list(csv.DictReader(f))

    rows = [r for r in rows if r["experiment"] != experiment]

    rows.append({
        "experiment": experiment,
        "execution_time_seconds": execution_time,
        "average_power_watts": power,
        "energy_joules": energy,
        "measurement_type": "measured",
        "measurement_method": "Windows Energy Meter RAPL_Package0_PKG cumulative energy",
    })

    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_experiment():
    command = [
        sys.executable,
        r"person2_lstm\train_lstm.py",
    ]

    energy_before = read_energy()
    start_time = time.perf_counter()

    subprocess.run(command, check=True)

    execution_time = time.perf_counter() - start_time
    energy_after = read_energy()

    raw_difference = energy_after - energy_before
    energy_joules = raw_difference * 3.6e-9
    average_power = energy_joules / execution_time

    write_result(
        "Centralized LSTM",
        execution_time,
        average_power,
        energy_joules,
    )

    print(f"Execution time: {execution_time:.3f} seconds")
    print(f"Energy difference: {raw_difference:.0f} pWh")
    print(f"Energy: {energy_joules:.3f} J")
    print(f"Average power: {average_power:.3f} W")
    print(f"Results saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    run_experiment()
