import matplotlib.pyplot as plt
import numpy as np


def gen_data(n, start=0, end=10):
    x = np.linspace(start, end, n)
    y = np.sin(10*x) - x*x
    return y

def gen_data_osc(n):
    return np.array([1024 + (-2)**(-i/100) for i in range(n)])

def gen_data_rand(n):
    return np.random.randn(n) + 0.3*np.linspace(0, 10, n)

def calc_cov(X, Y):
    return np.sum((X - np.average(X))*(Y - np.average(Y))) / (X.shape[0] - 1)

def angular_coef(X,Y):
    return calc_cov(X,Y)/calc_cov(X,X)

def linear_coef(a, X, Y):
    return np.average(Y) - a*np.average(X)

def kg_coef(est, measurement):
    return est / (est + measurement)

def kg_iter(prev, measurement):
    return prev + kg_coef(prev, measurement) * (measurement - prev)

count = 100
end = 100
time = np.linspace(0, end, count)
data = gen_data_osc(count)

delta = end / count

preds = []
kg_preds = []

kg_prediction = 0

mem_size=20
memory = []
time_mem = []

for i in range(1, count):
    if i == 1:
        memory.append(data[i])
        time_mem.append(time[i])
    if len(memory) >= mem_size:
        del memory[0]
        del time_mem[0]

    memory.append(data[i])
    time_mem.append(time[i])

    a = angular_coef(np.array(time_mem), np.array(memory))
    b = linear_coef(a, np.array(time_mem), np.array(memory))

    prediction = (time[i]+delta)*a + b
    kg_prediction = kg_iter(prediction, data[i])
    preds.append(prediction)
    kg_preds.append(kg_prediction)

estimate = time*a + b

plt.scatter(time, data, label="Medições", color="#FF5850")
plt.scatter(time[1:], preds, label="Est. Min. Quad.", color="#62B21C")
plt.scatter(time[1:], kg_preds, label="Est. Kalman", color="#C000FF")
plt.plot(time, estimate, label="Min. Quad. Final", color="#36A1FF")
plt.xlabel("Tempo")
plt.ylabel("Temperatura")
plt.title("Aproximaçao por Kalman Filter com Memória Limitada (%i elementos)" % mem_size)
# Place a legend to the right of this smaller subplot.
plt.legend()

plt.show()