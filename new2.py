import time

# Higher 64 bits are the difference between Epoch and 1900 in seconds
NTP_OFFSET = (-int(time.mktime ((1900, 1, 1, 0, 0, 0, 0, 0, 0)))) << 32

def posix_to_ntp (timestamp: float):
    """
    Convert a POSIX timestamp (float) to an NTP timestamp (64-bit fixed-point)
    """

    # Convert human-readable time to datetime object
    timestamp_fixed_whole = int (timestamp)
    timestamp_fixed_fract = int (timestamp%1 * (2**32))
    timestamp_fixed = (timestamp_fixed_whole << 32) + timestamp_fixed_fract

    # Calculate the time difference from NTP epoch
    timestamp_fixed_ntp = timestamp_fixed + NTP_OFFSET
    return timestamp_fixed_ntp


def ntp_to_posix (timestamp: int):
    """
    Convert an NTP timestamp (64-bit fixed-point) to a POSIX timestamp (float)
    """

    timestamp_epoch = timestamp - NTP_OFFSET
    timestamp_epoch_whole = timestamp_epoch >> 32
    timestamp_epoch_fract = timestamp_epoch - (timestamp_epoch_whole << 32)

    timestamp_epoch_float = timestamp_epoch_whole + timestamp_epoch_fract / 2**32
    return timestamp_epoch_float

if __name__ == "__main__":
    # The following is just a proof-of-concept procedure to make
    # sure it's working fine. Run this file directly to test it.
    # Takes the current system time (float), converts to NTP timestamp, and
    # back to system time (float).

    t = time.time ()
    nt = epoch_to_ntp (t)
    ut = ntp_to_epoch (nt)

    print ("Original time: ", t)
    print ("Processed time: ", ut)
    print (time.ctime (ut))
