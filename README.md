# brachy-hdr-tg43-check


Purpose
----------------------
A command line interface to independently calculate doses from Oncentra MasterPlan brachytherapy RTPlan files. For research purposes only.

Install
-------
 ```
 pip install -r requirements.txt
 ``` 
 Open up `hdrpackage\serverconfig.cfg` and edit the following details:
```
Driver={MIMER};
Server=[name/ip address of server];
Database=OTP_DATABASE;
Uid=DBLOOK;
Pwd=[database password]
```

You can test your connection to the database by running:
```
python tests\test_dbconn.py
```
which should pass if successful.

Usage
-------
```
python main.py
``` 
to start the program. You'll be prompted to enter the patient ID, case label, and plan name. You can quit at any time by entering `quit`. The program will return the RTPLAN file from the selected plan for processing.

Parser
-----
The RTPLAN file is parsed by `hdrpackage\parse_omp_rtplan.py`.


TG43
-----
The [TG43](https://www.google.co.uk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0ahUKEwjPvfn54PvRAhUKsBQKHQmZAPQQFggcMAA&url=http%3A%2F%2Fwww.teambest.com%2Fbesttotalsolutions%2FPDFs%2FTG43_update_Iodine_Rivard_Coursey_DeWerd_et_al_March2004.pdf&usg=AFQjCNE9doofriCa-TNFCPn6YEvWB4xBQg&sig2=7Tpv3NUcPVXjMRY1jhXGhw) brachytherapy dose calculation method is included here for use with a MicroSelectron 192Ir source. Raw source data files have been transcribed from the [ESTRO consensus dataset ](http://www.estro.org/about/governance-organisation/committees-activities/tg43-ir-192-hdr) in the `hdrpackage\source_files` directory. Care has been taken to interpret the TG43 reports for recommendations on interpolation/extrapolation routines, but this will not necessarily reflect the operation of Oncentra MasterPlan.


Tests
-----
Run tests with:
```
python tests\tests.py
```
