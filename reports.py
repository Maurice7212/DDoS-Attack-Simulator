import os
import csv
import datetime
from matplotlib.backends.backend_pdf import PdfPages

class ReportGenerator:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_csv(self, traffic_data, resource_data, config):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"report_{timestamp}.csv")

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Config"])
            for k, v in config.items():
                writer.writerow([k, v])

            writer.writerow([])
            writer.writerow(["Traffic Data (time, rps)"])
            writer.writerows(zip(traffic_data["x"], traffic_data["y"]))

            writer.writerow([])
            writer.writerow(["Resource Data (time, usage%)"])
            writer.writerows(zip(resource_data["x"], resource_data["y"]))

        return filename

    def export_pdf(self, traffic_chart, resource_chart, config):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"report_{timestamp}.pdf")

        with PdfPages(filename) as pdf:
            # Page 1: Config
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 size
            ax.axis("off")
            lines = ["Attack Report", "================="] + [
                f"{k}: {v}" for k, v in config.items()
            ]
            ax.text(0.05, 0.95, "\n".join(lines), va="top", fontsize=12)
            pdf.savefig(fig)
            plt.close(fig)

            # Page 2: Traffic chart
            pdf.savefig(traffic_chart.figure)

            # Page 3: Resource chart
            pdf.savefig(resource_chart.figure)

        return filename
