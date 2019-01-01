import pickle as pl


def save_data(data, log_file_name='log.dat'):
    f = open(log_file_name, 'wb')
    pl.dump(data, f)
    f.close()


def get_data(log_file_name='log.dat'):
    f = open(log_file_name, 'rb')
    return pl.load(f)
