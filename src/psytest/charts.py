
from math import pi
from pathlib import Path
import matplotlib.pyplot as plt

def make_radar(labels, values, out_path: Path):
    # Single-plot radar without explicit colors/styles
    N = len(labels)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    vals = list(values) + values[:1]

    fig = plt.figure()  # single plot, default style/colors
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.plot(angles, vals)
    ax.fill(angles, vals, alpha=0.1)

    fig.savefig(out_path)
    plt.close(fig)
    return out_path
