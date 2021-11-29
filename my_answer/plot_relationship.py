import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def get_ping_vals(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        ret = []
        num = 0
        for line in lines:
            if 'bytes from' not in line:
                continue
            try:
                rtt = line.split(' ')[-2]
                rtt = rtt.split('=')[1]
                rtt = float(rtt)
                ret.append(rtt)
            except:
                break
        return np.array(ret)

plt.figure(figsize=(8, 6))
# plt.style.use("seaborn")
qs = np.array([5, 20, 100])
filenames = ["./bb-q5/ping.txt", "./bb-q20/ping.txt", "./bb-q100/ping.txt"]
rtts = np.array([np.mean(get_ping_vals(i)) for i in filenames])

slope, intercept, r_value, p_value, std_err = stats.linregress(qs, rtts)
plt.scatter(qs, rtts, s=100, label="Observations")
for x, y in zip(qs, rtts):
    text = '(' + str(x) + ', {:.2f})'.format(y)
    plt.text(x - 10, y - 10, text)
 
plt.plot(
    np.arange(0, 101), 
    np.arange(0, 101) * slope + intercept, 
    label="Fitted Line via Linear Regression \n$RTT$" + 
          "$= {:.2f} + {:.2f} \\times qsize$\np-val = {:.2f}, r = {:.2f}, stderr = {:.2f}".format(
              intercept, slope, p_value, r_value, std_err)
)

plt.title("Relatinship between RTT and Queue size", size=18)
plt.xlabel("queue size", size=14)
plt.ylabel("rtt time in average (ms)", size=14)
plt.legend(loc="best")
plt.savefig("./fit.pdf")