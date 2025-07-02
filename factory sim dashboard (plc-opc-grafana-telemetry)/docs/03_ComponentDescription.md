## Component: opc_rest_api.py

- Endpoint: `/motion` (HTTP POST)
- Reads tag: `DB_Tank.MotionDetected` via OPC UA
- Inverts Boolean and writes back to PLC
- Use Case: External web system toggles simulated motion sensor

Example:
```bash
curl -X POST http://localhost:5000/motion
