# Database Sharding

A Python-based simulation of database sharding strategies using MySQL.

## 🧠 Project Overview

This project lets you explore core database sharding techniques:

- **Hash Sharding**: Distributes data across shards using hash functions (e.g., `user_id % num_shards`).

## ⚙️ Features

- create multiple MySQL-based shards using `docker-compose.yml`.
- Create dynamic id 12 characters or 52 bits unique id.
- Using union-find algorithm to keep join data in same shard.
- Automatically route `INSERT`, `SELECT`, and `UPDATE` queries to the correct shard.
- Support for executing queries involving both sharded tables and broadcast/reference tables.
- Designed for easy extension to additional sharding strategies or database systems.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL (local or Docker)
- Redis
- `fastapi` library

### Installation

```bash
git clone https://github.com/shaakib99/database_sharding.git
cd database_sharding
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
fastapi dev
