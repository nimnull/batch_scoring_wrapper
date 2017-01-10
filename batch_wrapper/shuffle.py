import os
import random
import time

import pandas as pd
from datarobot_batch_scoring.reader import BatchGenerator, SlowReader


REF_NAME = "ref_id"


class ShuffleDS(object):

    def __init__(self, filename, encoding, delimiter, fast_mode, ui):
        self.buffered = []
        batch_gen = BatchGenerator(filename, 1, 1, delimiter, ui, fast_mode,
                                   encoding)

        with batch_gen.csv_input_file_reader() as csvfile:
            self.reader = SlowReader(csvfile, encoding, ui)
            self.reader.fieldnames.append(REF_NAME)
            for num, row in enumerate(self.reader):
                row.append(num)
                self.buffered.append(row)

    def get_shuffled(self):
        shuffled = self.buffered[:]
        random.shuffle(shuffled)
        shuffled = [self.reader.fieldnames] + shuffled
        return shuffled


def compute_divergency(datasets, encoding, ui):
    dataframes = map(pd.DataFrame.from_csv, datasets)
    result = reduce(lambda x, y: pd.merge(x, y, on=REF_NAME, sort=True),
                    dataframes)
    result['diff'] = result['predicted_x'] - result['predicted_y']

    # print(result.select(lambda x: x['diff'] == 0.0))
    filename = 'out.csv'
    name_mod = time.time()
    if os.path.exists(filename):
        do_drop = ui.prompt_yesno("Drop existing %s file?" % filename)
        if do_drop:
            os.unlink(filename)
        else:
            filename = "%d_%s" % (name_mod, filename)
    result.to_csv(filename, encoding=encoding)
    ui.info("Results saved as %s file" % filename)

    diverged = result.loc[result['diff'] != 0]

    if diverged.size != 0:
        filename = 'diverged.csv'
        if os.path.exists(filename):
            do_drop = ui.prompt_yesno("Drop existing %s file?" % filename)
            if do_drop:
                os.unlink(filename)
            else:
                filename = "%d_%s" % (name_mod, filename)

        diverged.to_csv(filename, encoding=encoding)
        ui.info("We have diverged rows. Awailable as %s" % filename)
    else:
        ui.info("First and second pass predictions matched")
