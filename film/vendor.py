"""Copy the exact npm-installed runtime modules and retain their licences."""
from pathlib import Path
import shutil
P=Path(__file__).parent
(P/'vendor/gsap').mkdir(parents=True,exist_ok=True)
shutil.copyfile(P/'node_modules/three/build/three.module.js',P/'vendor/three.module.js')
shutil.copyfile(P/'node_modules/three/LICENSE',P/'vendor/THREE-LICENSE.txt')
for n in ['index.js','gsap-core.js','CSSPlugin.js']:
 shutil.copyfile(P/'node_modules/gsap'/n,P/'vendor/gsap'/n)
shutil.copyfile(P/'node_modules/gsap/README.md',P/'vendor/GSAP-README.md')
shutil.copyfile(P/'node_modules/gsap/package.json',P/'vendor/GSAP-package.json')
(P/'vendor/GSAP-LICENSE-NOTICE.txt').write_text("GSAP 3.12.5. Copyright 2008-2024, GreenSock. All rights reserved.\nSubject to the terms at https://gsap.com/standard-license\nSee the upstream README and package metadata included here.\nOriginal copyright notices are retained in each module.\n")
