# _A python program for comparing monthly energy usage with the dutch 'Prijsplafond'._

The program uses python 3.7 with
* datetime
* colored 1.4.2

Input for the calculations is a list with energy meter values.
The list can be adjusted manually. 
If you have a smartmeter you should be able to create the list automatically.

![prijsplafond_meterstanden](https://user-images.githubusercontent.com/15167631/212654997-6bcacc93-7de2-4067-8431-ee433b36d808.PNG)

Output of program contains results of all meter values compared to the previous meter value.
A summary is calculated for each period.

![prijsplafond](https://user-images.githubusercontent.com/15167631/212651589-cd4d4a22-4035-4c82-8989-0a3b5c9fd468.PNG)

The summary adjusts each period to the period's number of days. 
For the last not completed period an estimation is calculated for the whole period.

![prijsplafond_periodes](https://user-images.githubusercontent.com/15167631/212652900-1a4487b5-82c6-4955-b5c9-934f57949743.PNG)

For each period the difference between energy usage and 'prijsplafond' is calculated (VERSCHIL).
If the energy usage is within the 'prijsplafond' then the difference is displayed in **green**.
If using more energy than the 'prijsplafond' the difference is displayed in **red**.




