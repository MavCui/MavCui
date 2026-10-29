from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / 'assets' / 'profile'
ROOT.mkdir(parents=True, exist_ok=True)
nodes = [(85,48),(210,27),(210,69),(345,48),(480,24),(480,72),(615,48),(750,27),(750,69),(875,48)]
edges = [(0,1),(0,2),(1,3),(2,3),(3,4),(3,5),(4,6),(5,6),(6,7),(6,8),(7,9),(8,9)]
for theme, bg, line, node in [('dark','#0d1117','#33465e','#60a5fa'),('light','#ffffff','#cbd5e1','#2563eb')]:
    frames = []
    for frame in range(160):
        im = Image.new('RGB', (960,96), bg)
        d = ImageDraw.Draw(im)
        for a,b in edges:
            d.line([nodes[a],nodes[b]], fill=line, width=2)
        for x,y in nodes:
            d.ellipse((x-3,y-3,x+3,y+3),fill=node)
        for offset in (0, 40, 80, 120):
            phase = ((frame + offset) % 160) / 160
            edge_index = min(int(phase * len(edges)), len(edges)-1)
            t = (phase * len(edges)) % 1
            a,b = edges[edge_index]
            x = nodes[a][0]*(1-t)+nodes[b][0]*t
            y = nodes[a][1]*(1-t)+nodes[b][1]*t
            d.ellipse((x-4,y-4,x+4,y+4),fill='#22d3ee' if theme=='dark' else '#0284c7')
        if frame == 0:
            im.save(ROOT / f'hero-{theme}-static.png', optimize=True)
        frames.append(im.quantize(colors=32))
    frames[0].save(ROOT / f'hero-{theme}.gif', save_all=True, append_images=frames[1:], duration=50, loop=0, optimize=True)
