TssWrapper around tsschecker binary  

# Threading branch
Need to implement sshd_config modification to allow simultaneous connections for the proper number of threads.  
Currently 36 versions for iPhone6,1 (MaxSessions 36 in /etc/ssh/sshd_config) may require reboot or pkill of all processes using/service restart  