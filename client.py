import socket, sntp, time
from _datetime import datetime, timedelta
import win32api
import conversions

if __name__ == "__main__":
    ntp_servers = {
        "time.google.com": ("time.google.com", 123),
        "us.pool.ntp.org": ("us.pool.ntp.org", 123),  # Example NTP server for the US region
        "europe.pool.ntp.org": ("europe.pool.ntp.org", 123),  # Example NTP server for the Europe region
        # Add more NTP servers for different regions/time zones as needed
    }

    # Specify the desired NTP server here
    selected_ntp_server = "time.google.com"
    server_addr = ntp_servers[selected_ntp_server]

# the below function sets the clock of the local system
    def setsystime(time_str):
        '''takes time in string and sets it to the locale system ->use time.ctime()'''
        ntp_dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
        ist_dt = ntp_dt - timedelta(hours=5, minutes=30)
        time_t = (ist_dt.year, ist_dt.month, ist_dt.day,
                  ist_dt.hour, ist_dt.minute, ist_dt.second, 0)
        dayofweek = datetime(*time_t).isocalendar()[2]
        t = time_t[:2] + (dayofweek,) + time_t[2:]
        win32api.SetSystemTime(*t)


    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c_sock:
        hserver_req = sntp.SNTPMsg()
        hserver_req["LI"] = 3  # alarm condition clock not synchronized
        hserver_req["VN"] = 4
        hserver_req["Mode"] = 3  # 3-> client coz its sending request to (hserver)higher server
        hserver_req["Stratum"] = 15  # 2-15 -> secondary reference server
        hserver_req["OriginateTimestamp"] = conversions.posix_to_ntp(time.time()) # time when the message departs
        hserver_req["TransmitTimestamp"] = conversions.posix_to_ntp(time.time()) # time when the message departs

        c_sock.sendto(hserver_req, server_addr)
        hserver_res, addr = c_sock.recvfrom(48)
        hserver_res = sntp.SNTPMsg(hserver_res)
        if hserver_res["OriginateTimestamp"] == hserver_req["TransmitTimestamp"]:
            # the above check is done for reply attacks
            if hserver_res["Stratum"] == 0 or hserver_res["TransmitTimestamp"] == 0 or (
                    hserver_res["Mode"] != 4 and hserver_res["Mode"] != 5):
                print("Server reply is discarded\nDoes not comply with message standard specified by rfc")
            else:
                print("Processing server reply")
                print(f"The current primary server:{server_addr[0]}\nThe server response message :\n{hserver_res}")
                # calculating round trip delay
                t1 = hserver_req["OriginateTimestamp"]
                t2 = hserver_res["RecieveTimestamp"]
                t3 = hserver_res["TransmitTimestamp"]
                t4 = conversions.posix_to_ntp(time.time())
                # print(time.ctime(conversions.ntp_to_posix(t1)))
                # print(time.ctime(conversions.ntp_to_posix(t2)))
                # print(time.ctime(conversions.ntp_to_posix(t3)))
                # print(time.ctime(conversions.ntp_to_posix(t4)))

                # print(f"t4:{t4},{time.ctime(conversions.ntp_to_posix(t4))}")
                # d is the rtd 
                d = (t4 - t1) - (t3 - t2)
                # t is the clock offset
                t = ((t2 - t1) + (t3 - t4)) / 2

                # the below transmit time is the request one same as local time
                accurate_time = hserver_req["TransmitTimestamp"] + int(t) -int((d / 2))
                ist_accurate_time = conversions.ntp_to_posix(accurate_time) + (5 * 3600) + (30 * 60)
                print(ist_accurate_time,accurate_time)

                print(f"accurate time : {time.ctime(conversions.ntp_to_posix(accurate_time))},current time {time.ctime()}")
                print(f"the supposed ist time {time.ctime(ist_accurate_time)}")
                print(f"Transmit time ins response {time.ctime(conversions.ntp_to_posix(t3))}")

                # setsystime(time.ctime(conversions.ntp_to_posix(accurate_time)))

