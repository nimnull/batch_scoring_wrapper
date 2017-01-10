import argparse


def get_parsed_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='Provides status updates while '
                        'the script is running.')

    dataset_gr = parser.add_argument_group('Dataset and server')
    dataset_gr.add_argument('--host', type=str,
                            help='Specifies the protocol (http or https) and '
                                 'hostname of the prediction API endpoint. '
                                 'E.g. "https://example.orm.datarobot.com"')
    dataset_gr.add_argument('project_id', type=str,
                            nargs='?',
                            help='Specifies the project '
                            'identification string.')
    dataset_gr.add_argument('model_id', type=str,
                            nargs='?',
                            help='Specifies the model identification string.')
    dataset_gr.add_argument('dataset', type=str,
                            help='Specifies the .csv input file that '
                            'the script scores.')
    dataset_gr.add_argument('--out', type=str,
                            nargs='?', default='out.csv',
                            help='Specifies the file name, '
                            'and optionally path, '
                            'to which the results are written. '
                            'If not specified, '
                            'the default file name is out.csv, '
                            'written to the directory containing the script. '
                            '(default: %(default)r)')
    auth_gr = parser.add_argument_group('Authentication parameters')
    auth_gr.add_argument('--user', type=str,
                         help='Specifies the username used to acquire '
                         'the api-token. '
                         'Use quotes if the name contains spaces.')
    auth_gr.add_argument('--password', type=str, nargs='?',
                         help='Specifies the password used to acquire '
                         'the api-token. '
                         'Use quotes if the name contains spaces.')
    auth_gr.add_argument('--api_token', type=str, nargs='?',
                         help='Specifies the api token for the requests; '
                         'if you do not have a token, '
                         'you must specify the password argument.')
    auth_gr.add_argument('--create_api_token', action="store_true",
                         default=False,
                         help='Requests a new API token. To use this option, '
                         'you must specify the '
                         'password argument for this request '
                         '(not the api_token argument). '
                         '(default: %(default)r)')
    auth_gr.add_argument('--datarobot_key', type=str,
                         nargs='?',
                         help='An additional datarobot_key '
                         'for dedicated prediction instances.')
    conn_gr = parser.add_argument_group('Connection control')
    conn_gr.add_argument('--timeout', type=int,
                         default=30,
                         help='The timeout for each post request. '
                         '(default: %(default)r)')
    conn_gr.add_argument('--n_samples', type=int,
                         nargs='?',
                         default=False,
                         help='DEPRECATED. Specifies the number of samples '
                              '(rows) to use per batch. If not defined the '
                              '"auto_sample" option will be used.')
    conn_gr.add_argument('--n_concurrent', type=int,
                         nargs='?',
                         default=4,
                         help='Specifies the number of concurrent requests '
                         'to submit. (default: %(default)r)')
    conn_gr.add_argument('--n_retry', type=int,
                         default=3,
                         help='Specifies the number of times DataRobot '
                         'will retry if a request fails. '
                         'A value of -1 specifies an infinite '
                         'number of retries. (default: %(default)r)')
    conn_gr.add_argument('--resume', action='store_true',
                         default=False,
                         help='Starts the prediction from the point at which '
                         'it was halted. '
                         'If the prediction stopped, for example due '
                         'to error or network connection issue, you can run '
                         'the same command with all the same '
                         'all arguments plus this resume argument.')
    conn_gr.add_argument('--compress', action='store_true',
                         default=False,
                         help='Compress batch. This can improve throughout '
                              'when bandwidth is limited.')
    csv_gr = parser.add_argument_group('CVS parameters')
    csv_gr.add_argument('--keep_cols', type=str,
                        nargs='?',
                        help='Specifies the column names to append '
                        'to the predictions. '
                        'Enter as a comma-separated list.')
    csv_gr.add_argument('--delimiter', type=str,
                        nargs='?', default=None,
                        help='Specifies the delimiter to recognize in '
                        'the input .csv file. E.g. "--delimiter=,". '
                        'If not specified, the script tries to automatically '
                        'determine the delimiter. The special keyword "tab" '
                        'can be used to indicate a tab delimited csv. "pipe"'
                        'can be used to indicate "|"')
    csv_gr.add_argument('--pred_name', type=str,
                        nargs='?', default=None,
                        help='Specifies column name for prediction results, '
                        'empty name is used if not specified. For binary '
                        'predictions assumes last class in lexical order '
                        'as positive')
    csv_gr.add_argument('--fast', action='store_true',
                        default=False,
                        help='Experimental: faster CSV processor. '
                        'Note: does not support multiline csv. ')
    csv_gr.add_argument('--auto_sample', action='store_true',
                        default=False,
                        help='Override "n_samples" and instead '
                        'use chunks of about 1.5 MB. This is recommended and '
                        'enabled by default if "n_samples" is not defined.')
    csv_gr.add_argument('--encoding', type=str,
                        default='', help='Declare the dataset encoding. '
                        'If an encoding is not provided the batch_scoring '
                        'script attempts to detect it. E.g "utf-8", "latin-1" '
                        'or "iso2022_jp". See the Python docs for a list of '
                        'valid encodings '
                        'https://docs.python.org/3/library/codecs.html'
                        '#standard-encodings')
    csv_gr.add_argument('--skip_dialect', action='store_true',
                        default=False, help='Tell the batch_scoring script '
                        'to skip csv dialect detection.')
    csv_gr.add_argument('--skip_row_id', action='store_true', default=False,
                        help='Skip the row_id column in output.')
    csv_gr.add_argument('--output_delimiter', type=str, default=None,
                        help='Set the delimiter for output file.The special '
                             'keyword "tab" can be used to indicate a tab '
                             'delimited csv. "pipe" can be used to indicate '
                             '"|"')
    misc_gr = parser.add_argument_group('Miscellaneous')
    misc_gr.add_argument('-y', '--yes', dest='prompt', action='store_true',
                         help="Always answer 'yes' for user prompts")
    misc_gr.add_argument('-n', '--no', dest='prompt', action='store_false',
                         help="Always answer 'no' for user prompts")
    misc_gr.add_argument('--dry_run', dest='dry_run', action='store_true',
                         help="Only read/chunk input data but dont send "
                         "requests.")
    misc_gr.add_argument('--stdout', action='store_true', dest='stdout',
                         default=False,
                         help='Send all log messages to stdout.')
    misc_gr.add_argument('--scoring_ver', type=str, default=None)

    defaults = {
        'prompt': None,
        'out': 'out.csv',
        'create_api_token': False,
        'timeout': 30,
        'n_samples': False,
        'n_concurrent': 4,
        'n_retry': 3,
        'resume': False,
        'fast': False,
        'stdout': False,
        'auto_sample': False,
    }
    parser.set_defaults(**defaults)

    for action in parser._actions:
        if action.dest in defaults and action.required:
            action.required = False
            if '--' + action.dest not in argv:
                action.nargs = '?'

    parsed_args = {k: v
                   for k, v in vars(parser.parse_args(argv)).items()
                   if v is not None}
    return parsed_args
