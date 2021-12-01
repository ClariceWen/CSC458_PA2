'''
Plot ping RTTs over time
'''
import os, sys
from helper import *
import plot_defaults

from matplotlib.ticker import MaxNLocator
from pylab import figure

parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    help="Ping output files to plot",
                    required=True,
                    action="store",
                    nargs='+')

parser.add_argument('--freq',
                    help="Frequency of pings (per second)",
                    type=int,
                    default=10)

parser.add_argument('--out', '-o',
                    help="Output png file for the plot.",
                    default=None) # Will show the plot

args = parser.parse_args()

def parse_ping(fname):
    ret = []
    lines = open(fname).readlines()
    num = 0
    sum = 0
    count = 0
    for line in lines:
        if 'bytes from' not in line:
            continue
        try:
            rtt = line.split(' ')[-2]
            rtt = rtt.split('=')[1]
            rtt = float(rtt)
            sum += rtt
            count += 1
            ret.append([num, rtt])
            num += 1
        except:
            break
    print "AVERAGE PING TIME IS: "
    if count > 0:
        print sum/count
    return ret

m.rc('figure', figsize=(16, 6))
fig = figure()
ax = fig.add_subplot(111)
for i, f in enumerate(args.files):
    data = parse_ping(f)
    if len(data) == 0:
        print >>sys.stderr, "%s: error: no ping data"%(sys.argv[0])
        sys.exit(1)

    xaxis = map(float, col(0, data))
    start_time = xaxis[0]
    xaxis = map(lambda x: (x - start_time) / args.freq, xaxis)
    qlens = map(float, col(1, data))

    ax.scatter(xaxis, qlens, lw=2)
    ax.xaxis.set_major_locator(MaxNLocator(4))

plt.ylabel("RTT (ms)")
plt.grid(True)

if args.out:
    plt.savefig(args.out)
else:
    plt.show()


def parse_download_time(fname):
    """parse into float"""
    download_times = []
    lines = open(fname).readlines()
    num = 0
    for line in lines:
        download_times.append(float(line))
    return download_times

m.rc('figure', figsize=(16, 6))
fig = figure()
ax = fig.add_subplot(111)
for i, f in enumerate(args.dfiles):
    data = parse_download_time(f)
    if len(data) == 0:
        print >>sys.stderr, "%s: error: no download time data"%(sys.argv[0])
        sys.exit(1)

    ax.scatter(range(1, len(data) + 1), data, lw=2)
    ax.xaxis.set_major_locator(MaxNLocator(4))

plt.ylabel("(curl) Download Time (ms)")
plt.grid(True)

if args.dout:
    plt.savefig(args.dout)
else:
    plt.show()
