# Les montants s'écrivent « 3 837,50 $ » avec une espace INSÉCABLE avant le $ (30 sept. 2026),
# pour que le $ ne parte jamais seul à la ligne. Pour les tests qui lisent le texte de la page,
# c'est une espace comme une autre : on la ramène à une espace simple à la lecture.
from playwright.sync_api import Locator, Page, ElementHandle
def _nb(v):
    if isinstance(v, str): return v.replace('\xa0', ' ')
    if isinstance(v, list): return [_nb(x) for x in v]
    if isinstance(v, dict): return {k: _nb(x) for k, x in v.items()}
    return v
for C, noms in ((Locator, ('inner_text', 'text_content', 'all_inner_texts', 'evaluate', 'input_value')), (Page, ('inner_text', 'text_content', 'evaluate', 'input_value')), (ElementHandle, ('inner_text', 'text_content', 'evaluate'))):
    for n in noms:
        f = getattr(C, n, None)
        if f is None: continue
        def w(self, *a, _f=f, **k): return _nb(_f(self, *a, **k))
        setattr(C, n, w)
