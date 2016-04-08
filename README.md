# netsnmp-galileo
A tar of net-snmp compiled for the Intel Galileo Gen 2

I wanted to use net-snmp on the Galileo Gen 2, unfortunately I could not find the package.

Why SNMP? Because much of the SCADA and IIoT infrastructure is monitored using tools like Nagios and SolarWinds etc.

You can download it here,  to use it run:

    tar -zxvf net-snmp-compiled.tar.gz 
    cd net-snmp-compiled 
    make install

But if you need to compile it on your own, below are the stpes I took.`

This is a quick write up on installing Net-SNMP and creating custom MIB on the Galileo. I am using the eglibc image here: http://downloadmirror.intel.com/25384/eng/iot-devkit-201510010757-mmcblkp0-galileo.direct.xz
 
    wget http://downloads.sourceforge.net/project/net-snmp/net-snmp/5.7.3/net-snmp-5.7.3.tar.gz  

We untar to /tmp to avoid long filename issues  

    tar -xvf net-snmp-5.7.3.tar.gz -C /tmp  
    cd /tmp  
  
    ./configure --disable-ipv6  --disable-embedded-perl --without-perl-modules --disable-snmptrapd-subagent   

Compiling tkaes a very long time, to avoid having to start over use nohup.
  
    nohup make &   
    tail -f nohup.out   
    make install  
  
  
Once done, you need to configure it, the command snmpconf does most of this for you. 

    snmpconf  
    Select snmpd.conf  
    Select Access  

Create readwrite and read only groups (I suggest galileo and galileo-rw)   

    finished  
  
As an example we will create a custom MIB to monitor the temperature using a TMP36.
Create a script called /usr/local/bin/temp.py . (attacheD)

Run snmpconf and add the custom MIB.

    snmpconf
    1:  Extending the Agent  
    1:  run a simple command using exec()  
    ENTER  
    name: temperature  
    The path to the program to be run.: /usr/local/bin/temp.py  
    The arguments to pass to /usr/local/bin/temp.py:   
    finsihed  
    finished  
    quit  
  
  
Move the snmpd.conf in to etc and start snmpd. 
 
    mv snmpd.conf /etc/.  
    snmpd.conf -c /etc/snmpd.conf  

Now we can test. From another machine run snmpwalk.

    #This will not show the custom MIB  
    snmpwalk -c galileo -v2c 192.168.1.100  
  
    #Display the custom MIB  
    snmpwalk -c galileo -v2c 192.168.1.100 nsExtendOutput1  
  
    NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."temperature" = STRING: 82.66  
    NET-SNMP-EXTEND-MIB::nsExtendOutputFull."temperature" = STRING: 82.66  
    NET-SNMP-EXTEND-MIB::nsExtendOutNumLines."temperature" = INTEGER: 1  
    NET-SNMP-EXTEND-MIB::nsExtendResult."temperature" = INTEGER: 0  
  
  
    #Get just the OID  
  
    snmptranslate -On NET-SNMP-EXTEND-MIB::nsExtendOutput1Line.\"temperature\"  
  
  
    #Query by just the OID  
  
    snmpwalk -c galileo -v2c 192.168.1.100 .1.3.6.1.4.1.8072.1.3.2.3.1.1.11.116.101.109.112.101.114.97.116.117.114.101  
    NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."temperature" = STRING: 81.78  

