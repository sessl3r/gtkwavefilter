# GTKWave Filter's

This repository contains a collection of filter processes coming in handy when
viewing waveforms in GTKWave.

## Usage

To use a translate filter process right click on the signal in GTKWave.
Select Data Format -> Translate Filter Process.
In the dialog add the process and select it.

To use a transaction filter process do the same but select Transaction Filter
Process.

## wrapper.sh

Most of the time it does not work to use a transaction filter with arguments
directly into a python script. Therefore wrapper.sh is a simple wrapper which
just calls a python script with arguments.
