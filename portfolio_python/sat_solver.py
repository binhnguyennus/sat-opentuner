from sat_portfolio import *

if __name__ == '__main__':
    parser.add_argument('-id', '--instance-directory', 
        dest = 'instances_dir',
        default = 'instances/sat_lib/',
        help = 'The directory containing instances to be solved.')
    parser.add_argument('-f', '--instance-file',
        dest = 'instances',
        default = 'instance_set_4.txt',
        help = 'The file with the names of the selected instances.')
    parser.add_argument('-s', '--solvers-directory',
        dest = 'solvers_dir',
        default = 'solvers/',
        help = 'The directory containing the solver binaries.')
    parser.add_argument('-rs', '--resource-sharing', nargs = '+',
        dest = 'resource_sharing',
        required = True,
        help = 'A sequence of values in (1,2,5,8,10), one for each solver.')

    args = parser.parse_args()
    solvers_dir = args.solvers_dir
    resource_sharing = [int(s) for s in args.resource_sharing]
    instances_dir = args.instances_dir
    instances = args.instances
    debug = args.debug

    solvers = [(solvers_dir + 'glueSplit/glueSplit_clasp ', ''),
            (solvers_dir + 'Lingeling/lingeling -v ', ''),
            (solvers_dir + 'Lingeling/lingeling -v --druplig ', ''),
            (solvers_dir + 'Sparrow/SparrowToRiss.sh ', ' 1 .'),
            (solvers_dir + 'minisat_blbd/minisat_blbd ', ''),
            (solvers_dir + 'SGSeq/SGSeq.sh ', ''),
            (solvers_dir + 'glucose/glucose ', ''),
            (solvers_dir + 'cryptominisat/cryptominisat ', ''),
            (solvers_dir + 'CCAnrglucose/CCAnr+glucose.sh ', ' 1 1000')]

    portfolio = Portfolio(solvers, instances_dir,
                            instances,
                            resource_sharing,
                            debug)
    portfolio.solve()
