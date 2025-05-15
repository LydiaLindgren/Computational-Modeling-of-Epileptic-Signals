import numpy as np
import brainsignals.neural_simulations as ns
import numpy as np
import LFPy
from lfpykit.models import CurrentDipoleMoment
from elephant.spike_train_generation import inhomogeneous_poisson_process
from quantities import Hz, ms
import neo

def syn_rate(tvec, dt, freq, avrg_rate, phase=0):
    """Return synaptic rate profile
       Parameters
       ----------
       tvec : array [ms]
       freq : float [Hz]
       avrg_rate : float [Hz]
       phase : float [radians]
           A phase shift of 180 degrees needs np.pi as input.

       Returns
       -------
       rate_syn : array
           array containing the time development of the synaptic
           firing rates
    """
    rate_signal = np.sin(2 * np.pi * freq * tvec / 1000 + phase) + 1.01
    rate_syn = neo.AnalogSignal(np.array(rate_signal)  * avrg_rate * Hz,
                                sampling_rate=(1/dt * 1000)* Hz,
                                t_stop=tvec[-1] * ms)
    return rate_syn


def synapses_locs(cell, z_min, z_max, ndix):
    """Return synapse locations
       Parameters
       __________
       cell : LFPy object
       z_min : float [µm]
       z_max : float [µm]
       ndix : int

       Returns
       _______
       synapse locations
    """
    return cell.get_rand_idx_area_norm(z_min=z_min, z_max=z_max, nidx=ndix)


def synapse_params(reversal_potential):
    synapse_params = {
        'e' : reversal_potential,    # reversal potential
        'syntype' : 'Exp2Syn',       # synapse type
        'tau1' : 0.1,                # synaptic time constant
        'tau2' : 1.,                 # synaptic time constant
        'weight' : 0.001,            # synaptic weight
        'record_current' : False,    # record synapse current
        }

    return synapse_params

def amp_FT(tvec, signal, freq):
    freqs_cdms_sum, cdms_sum_psd = ns.return_freq_and_amplitude(tvec, signal)
    freq_idx = np.argmin(abs(freqs_cdms_sum - freq))
    
    # freq should be equal to freqs_cdms_sum[freq_idx]
    print(freqs_cdms_sum[freq_idx], cdms_sum_psd[0][freq_idx])
    
    return freqs_cdms_sum[freq_idx], cdms_sum_psd[0][freq_idx]

def baseline_model(synidxs_ex, synidxs_in, syn_rate_0, syn_rate_pi, tstop, dt):
    cell = ns.return_hay_cell(tstop, dt, make_passive=False)

    # Simultaneous input
    synapse_params_ex = synapse_params(0)
    synapse_params_in = synapse_params(-90)

    # Excitatory
    for synidx in synidxs_ex:
        synapse_params_ex["idx"] = synidx
        synapse = LFPy.Synapse(cell, **synapse_params_ex)
        spiketimes_rate = inhomogeneous_poisson_process(syn_rate_0 * 1.2)

        synapse.set_spike_times(np.array(spiketimes_rate)*1000)

    # Inhibitory
    for s_, synidx in enumerate(synidxs_in):
        synapse_params_in["idx"] = synidx
        synapse = LFPy.Synapse(cell, **synapse_params_in)
        spiketimes_rate = inhomogeneous_poisson_process(syn_rate_pi * 1.2)

        synapse.set_spike_times(np.array(spiketimes_rate)*1000)

    cell.simulate(rec_imem=True, rec_vmem=True)
    
    mps = cell.vmem[0, -len(cell.tvec):]
    cdms = CurrentDipoleMoment(cell).get_transformation_matrix() @ cell.imem
    
    del cell
    del synapse
    return cdms, mps

# def alternative_model()
