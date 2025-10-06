# Group 112 - Phase 1

**Team Members:**  
Elhadji Ndoye  
Sarah Papabathini  
Rosa Sierra Villanueva  
Ryan Blue  



## Overview

- License Metric – Checks if the repository uses a permissive license such as MIT, Apache-2.0, BSD.
- Size Metric – Measures the project size based on the number of files and lines of code.
- Ramp-Up Metric – Estimates how easy it is for a new contributor to get started by analyzing the README and setup instructions.
- Bus Factor Metric – Measures project resilience based on the number of active contributors.

The program outputs one JSON object per line (**NDJSON**) that includes all metrics and a **NetScore**, which is the average of the metric values.


## Installation
To install all dependencies listed in `requirements.txt`, run:

```bash
./run install
```

## Running the Program

Place your URLs into a file (for example, `urls.txt`) — one per line — then run:

```bash
./run urls.txt
```

**An Example Output Would be Something Like the Following:**

```json
{"name":"requests","category":"REPO","license":1.0,"size":0.9,"ramp_up":0.7,"bus_factor":0.8,"net_score":0.85}
```


## Running Tests

To verify functionality and test coverage which should be around 80%, run:

```bash
./run test
```


## NetScore Formula

The NetScore is calculated as the average of all four normalized metric values (each between 0 and 1):

NetScore = (License + Size + Ramp-Up + Bus Factor) / 4


## Known Issues / Future Work

- Ramp-Up metric currently uses simple keyword-based heuristics; can be improved with NLP analysis in the future.
- Bus Factor metric only checks recent contributors, the last 6 months.
- API rate limits may slow responses when testing multiple URLs; timeouts and retries are implemented to reduce this.

