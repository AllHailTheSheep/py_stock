def save(array):
    import numpy as np
    np.savetxt(array)


def firefox_proc_daemon(name):
    import psutil
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == name:
            proc.kill()
