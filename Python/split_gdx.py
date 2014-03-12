import sys
import os
import subprocess
import glob

GAMS_Path = '/home/nigel/GAMS/24.0'
WINE = '/usr/bin/wine'
GDX_DUMP = os.path.join(GAMS_Path, 'gdxdump')
GAMS = os.path.join(GAMS_Path, 'gams')

def splitgdx(fName, periods):
    """ Master function, will split a GDX file into a smaller file which
    contains all information required for the trading periods.

    Parameters:
    -----------
    fName: FileName of the GDX file
    periods: List of the trading periods to be split.

    Returns:
    --------
    GDX: A GDX File which is substantially smaller and easier to load/run.
    """

    gms_file = convert_to_gms(fName)
    new_gms_file = scrub_trading_periods(gms_file, periods)
    create_gdx(new_gms_file)


def convert_to_gms(fName):
    """ Take a GDX File and dump it to a GMS file using the installed
    GAMS utility GDXDUMP.

    Parameters:
    -----------
    fName: The GDX File to be dumped:

    Returns:
    --------
    output_name: Name of the dumped GMS File
    """

    output_name = fName.replace('.gdx', '.gms')
    output = "Output=%s" % output_name
    cmd = [WINE, GDX_DUMP, fName, output]
    subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr,
            env={"PATH": "/"})
    return output_name

def scrub_trading_periods(fName, periods):
    """ Remove all information to other non included trading periods.

    Parameters:
    -----------
    fName: The filename of the .GMS file
    periods: What periods to include

    Returns:
    --------
    new_gms_name: filename of the new, reduced GMS file
    """
    tps = ["TP%s" % x for x in periods]
    periods = [str(x) for x in periods]
    new_gms_name = fName.replace('.gms', "".join(periods) +'.gms')
    with open(fName, 'rb') as r:
        with open(new_gms_name, 'wb') as w:
            old_flag = False
            buffer_str = None
            for line in r:
                lupdate, new_flag = check_line(line, tps)
                if lupdate != "Empty":
                    if new_flag == False and old_flag == True:
                        buffer_str = buffer_str.replace(',', r'/;')

                    if buffer_str is not None:
                        w.write(buffer_str)
                    buffer_str = lupdate

                old_flag = new_flag

            w.write(buffer_str)

    return new_gms_name


def check_line(line, tps):
    """ Check a line for inclusion in the new file

    Parameters:
    -----------
    line: The line to be checked
    tps: List of TP Objects to check against

    Returns:
    --------
    line: The line to be added or "Empty"
    new_flag: The flag which is context specific

    """

    if line[:3] ==  "'TP" :
        new_flag = True
        if any([x in line for x in tps]):
            return line, new_flag
        else:
            return "Empty", new_flag
    else:
        new_flag = False
        return line, new_flag

def create_gdx(fName):
    """ Convert a GMS file to a GDX using GAMS"""
    outputname = fName.replace('.gms', '.gdx')
    output="GDX=%s" % outputname
    cmd = [WINE, GAMS, fName, output]
    subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr,
            env={"PATH": "/"})

def cleanup(patterns=('.gms', '.lst')):
    """ Cleans up the temporary files created by the program """
    files = glob.glob('*')
    for f in files:
        if any((x in f for x in patterns)):
            os.remove(f)


if __name__ == '__main__':
    fName = sys.argv[1]
    periods = sys.argv[2:]
    print """I am going to scrub the file %s to ensure that the following
periods %s are the only ones included""" % (fName, periods)
    splitgdx(fName, periods)
    cleanup()

