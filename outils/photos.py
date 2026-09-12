#!/usr/bin/env python3
"""
Telecharge les photos du catalogue, rogne les marges et les normalise
au meme format carre. Relancable : les images deja traitees sont ignorees.
"""
import csv, os, sys, io, time
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    from PIL import Image, ImageChops
except ImportError:
    sys.exit("Il manque une bibliotheque. Relance via telecharger_photos.command")

ICI      = os.path.dirname(os.path.abspath(__file__))
SOURCE   = os.path.join(ICI, "photos.csv")
DOSSIER  = os.path.join(ICI, "photos")
RAPPORT  = os.path.join(ICI, "photos_manquantes.csv")
TAILLE   = 800      # pixels du carre final
MARGE    = 0.05     # 5 % de marge autour du flacon
FILS     = 8        # telechargements simultanes
UA       = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def rogner(im):
    """Retire la marge uniforme autour du produit, quelle que soit sa couleur."""
    if im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 255:
        bbox = im.getchannel("A").getbbox()          # fond transparent
    else:
        rgb = im.convert("RGB")
        fond = Image.new("RGB", rgb.size, rgb.getpixel((0, 0)))
        diff = ImageChops.difference(rgb, fond)
        bbox = ImageChops.add(diff, diff, 2.0, -12).getbbox()
    return im.crop(bbox) if bbox else im


def carrer(im):
    """Centre l'image sur un carre, avec une marge constante."""
    cote = int(max(im.size) * (1 + 2 * MARGE))
    fond = (255, 255, 255, 0) if im.mode == "RGBA" else (255, 255, 255)
    canevas = Image.new(im.mode, (cote, cote), fond)
    canevas.paste(im, ((cote - im.width) // 2, (cote - im.height) // 2))
    return canevas.resize((TAILLE, TAILLE), Image.LANCZOS)


def traiter(barcode, url):
    sortie = os.path.join(DOSSIER, f"{barcode}.webp")
    if os.path.exists(sortie) and os.path.getsize(sortie) > 500:
        return barcode, "deja"
    derniere = ""
    for essai in range(3):
        try:
            r = requests.get(url, headers=UA, timeout=25)
            if r.status_code != 200:
                derniere = f"HTTP {r.status_code}"
                time.sleep(1 + essai)
                continue
            im = Image.open(io.BytesIO(r.content))
            im.load()
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
            carrer(rogner(im)).save(sortie, "WEBP", quality=88, method=4)
            return barcode, "ok"
        except Exception as e:
            derniere = type(e).__name__
            time.sleep(1 + essai)
    return barcode, f"echec: {derniere}"


def main():
    if not os.path.exists(SOURCE):
        sys.exit(f"Fichier introuvable : {SOURCE}")
    os.makedirs(DOSSIER, exist_ok=True)
    with open(SOURCE, encoding="utf-8") as f:
        taches = [(l["barcode"], l["url"]) for l in csv.DictReader(f) if l.get("url")]

    total = len(taches)
    print(f"\n  {total} photos a traiter\n  Dossier : {DOSSIER}\n")
    ok = deja = 0
    rates = []

    with ThreadPoolExecutor(max_workers=FILS) as ex:
        futurs = {ex.submit(traiter, b, u): (b, u) for b, u in taches}
        for i, fut in enumerate(as_completed(futurs), 1):
            bc, res = fut.result()
            if res == "ok":
                ok += 1
            elif res == "deja":
                deja += 1
            else:
                rates.append((bc, futurs[fut][1], res))
            if i % 25 == 0 or i == total:
                pct = 100 * i / total
                print(f"\r  [{i:>5}/{total}] {pct:5.1f} %   "
                      f"telechargees {ok}   deja la {deja}   echecs {len(rates)}",
                      end="", flush=True)

    print("\n")
    if rates:
        with open(RAPPORT, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["barcode", "url", "raison"])
            w.writerows(rates)
        print(f"  {len(rates)} echecs listes dans photos_manquantes.csv")
        print("  Relance le script : il ne reprendra que celles-la.\n")
    else:
        print("  Toutes les photos sont passees.\n")
    print(f"  Termine : {ok + deja} images pretes dans le dossier photos/\n")


if __name__ == "__main__":
    main()
