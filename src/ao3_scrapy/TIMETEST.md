# Testing Results

## AutoThrottle
| # of Pages          | With AutoThrottle   | Without AutoThrottle                                           |
|:--------------------| --------------------| -------------------------------------------------------------- |
| 3                   | 15.6131 seconds     | 5.2771 seconds                                                 |
| 106                 | -                   | 130.9034 seconds (before crashing with TooManyRequests error)  |
| 118                 | 137.4175 seconds (before crashing with TooManyRequests error) |                      |


## Time Delay
| Time Delay | # of Pages  |  Time (seconds) | Crashed? | Person Testing |
| 1          | 117         | 163.5500        | Yes      | Fiza           |
| 1          | 177         | 229.35          | Yes      | Jessica        |
| 1.5        | 118         | 231.3712        | Yes      | Fiza           |
| 1.5        | 118         | 227.19          | Yes      | Jessica        |
| 2          | 120         | 297.8183        | No       | Fiza           |
| 2          | 212         | 528.02          | Yes      | Jessica        |
