"""Simulacion pura de la migracion tecnologica de Auditoria 21."""

from pathlib import Path


def test_target_versions():
    req = Path('requeriments').read_text()
    assert 'django==5.2.17' in req
    assert 'channels==4.3.2' in req
    assert 'channels-redis==4.3.0' in req
    assert 'daphne==4.2.3' in req
    assert 'pillow==12.3.0' in req
    assert Path('.python-version').read_text().strip() == '3.13'


def test_no_legacy_imports():
    forbidden = ('from django.conf.urls', 'from django.core.urlresolvers', 'ugettext', 'force_text', 'smart_text', 'request.is_ajax')
    for p in Path('.').rglob('*.py'):
        if 'migrations' in p.parts or p.name.startswith('auditoria') or p.name.startswith('audit'):
            continue
        text = p.read_text(errors='ignore')
        assert not any(x in text for x in forbidden), p


def test_asgi_shape():
    asgi = Path('app/asgi.py').read_text()
    routing = Path('app/routing.py').read_text()
    settings = Path('app/settings.py').read_text()
    assert 'get_asgi_application' in asgi
    assert '"http"' in asgi
    assert '.as_asgi()' in routing
    assert "ASGI_APPLICATION = 'app.asgi.application'" in settings


def test_xlsx_importer():
    text = Path('cards/views.py').read_text()
    assert 'load_workbook' in text
    assert 'xlrd.open_workbook' not in text


def main():
    test_target_versions()
    test_no_legacy_imports()
    test_asgi_shape()
    test_xlsx_importer()
    print('AUDITORIA 21 SIMULACION: OK')


if __name__ == '__main__':
    main()
