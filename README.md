# Offline Voice Assistant (IoT Edge)

An offline, privacy-preserving voice assistant that runs entirely on local hardware and exposes **IoT observability** and **runtime control** via MQTT + Node-RED. Operational events are stored in **SQLite** and telemetry can be sent to **InfluxDB**.

## Prerequisites (tested)

- **OS**: Windows 11
- **Python**: 3.11
- **Node-RED**: installed locally (see official docs)
- **MQTT broker**: local broker recommended (e.g., Mosquitto on `localhost:1883`)
- **InfluxDB**: local NoSQL database on port `8086`
- **Build tools (Windows, install-time only)**:
  - Visual C++ Build Tools and **CMake**
  - Use **x64 Native Tools Command Prompt for VS 2022** when installing

> Build tools are needed only to compile dependencies (e.g., `llama-cpp-python`). After a successful install, they can be uninstalled; the project folder can be moved to another device.

## Running with Node-RED

After verifying the installation of the prerequisites, start Node-RED locally and access the Flows Dashboard. In the repository there a file `nore-red.json`, which contains three flows. Once imported, run the first flow to install the requirements. Then, go to `localhost:8088/dashboard` to access the assistant dashboard and use the controls to start/stop the assistant.
