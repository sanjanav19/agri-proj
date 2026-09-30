import csv
import sys
import subprocess
import time
from pathlib import Path

ENERGY_COUNTER = r"\Energy Meter(RAPL_Package0_PKG)\Energy"
OUTPUT_CSV = Path(__file__).parent / "energy_results.csv"


def read_energy():
    result = subprocess.run(
        ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "-NoProfile", "-Command",
         f"(Get-Counter '{ENERGY_COUNTER}').CounterSamples[0].CookedValue"],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def run_experiment():
    command = [
        sys.executable,
        r"person3_federated\federated_training.py",
    ]

    energy_before = read_energy()
    start_time = time.perf_counter()

    subprocess.run(command, check=True)

    execution_time = time.perf_counter() - start_time
    energy_after = read_energy()

    raw_energy_difference = energy_after - energy_before

    # Windows Energy Meter/RAPL package energy is reported in pWh.
    energy_joules = raw_energy_difference * 3.6e-9
    average_power = energy_joules / execution_time if execution_time > 0 else 0.0

    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "experiment",
                "execution_time_seconds",
                "average_power_watts",
                "energy_joules",
                "measurement_type",
                "measurement_method",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "experiment": "Federated LSTM",
                "execution_time_seconds": execution_time,
                "average_power_watts": average_power,
                "energy_joules": energy_joules,
                "measurement_type": "measured",
                "measurement_method": "Windows Energy Meter RAPL_Package0_PKG cumulative energy",
            }
        )

    print(f"Execution time: {execution_time:.3f} seconds")
    print(f"Energy difference: {raw_energy_difference:.0f} pWh")
    print(f"Energy: {energy_joules:.3f} J")
    print(f"Average power: {average_power:.3f} W")
    print(f"Results saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    run_experiment()
