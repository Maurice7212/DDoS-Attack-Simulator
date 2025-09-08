import plotly.graph_objects as go
import random
import time

# Simulated traffic data (replace with log reading in real use)
timestamps = []
requests_per_second = []

for i in range(30):
    timestamps.append(i)
    requests_per_second.append(random.randint(5, 15))
    time.sleep(0.1)

fig = go.Figure()
fig.add_trace(go.Scatter(x=timestamps, y=requests_per_second, mode="lines+markers", name="Requests/sec"))
fig.update_layout(title="Simulated Traffic", xaxis_title="Time (s)", yaxis_title="Requests/sec")
fig.show()
