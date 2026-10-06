## MongoDB Collections

**Database:** `f1db`

| Collection | Fields |
|---|---|
| `driver_stats` | `driver`, `laps`, `avg_lap`, `best_lap`, `worst_lap`, `std` |
| `lap_trend` | `track`, `lap`, `laps`, `avg_lap`, `fastest`, `slowest` |
| `lap_fastest` | `track`, `driver`, `laps`, `avg_lap`, `fastest`, `slowest` |
| `circuit_laptime` | `track`, `laps`, `avg_lap`, `fastest`, `slowest` |
| `circuit_speed` | `track`, `samples`, `avg_speed`, `min_speed`, `max_speed` |
| `speed_driver` | `track`, `driver`, `samples`, `avg_speed`, `min_speed`, `max_speed` |
| `speed_band` | `track`, `band`, `samples` |
| `tyre_speed` | `tyre`, `samples`, `avg_speed`, `min_speed`, `max_speed` |
| `pit_laps` | `track`, `driver`, `session`, `lap`, `frames`, `tyres` |
| `pit_stops` | `track`, `driver`, `stops`, `avg_frames`, `min_frames`, `max_frames` |