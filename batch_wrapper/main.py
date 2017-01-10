import csv
import itertools
import logging
import os
import subprocess
import sys
import tempfile

from .argparser import get_parsed_args
from .shuffle import REF_NAME, ShuffleDS, compute_divergency


SHUFFLE_FACTOR = 2  # do not change this factor for now
# ORD_BASE = 97


def main(argv=sys.argv[1:]):
    parsed_args = get_parsed_args(argv)

    loglevel = logging.DEBUG if parsed_args['verbose'] else logging.INFO

    subprocess.check_output(["pip install datarobot_batch_scoring"],
                            stderr=subprocess.STDOUT, shell=True)

    from datarobot_batch_scoring.reader import (
        investigate_encoding_and_dialect
    )
    from datarobot_batch_scoring.utils import UI

    stdout = parsed_args['stdout']
    dataset = parsed_args.pop('dataset')
    delimiter = parsed_args.get('delimiter')
    fast_mode = parsed_args['fast']
    encoding = parsed_args['encoding']
    skip_dialect = parsed_args['skip_dialect']
    output_delimiter = parsed_args.get('output_delimiter')
    keep_cols = parsed_args.pop('keep_cols', '')

    ui = UI(parsed_args.get('prompt'), loglevel, stdout)
    if not os.path.exists(dataset):
        ui.fatal('file %s does not exist.' % dataset)
    argnames = filter(lambda k: parsed_args[k], parsed_args)
    include_args = dict((arg, parsed_args[arg]) for arg in argnames)

    project_id = include_args.pop('project_id')
    model_id = include_args.pop('model_id')
    out = include_args.pop('out')
    user = include_args.get('user')
    api_token = include_args.get('api_token')
    passwd = include_args.get('password')
    # preliminary checks to avoid manual input
    if not user:
        ui.fatal("--user not specified")
    if not api_token and not passwd:
        ui.fatal("You need to specify either --password or --api_token")
    # flags parsed in a different way
    true_args = filter(lambda k: parsed_args[k] is True, parsed_args)
    # unparse arguments
    arg_string = [['--%s' % key, value] for key, value in include_args.items()
                  if key not in true_args]
    merged_args = list(itertools.chain.from_iterable(arg_string))
    # set args that have only mentions (no values)
    for argname in true_args:
        merged_args.append('--%s' % argname)
    # we renamed prompt so it should get back it's original way
    merged_args.append('-y')

    keep_cols = keep_cols.split(',')

    if REF_NAME not in keep_cols:
        keep_cols = filter(lambda arg: bool(arg), keep_cols)
        keep_cols.append(REF_NAME)

    merged_args += ['--keep_cols', ",".join(keep_cols),
                    '--pred_name', 'predicted']

    encoding = investigate_encoding_and_dialect(
        dataset=dataset,
        sep=delimiter,
        ui=ui,
        fast=fast_mode,
        encoding=encoding,
        skip_dialect=skip_dialect,
        output_delimiter=output_delimiter
    )

    writer_dialect = csv.get_dialect('dataset_dialect')
    output = []
    shuffler = ShuffleDS(dataset, encoding, delimiter, fast_mode, ui)

    for stage in range(SHUFFLE_FACTOR):
        shuffled = shuffler.get_shuffled()

        _, shuf_input = tempfile.mkstemp(suffix='.csv')
        _, shuf_output = tempfile.mkstemp(suffix='.csv')

        output.append(shuf_output)

        with open(shuf_input, 'wb') as fp:
            writer = csv.writer(fp, dialect=writer_dialect)
            writer.writerows(shuffled)
        pass_args = merged_args + ['--out', shuf_output, project_id, model_id,
                                   shuf_input]
        # display merged arguments
        ui.info("Scoring on %s shuffled file: %s" % (stage + 1, shuf_input))

        command = " ".join(map(unicode, ['batch_scoring'] + pass_args))
        ui.info(command)
        try:
            out = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                          shell=True)
        except subprocess.CalledProcessError as ex:
            out = ex.output
        finally:
            os.unlink(shuf_input)
        ui.info(out)

    compute_divergency(output, encoding, ui)

    for filename in output:
        if os.path.exists(filename):
            os.unlink(filename)


if __name__ == "__main__":
    main()
