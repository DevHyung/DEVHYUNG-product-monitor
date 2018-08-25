# -*- mode: python -*-

block_cipher = None


a = Analysis(['mrporter-site.py'],
             pathex=['D:\\ProjPy3\\Å©¸ù¿ÜÁÖ\\DEVHYUNG-product-monitor'],
             binaries=[],
             datas=[],
             hiddenimports=['requests','bs4','time','random','log','discord_hooks','lxml','json','datetime','collections'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mrporter-site',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='favicon.ico')
