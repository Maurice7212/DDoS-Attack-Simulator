import psutil
import time
import plotly.graph_objects as go

cpu_usage = []
mem_usage = []
timestamps = []

for i in range(30):
    cpu_usage.append(psutil.cpu_percent())
    mem_usage.append(psutil.virtual_memory().percent)
    timestamps.append(i)
    time.sleep(0.5)

fig = go.Figure()
fig.add_trace(go.Scatter(x=timestamps, y=cpu_usage, mode="lines+markers", name="CPU %"))
fig.add_trace(go.Scatter(x=timestamps, y=mem_usage, mode="lines+markers", name="Memory %"))
fig.update_layout(title="System Resource Usage", xaxis_title="Time (s)", yaxis_title="Usage %")
fig.show()
