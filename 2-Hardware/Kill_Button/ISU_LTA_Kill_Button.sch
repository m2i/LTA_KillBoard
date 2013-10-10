EESchema Schematic File Version 2  date 12/5/2012 12:39:28 PM
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:ISU_Parts
LIBS:ISU_LTA_Kill_Switch-cache
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title "ISU LTA Kill Button"
Date "5 dec 2012"
Rev "A"
Comp "Iowa State University"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Connection ~ 3900 3800
Wire Wire Line
	3900 3300 3900 3800
Wire Wire Line
	7350 3800 9150 3800
Wire Wire Line
	5800 3600 4300 3600
Wire Wire Line
	4300 3600 4300 3800
Wire Wire Line
	4300 3800 3400 3800
Connection ~ 8050 3800
Wire Wire Line
	8050 3850 8050 3800
Wire Wire Line
	9150 4400 9150 4500
Wire Wire Line
	7600 3550 7600 3500
Wire Wire Line
	7600 3500 7350 3500
Wire Wire Line
	5800 3500 5600 3500
Wire Wire Line
	5600 3500 5600 3550
Wire Wire Line
	8050 4250 8050 4300
Wire Wire Line
	3400 4000 3800 4000
Text Label 3800 4000 0    60   ~ 0
Easy_Button_Sp-
Text Label 3900 3300 0    60   ~ 0
Easy_Button_SP+
$Comp
L SPEAKER SP?
U 1 1 50BF945A
P 3100 3900
F 0 "SP?" H 3000 4150 70  0000 C CNN
F 1 "SPEAKER" H 3000 3650 70  0000 C CNN
	1    3100 3900
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR3
U 1 1 50836A05
P 8050 4300
F 0 "#PWR3" H 8050 4300 30  0001 C CNN
F 1 "GND" H 8050 4230 30  0001 C CNN
	1    8050 4300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR1
U 1 1 50836A01
P 5600 3550
F 0 "#PWR1" H 5600 3550 30  0001 C CNN
F 1 "GND" H 5600 3480 30  0001 C CNN
	1    5600 3550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR2
U 1 1 508369FD
P 7600 3550
F 0 "#PWR2" H 7600 3550 30  0001 C CNN
F 1 "GND" H 7600 3480 30  0001 C CNN
	1    7600 3550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR5
U 1 1 508369F6
P 9150 4500
F 0 "#PWR5" H 9150 4500 30  0001 C CNN
F 1 "GND" H 9150 4430 30  0001 C CNN
	1    9150 4500
	1    0    0    -1  
$EndComp
$Comp
L SYNAPSE_S200 RF1
U 1 1 5083698A
P 6550 4050
F 0 "RF1" H 6550 4750 60  0000 C CNN
F 1 "SYNAPSE_S200" H 6600 4850 60  0000 C CNN
	1    6550 4050
	1    0    0    -1  
$EndComp
$Comp
L C C1
U 1 1 50836582
P 8050 4050
F 0 "C1" H 8100 4150 50  0000 L CNN
F 1 "10u" H 8100 3950 50  0000 L CNN
	1    8050 4050
	1    0    0    -1  
$EndComp
$Comp
L BATTERY BT1
U 1 1 50836572
P 9150 4100
F 0 "BT1" H 9150 4300 50  0000 C CNN
F 1 "BATTERY" H 9150 3910 50  0000 C CNN
	1    9150 4100
	0    1    1    0   
$EndComp
$EndSCHEMATC
