import numpy as np


def log_threshold(prf, pul_dur, v):
    if v == 0:
        return np.log10(7.1e-4*np.sqrt(prf*pul_dur) * (2*np.tanh(3.52/(prf*pul_dur))/1.76) *
                        np.sqrt(-3*1.76/(2*np.tanh(3.52/(prf*pul_dur)) * ((np.tanh(3.52/(prf*pul_dur)))**2-3))))
    elif v == 1:
        return np.log10(3.3e-4*np.sqrt(prf*pul_dur) * (2*np.tanh(3.52/(prf*pul_dur))/1.76) *
                        np.sqrt(-3*1.76/(2*np.tanh(3.52/(prf*pul_dur)) * ((np.tanh(3.52/(prf*pul_dur)))**2-3))))
    elif v == 2:
        return np.log10(2.8e-4*np.sqrt(prf*pul_dur) * (2*np.tanh(3.52/(prf*pul_dur))/1.76) *
                        np.sqrt(-3*1.76/(2*np.tanh(3.52/(prf*pul_dur)) * ((np.tanh(3.52/(prf*pul_dur)))**2-3))))
    else:
        return 0
    
    
def threshold(prf, pul_dur, v):
    if v == 0:
        return 7.1e-4*np.sqrt(prf*pul_dur) * (2*np.tanh(3.52/(prf*pul_dur))/1.76) * \
            np.sqrt(-3*1.76/(2*np.tanh(3.52/(prf*pul_dur)) * ((np.tanh(3.52/(prf*pul_dur)))**2-3)))
    elif v == 1:
        return 3.3e-4*np.sqrt(prf*pul_dur) * (2*np.tanh(3.52/(prf*pul_dur))/1.76) * \
            np.sqrt(-3*1.76/(2*np.tanh(3.52/(prf*pul_dur)) * ((np.tanh(3.52/(prf*pul_dur)))**2-3)))
    elif v == 2:
        return 2.8e-4*np.sqrt(prf*pul_dur) * (2*np.tanh(3.52/(prf*pul_dur))/1.76) * \
            np.sqrt(-3*1.76/(2*np.tanh(3.52/(prf*pul_dur)) * ((np.tanh(3.52/(prf*pul_dur)))**2-3)))
    else:
        return 0
