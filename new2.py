import struct
import datetime

def human_readable_to_ntp_64bit(human_readable_time):
    # NTP epoch starts on January 1, 1900
    ntp_epoch = datetime.datetime(1900, 1, 1, 0, 0, 0)

    
    # Convert human-readable time to datetime object
    dt_object = datetime.datetime.strptime(human_readable_time, '%Y-%m-%d %H:%M:%S')

    
    # Calculate the time difference from NTP epoch
    time_difference = dt_object - ntp_epoch
    
    # Calculate seconds and fractional seconds
    seconds = int(time_difference.total_seconds())
    #fractional_seconds = int((time_difference.microseconds / 1e6) * (2**32))
    
    # Combine seconds and fractional seconds into a 64-bit integer
    return seconds
    ntp_64bit = (seconds << 32) #| fractional_seconds
    
    return ntp_64bit

# Example: Convert human-readable time to NTP 64-bit integer
human_readable_time = "2022-03-05 12:00:00"
ntp_64bit = human_readable_to_ntp_64bit(human_readable_time)

print("Human-Readable Time:", human_readable_time)
print("NTP 64-bit Integer:", ntp_64bit)
