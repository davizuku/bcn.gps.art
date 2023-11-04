#!/usr/bin/env python3

import math
import os
from pathlib import Path
import svgutils

def rotateSvgFile(filename):
    svg = svgutils.transform.fromfile(filename)
    originalSVG = svgutils.compose.SVG(filename)
    originalWidth = float(svg.width.replace('px', ''))
    originalHeight = float(svg.height.replace('px', ''))
    diagonal = math.sqrt(math.pow(originalHeight, 2) + math.pow(originalWidth, 2))
    originalSVG.rotate(45, originalWidth/2, originalHeight/2)
    originalSVG.moveto((diagonal-originalWidth)/2, (diagonal-originalHeight)/2)
    figure = svgutils.compose.Figure(diagonal, diagonal, originalSVG)
    figure.save(filename)

def main():
    os.chdir(os.path.dirname(__file__) + '/..');
    srcDir = 'data/gpx'
    outDir = 'data/svg'
    converterBin = './bin/converter.py'
    styles = {
        'regular': 'fill:none;stroke-width:20;stroke:black',
        'bold': 'fill:none;stroke-width:40;stroke:black',
        'filled': 'fill:black;stroke:none',
    }

    for filename in os.listdir(srcDir):
        if not filename.endswith('.gpx'):
            continue
        gpxFile = Path(filename)
        svgFile = gpxFile.with_suffix('.svg')
        print('Processing {} into {}'.format(gpxFile, svgFile))
        inputFile = srcDir + '/' + str(gpxFile)
        for st in styles:
            outputFolder = outDir + '/' + st
            if not os.path.isdir(outputFolder):
                os.mkdir(outputFolder)
            outputFile = outputFolder + '/' + str(svgFile)
            os.system(
                "{} -i \"{}\" -o \"{}\" -d --style '{}'".format(converterBin, inputFile, outputFile, styles[st]))
            rotateSvgFile(outputFile)

if __name__ == '__main__':
    main()
