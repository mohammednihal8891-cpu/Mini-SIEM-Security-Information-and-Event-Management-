# 🔐 Mini SIEM — Security Information and Event Management

## 📌 About the Project

Mini SIEM is a beginner-friendly cybersecurity project developed using Python on Kali Linux.

It analyzes SSH authentication logs, detects repeated failed login attempts, generates security alerts, and stores events and alerts in log files.

## 🚀 Features

* 🔍 SSH authentication log analysis
* 🚨 Failed login detection
* 🛡️ Possible brute-force activity detection
* ⚠️ HIGH, MEDIUM, and LOW alert severity summary
* 🧪 Safe demonstration mode
* 📝 Event and alert logging
* 📊 Menu-based terminal interface

## 🛠️ Technologies Used

* Python 3
* Kali Linux
* Linux systemd journal (`journalctl`)
* Git and GitHub

## ⚙️ Installation and Usage

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd mini-siem
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Run the program

```bash
python3 siem.py
```

## 📋 Menu Options

1. Analyze system logs
2. Run safe demo
3. View recent alerts
4. Alert Summary
5. Exit

## 🔎 How It Works

1. The program reads available SSH authentication logs.
2. It searches for failed password events.
3. It counts failed login attempts by source IP address.
4. If five or more matching failed attempts are found for an IP, it generates a HIGH severity alert.
5. Events and alerts are saved in local log files.
6. The Alert Summary displays the number of saved alerts by severity.

## ⚠️ Important Notes

* Log availability depends on the Linux system configuration and user permissions.
* The detection threshold is configurable in the Python source code.
* The demo mode uses simulated data and does not perform real attacks.
* This is an educational project, not a production-grade SIEM.
* Only analyze systems and logs you are authorized to access.

## 👨‍💻 Author

**Mohammed Nihal**

Cybersecurity Student
