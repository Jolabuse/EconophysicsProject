import pandas as pd
import math
import matplotlib.pyplot as plt

df = pd.read_csv("AMZN.csv")

df = df.iloc[:,[0,1]]
dates = pd.to_datetime(df["Date"])
df["Date"] = dates
df.sort_values(by="Date", inplace=True)
df.set_index("Date", inplace=True)
print(df)

#ex 5.1.1
df_0 = df[pd.to_datetime('2019-01-02', format="%Y-%m-%d"):pd.to_datetime('2019-01-15', format="%Y-%m-%d")]
#two first week
x0 = df_0.mean()
print("x0 = ",x0)

#ex 5.1.2
df_inf = df[pd.to_datetime('2020-12-15', format="%Y-%m-%d"):pd.to_datetime('2020-12-30', format="%Y-%m-%d")]
#two last week
xinf = df_inf.mean()
print("xinf = ",xinf)

#ex 5.1.3

var_inf = df_inf.var()
print("var_inf = ",var_inf)

#ex5.1.4

def a(t,k,x0,xinf):
    return (x0-xinf)*math.exp(-k*t)+xinf

k = 1.82
plt_df = []
for i in range(len(df)):
    plt_df.append(a(i,k,x0, xinf))
plt_df = pd.DataFrame(plt_df,index=dates)
print(plt_df)

plt.plot(plt_df)
plt.plot(df)

#ex5.1.5
sigma_inf = df_inf.std()
print("sigma inf = ",sigma_inf)

#ex5.1.6
def sigma(x0,xinf,t,k, D) :
    return math.sqrt((2*x0-xinf)*xinf*math.exp(-2*k*t)+D/k)

D = 13.36
plt_df_pos = [math.sqrt(D/k)]
for i in range(1,len(plt_df)):
    plt_df_pos.append(plt_df["Open"][i]+sigma(x0,xinf,i,k, D))

plt_df_pos = pd.DataFrame(plt_df_pos,index=dates)

plt_df_neg = [math.sqrt(D/k)]
for i in range(1,len(plt_df)):
    plt_df_neg.append(plt_df["Open"][i] - sigma(x0,xinf,i,k, D))

plt_df_neg = pd.DataFrame(plt_df_neg, index=dates)

plt.plot(plt_df_pos)
plt.plot(plt_df_neg)
plt.title("Means + SD")
plt.show()

#5.2.1

df = df[pd.to_datetime('2009-03-06'):]
dates = dates[22:len(dates)]


def moving_average(df,t):
    month_df = df["Open"][t:(t+22)] #we add 22 as it represents a delay of one month
    return month_df.mean()

moving_average_df = []

for t in range(len(df)-22):
    moving_average_df.append(moving_average(df,t))


moving_average_df = pd.DataFrame(moving_average_df, index=dates)


plt.plot(moving_average_df)
plt.title("Moving average")
plt.show()

#5.2.2
def moving_variance(df,t):
    month_df = df["Open"][t:(t+22)] #we add 22 as it represents a delay of one month
    return month_df.var()

moving_variance_df = []

for t in range(len(df)-22):
    moving_variance_df.append(moving_variance(df,t))



moving_variance_df = pd.DataFrame(moving_variance_df, index=dates)


plt.plot(moving_variance_df)
plt.title("Moving variance")
plt.show()

#5.2.3
exceed_30 = []

x0 = moving_variance_df[0][0]

for i in range(len(moving_variance_df)):
    if moving_variance_df[0][i] > 30:
        exceed_30.append(i)


x_exceed_df =[]
for i in exceed_30:
    x_exceed_df.append(moving_variance_df[0][i])
print(x_exceed_df)

def get_x_inf(x0,k,t,x_mean):
    return (x0*math.exp(-k*t)-x_mean)/(math.exp(-k*t)-1)

x_inf_df = []
for i in range(len(exceed_30)):
    t = exceed_30[i]
    x_inf_df.append(get_x_inf(x0,k,t,moving_average_df[0][t]))

print(x_inf_df)


#5.2.4
exceed_10 = []
for i in range(len(moving_variance_df)):
    if moving_variance_df[0][i] > 10:
        exceed_10.append(i)
print(exceed_10)
