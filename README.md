# Inventory_Management_System
A modern and feature-rich **Inventory Management System (IMS)** built using **Flask**, **SQLAlchemy**, and **Bootstrap 5**.  
It provides an intuitive web interface to handle **product stock**, **warehouse locations**, **item movements**, and **inventory reports** in real time.

---

## 🧭 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Requirements](#-system-requirements)
- [Installation Guide](#-installation-guide)
- [Database Setup](#-database-setup)
- [How to Run the Project](#-how-to-run-the-project)
- [Folder Structure](#-folder-structure)
- [Usage Instructions](#-usage-instructions)
- [Application Flow](#-application-flow)
- [Sample Credentials](#-sample-credentials)
- [Screenshots / Output](#-screenshots--output)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)
- [License](#-license)

---

## 💡 Overview

This project aims to simplify and automate inventory tracking for small to medium-sized setups.  
With this system, you can:
- Manage all **products**, **locations**, and **movements** in one place
- Generate **real-time balance reports**
- Prevent **negative stock errors**
- Enjoy a clean, responsive UI made with Bootstrap and pastel gradients

It’s lightweight, database-driven, and can easily scale from a local setup to a cloud-hosted environment.

---

## 🌟 Features

### 🔐 Authentication
- Secure login, registration, and logout system
- Passwords hashed using Werkzeug security

### 📦 Product Management
- Add, edit, and delete products
- Assign unique product IDs and categories
- Initialize starting stock with quantity and location

### 📍 Location Management
- Create and manage storage points (warehouses, stores)
- Edit or delete locations anytime

### 🔁 Product Movement
- Record stock transfers between locations
- Validate stock levels before transfer
- Track every transaction chronologically

### 📈 Reporting & Dashboard
- Dashboard showing product, location, and movement stats
- Balance report for stock count across all locations
- Printable report format

### 💅 UI/UX
- Built with Bootstrap 5 and custom styling
- Responsive, gradient-themed dashboard
- Smooth navigation with consistent layout (`base.html`)

---

## 🧰 Tech Stack

| Layer | Technology Used |
|-------|------------------|
| **Backend** | Flask 3.0 |
| **Database ORM** | SQLAlchemy 2.0 |
| **Frontend** | HTML5, CSS3, Jinja2, Bootstrap 5, Bootstrap Icons |
| **Database** | SQLite |
| **Language** | Python 3.x |
| **Server** | Flask Development Server / WSGI |

---

## ⚙️ System Requirements

Make sure you have:
- 🐍 **Python 3.9+**
- 📦 **pip** package manager
- 💻 A code editor like VS Code or PyCharm
- 🗄️ Optional: Git (to clone the repository)

---

## 🪜 Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/inventory-management.git
cd inventory-management
