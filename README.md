# Computational Modeling of Epileptic Signals

This repository contains the code used for the master's thesis  
**"Computational Modeling of Epileptic Signals"** by Lydia Marie Lindgren (2025), submitted at NMBU.

The project investigates how rhythmic synaptic input in a single neuron can scale to measurable extracellular potentials, such as those observed in SEEG recordings during epileptic seizures.

## Tools and Frameworks

The simulations in this project were implemented using:

- **[LFPy](https://github.com/LFPy/LFPy)** – a Python package built on top of the NEURON simulator, used for simulating extracellular potentials based on detailed neuron models.
- **[ElectricBrainSignals](https://github.com/LFPy/ElectricBrainSignals)** – a collection of example scripts and resources developed by the LFPy team, which served as a foundation for parts of this project’s signal analysis workflow.
- **EBRAINS Collaboratory** – the simulations were executed in the [EBRAINS Collaboratory](https://ebrains.eu/service/collaboratory), which provides a pre-configured computing environment with all necessary dependencies for running LFPy and NEURON-based simulations without local installation issues.

All figures used in the thesis were generated using scripts contained in this repository.

## Notes

- This model uses a simplified population geometry and assumes fixed synaptic input patterns.
- All figures are reproducible with the provided random seed; changing the seed will produce alternate but qualitatively similar outputs.
  - Change the input of `np.random.seed(123)` to generate figures with new, randomized data. 
  
