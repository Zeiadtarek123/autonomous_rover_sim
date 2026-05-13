#!/usr/bin/env python3
"""
IMU Data Analyzer — collects 500 samples then plots and prints statistics.
Run while the simulation is active.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import numpy as np
import matplotlib
matplotlib.use('Agg')          # headless-safe backend
import matplotlib.pyplot as plt
import time, os

SAMPLES_TARGET = 500

class IMUAnalyzer(Node):
    def __init__(self):
        super().__init__('imu_analyzer')
        self.sub = self.create_subscription(Imu, '/imu/data', self.cb, 10)
        self.data = {k: [] for k in
                     ['ax','ay','az','gx','gy','gz','t']}
        self.t0 = None
        self.get_logger().info(f'Collecting {SAMPLES_TARGET} IMU samples …')

    def cb(self, msg):
        now = time.time()
        if self.t0 is None:
            self.t0 = now
        self.data['t'].append(now - self.t0)
        self.data['ax'].append(msg.linear_acceleration.x)
        self.data['ay'].append(msg.linear_acceleration.y)
        self.data['az'].append(msg.linear_acceleration.z)
        self.data['gx'].append(msg.angular_velocity.x)
        self.data['gy'].append(msg.angular_velocity.y)
        self.data['gz'].append(msg.angular_velocity.z)

        n = len(self.data['t'])
        if n % 100 == 0:
            self.get_logger().info(f'  {n}/{SAMPLES_TARGET} samples collected')
        if n >= SAMPLES_TARGET:
            self.report()
            rclpy.shutdown()

    def report(self):
        d = {k: np.array(v) for k, v in self.data.items()}
        print("\n╔══════════════════════════════════════╗")
        print("║           IMU ANALYSIS REPORT        ║")
        print("╠══════════════════════════════════════╣")
        for label, key in [('Accel X (m/s²)','ax'),('Accel Y (m/s²)','ay'),
                            ('Accel Z (m/s²)','az'),('Gyro  X (rad/s)','gx'),
                            ('Gyro  Y (rad/s)','gy'),('Gyro  Z (rad/s)','gz')]:
            arr = d[key]
            print(f"║ {label:<18} mean={np.mean(arr):+.5f}  std={np.std(arr):.5f}")
        print("╚══════════════════════════════════════╝\n")

        # ── Drift detection on gyro Z (cumulative integral) ──
        dt = np.diff(d['t'], prepend=0)
        gz_drift = np.cumsum(d['gz'] * dt)

        fig, axes = plt.subplots(3, 2, figsize=(14, 10))
        fig.suptitle('IMU Sensor Validation — Gazebo Simulation', fontsize=14)

        pairs = [
            (axes[0,0], d['t'], d['ax'], 'Accel X', 'm/s²', 'tab:red'),
            (axes[0,1], d['t'], d['az'], 'Accel Z (gravity ~9.81)', 'm/s²', 'tab:blue'),
            (axes[1,0], d['t'], d['gx'], 'Gyro X',  'rad/s', 'tab:orange'),
            (axes[1,1], d['t'], d['gz'], 'Gyro Z',  'rad/s', 'tab:green'),
            (axes[2,0], d['t'], gz_drift,'Gyro Z Cumulative Drift','rad','tab:purple'),
            (axes[2,1], d['t'], d['ay'], 'Accel Y', 'm/s²', 'tab:brown'),
        ]
        for ax, x, y, title, ylabel, color in pairs:
            ax.plot(x, y, color=color, alpha=0.8, linewidth=0.8)
            ax.axhline(np.mean(y), color='black', linestyle='--',
                       linewidth=1.2, label=f'mean={np.mean(y):.4f}')
            ax.set_title(title); ax.set_xlabel('Time (s)')
            ax.set_ylabel(ylabel); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

        plt.tight_layout()
        out = os.path.expanduser('~/imu_analysis.png')
        plt.savefig(out, dpi=150)
        self.get_logger().info(f'Plot saved → {out}')

def main():
    rclpy.init()
    rclpy.spin(IMUAnalyzer())

if __name__ == '__main__':
    main()