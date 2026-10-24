"""Rebuild the font-derived SVG used by the extruded chrome wordmark."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
P=Path(__file__).parent;f=TTFont(P/'assets/Display.ttf');gs=f.getGlyphSet();cm=f.getBestCmap();x=0;paths=[]
for c in 'SKIM':
 name=cm[ord(c)];pen=SVGPathPen(gs);gs[name].draw(pen);paths.append(f'<path transform="translate({x} 0)" d="{pen.getCommands()}"/>');x+=gs[name].width-70
(P/'assets/wordmark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1550 '+str(x)+' 1650"><g transform="scale(1 -1)">'+''.join(paths)+'</g></svg>')
