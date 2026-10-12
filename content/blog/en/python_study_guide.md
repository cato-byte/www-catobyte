## Python Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Downloaded. 10 December 2025 ](../../images/postgres_study_guide_title_img.png)

### Coding problem 1

Parse a log file with a specific format and generate a report. 

Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON

Take into account only the messages ON ERR and OFF

The report shbould look something like this.

Device was on for 7 seconds
Timestamps of error events:
   Jul 11 16:11:54:661
   Jul 11 16:11:56:067

```python

from date import datetime


with open(log_file) as log_f:
    start_time= ""
    end_time = ""
    err_times = []
    for line in f.readline():
        timestamp = line.split()[2]
        if "ON" in line:
            start_time = timestamp
        if "ERR" in line:
            err_times.add(timestamp)
        if "OFF" in line:
            end_time = timestamp
            break
    if start_time and end_time:
        moments_on = datatime.to_timestamp(end_time)-datatime.to_timestamp(start_time)
        moments_on = str(moments_on.to_seconds())
        print(f'Device was on for {momentos_on} seconds')
    print ('Timestamp for error events:')
    for err_timestamp in err_times:
        print(f'     {err_timestamp})

```