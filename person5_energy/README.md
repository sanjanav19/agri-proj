# Person 5 - Energy Measurement

## Purpose
This folder contains the energy measurement work for the FLyer project.

## Experiment
The first measured experiment is the existing Person 3 Federated LSTM implementation.

Configuration:
- Clients: 4
- Federated rounds: 20
- Local epochs: 5
- Batch size: 32
- Seed: 42

## Hardware and Platform
- Operating system: Windows 10 Home Single Language
- Processor: Intel(R) Core(TM) Ultra 7 155U

## Measurement Method
Energy was measured using the Windows Energy Meter counter:

`\Energy Meter(RAPL_Package0_PKG)\Energy`

The cumulative energy counter was read immediately before and after the experiment. The difference was converted to joules.

The measurement represents RAPL package energy and should not be interpreted as CPU-only or whole-system energy.

## Measured Result

| Experiment | Execution Time (s) | Average Power (W) | Energy (J) | Measurement |
|---|---:|---:|---:|---|
| Federated LSTM | 275.022 | 5.654 | 1555.071 | Measured |

## Limitations
- This result is based on one measured Federated LSTM run.
- Centralized LSTM and Edge-Cloud LSTM energy measurements have not yet been performed.
- Encryption energy has not been measured because an encryption-enabled experiment has not yet been provided.
- No charger wattage or CPU TDP value was used as a substitute for measured energy.
- Person 3 training code was not modified for the energy measurement.

## Files
- `energy_measurement.py` - energy measurement script
- `energy_results.csv` - measured energy result
- `README.md` - documentation
