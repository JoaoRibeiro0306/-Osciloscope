# uOsciloscope
IoT osciloscope

Program comes with a simulator that can also upload the code to an arduino. All the code besides main.py was developed by Professor Pedro Vitor.
main.py is the file that simulates de osciloscope with the following funcionalities:

Button 1 - Fast Click - Read data from the ADC and display the data.
Button 1 - Slow Click - It has 3 fucntions (It can only be changed by changing the commented code in he loop in main, due to the lack of buttons). This button can work as an auto scale (ajusting the wave to display close to 3 wave lengths and with the minimum vertical scale that still displays the wave), it can also send an email with the values collected by the ADC with indications of Vmax, Vmin, Vmed, Vrms and it can also be used to calibrate de osciloscope (Used to calibrate the ADC from the labs, not pertinent for the simulation).
Button 1 - Double Click - Displays the following values: Vmax, Vmin, Vmed, Vrms
Button 2 - Fast Click - Change the vertical scale incrementing it (From a set of values 1/2/5/10 V/div).
Button 2 - Slow Click - Change the horizontal scale incrementing it (From a set of values 5/10/20/50 ms/div).
Button 2 - Double Click - Calculate and display the Fourier Transform of the input wave. This is done using the DFT algorithm and might take some time to run when used with an arduino.

