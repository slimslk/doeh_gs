# DoEH: Domains of Endless Hunger
## Distributed Game Logic Engine (Python)

A high-performance, asynchronous game server responsible for core mechanics, player state management, and real-time world synchronization.

### Overview
This service acts as the "brain" of the ecosystem. It processes player actions, calculates game-state transitions (ticks), and ensures persistent data storage, all while maintaining high throughput via an event-driven architecture.

### Key Technical Features
*   **Asynchronous Processing**: Built with **Python 3.12** and **Asyncio**, ensuring non-blocking execution of game logic and I/O operations.
*   **State Management & Persistence**: 
    *   Uses **SQLAlchemy 2.0** with **Asyncpg** for high-efficiency, non-blocking interaction with **PostgreSQL**.
    *   Implements sophisticated connection pooling to handle concurrent state updates.
*   **Event-Driven Communication**: 
    *   Deeply integrated with **Apache Kafka** for inter-service synchronization.
    *   Consumes raw player events and produces processed state updates for the WebSocket Gateway.
*   **Data Validation**: Leverages **Pydantic** for strict type safety, data parsing, and robust configuration management.
*   **Tick-Based Engine**: Implements a configurable game loop (`GAME__TICK`) to synchronize logic cycles across the distributed system.

### Tech Stack
*   **Language:** Python 3.12
*   **Libraries:** Pydantic (v2), SQLAlchemy (Async), Asyncpg
*   **Messaging:** Apache Kafka (aiokafka)
*   **Database:** PostgreSQL
*   **Containerization:** Docker

---

### Configuration & Deployment

The engine is highly configurable via environment variables, allowing fine-tuning of both infrastructure (Kafka/DB) and game balance.

#### Core Settings
| Variable | Description |
| :--- | :--- |
| `GAME__TICK` | Logic cycle duration in milliseconds (default: 500ms) |
| `DB__URL` | Asynchronous PostgreSQL connection string |
| `KAFKA__BOOTSTRAP_SERVERS` | List of Kafka brokers |

#### Game Balance Configuration
The service allows real-time adjustment of player attributes without code changes:
* `PLAYER__MAX_HEALTH`, `PLAYER__MAX_ENERGY`
* `PLAYER__DEFAULT_ATTACK_DAMAGE`, `PLAYER__DEFAULT_DEFENCE`

#### Kafka Topics
The engine synchronizes with the ecosystem through these configurable topics:
* **Consumes:** `player-event`
* **Produces:** `location-update`, `player-update`, `game-update`

---

## Getting Started

### Building with Docker
```bash
# Build the game engine image
docker build -t game-engine-python .

# Run the engine
docker run --env-file .env game-engine-python
```
---

## ⚖️ Legal & Licensing

**Copyright © 2025-2026 Dmytro Kuzavkov (slimslk). All rights reserved.**

This software and its associated files are **proprietary** and confidential. 
Unauthorized copying, distribution, or modification of this code, via any medium, is strictly prohibited. 

The source code is provided on GitHub for **portfolio review and educational purposes only**. 
If you wish to use any part of this project for commercial purposes or public distribution, please contact the author at d.kuzavkov@gmail.com.
