# Blind Hunter Prompt - Story 1.1 Rerun

Use the `bmad-review-adversarial-general` stance. You receive only this unified diff. Do not use project context. Review for bugs, regressions, maintainability hazards, bad assumptions, dependency/tooling issues, and anything that could break users or later developers.

Output findings as a Markdown list. Each finding must include severity, affected file/line if inferable, issue, and concrete fix. If no findings, say so and list residual risks.

```diff
--- a/.gitignore
+++ b/.gitignore
@@ -0,0 +1,13 @@
+.venv/

+.ruff_cache/

+.pytest_cache/

+__pycache__/

+*.py[cod]

+build/

+dist/

+*.egg-info/

+.mypy_cache/

+.pyright/

+workspace-output/

+exports/

+*.log



--- a/.python-version
+++ b/.python-version
@@ -0,0 +1 @@
+3.11



--- a/README.md
+++ b/README.md
@@ -0,0 +1,37 @@
+# 3.ThucTheNgay

+

+Python desktop application scaffold for preparing satellite imagery report outputs.

+

+## Development

+

+This project uses Python 3.11 and `uv` project management.

+

+```bash

+uv sync --dev

+uv run pytest

+uv run ruff check .

+uv run python -m thucthengay

+```

+

+The current scaffold keeps tests independent from project data, network access, GeoTIFF files,

+PowerPoint templates, and a Qt event loop.

+

+## GDAL-compatible install path

+

+`rasterio` is the configured raster/GDAL access layer for the MVP package. On most supported

+platforms its wheels provide the compatible GDAL runtime needed by the application. If a platform

+cannot use those wheels, create the environment from `environment.yml` so GDAL, rasterio, pyproj,

+and shapely are resolved together by conda-forge:

+

+```bash

+conda env create -f environment.yml

+conda activate ttn-env

+python -m pip install uv

+UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv sync --dev

+UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run pytest

+UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run ruff check .

+UV_PROJECT_ENVIRONMENT="$CONDA_PREFIX" uv run python -m thucthengay

+```

+

+`UV_PROJECT_ENVIRONMENT` is required for this fallback path so `uv` installs into and runs from

+the active conda environment instead of creating a separate project `.venv`.



--- a/pyproject.toml
+++ b/pyproject.toml
@@ -0,0 +1,57 @@
+[project]

+name = "thucthengay"

+version = "0.1.0"

+description = "Desktop workflow for preparing satellite imagery reports."

+readme = "README.md"

+requires-python = ">=3.11,<3.12"

+dependencies = [

+    "PySide6>=6.7",

+    "pydantic>=2.7",

+    "rasterio>=1.3",

+    "shapely>=2.0",

+    "pyproj>=3.6",

+    "numpy>=1.26",

+    "Pillow>=10.0",

+    "python-pptx>=1.0",

+]

+

+[project.scripts]

+thucthengay = "thucthengay.app:main"

+

+[dependency-groups]

+dev = [

+    "pytest>=8.0",

+    "ruff>=0.4",

+]

+

+[build-system]

+requires = ["hatchling"]

+build-backend = "hatchling.build"

+

+[tool.hatch.build.targets.wheel]

+packages = ["src/thucthengay"]

+

+[tool.pytest.ini_options]

+testpaths = ["tests"]

+pythonpath = ["src"]

+

+[tool.ruff]

+target-version = "py311"

+line-length = 100

+exclude = [

+    ".venv",

+    ".ruff_cache",

+    ".pytest_cache",

+    "__pycache__",

+    "build",

+    "dist",

+    ".agents",

+    ".claude",

+    "_bmad",

+    "_bmad-output",

+    "scripts",

+    "webapp_geojson",

+]

+

+[tool.ruff.lint]

+select = ["E", "F", "I", "UP", "B"]



--- a/uv.lock
+++ b/uv.lock
@@ -0,0 +1,512 @@
+version = 1

+revision = 3

+requires-python = "==3.11.*"

+

+[[package]]

+name = "affine"

+version = "2.4.0"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/69/98/d2f0bb06385069e799fc7d2870d9e078cfa0fa396dc8a2b81227d0da08b9/affine-2.4.0.tar.gz", hash = "sha256:a24d818d6a836c131976d22f8c27b8d3ca32d0af64c1d8d29deb7bafa4da1eea", size = 17132, upload-time = "2023-01-19T23:44:30.696Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/0b/f7/85273299ab57117850cc0a936c64151171fac4da49bc6fba0dad984a7c5f/affine-2.4.0-py3-none-any.whl", hash = "sha256:8a3df80e2b2378aef598a83c1392efd47967afec4242021a0b06b4c7cbc61a92", size = 15662, upload-time = "2023-01-19T23:44:28.833Z" },

+]

+

+[[package]]

+name = "annotated-types"

+version = "0.7.0"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/ee/67/531ea369ba64dcff5ec9c3402f9f51bf748cec26dde048a2f973a4eea7f5/annotated_types-0.7.0.tar.gz", hash = "sha256:aff07c09a53a08bc8cfccb9c85b05f1aa9a2a6f23728d790723543408344ce89", size = 16081, upload-time = "2024-05-20T21:33:25.928Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/78/b6/6307fbef88d9b5ee7421e68d78a9f162e0da4900bc5f5793f6d3d0e34fb8/annotated_types-0.7.0-py3-none-any.whl", hash = "sha256:1f02e8b43a8fbbc3f3e0d4f0f4bfc8131bcb4eebe8849b8e5c773f3a1c582a53", size = 13643, upload-time = "2024-05-20T21:33:24.1Z" },

+]

+

+[[package]]

+name = "attrs"

+version = "26.1.0"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/9a/8e/82a0fe20a541c03148528be8cac2408564a6c9a0cc7e9171802bc1d26985/attrs-26.1.0.tar.gz", hash = "sha256:d03ceb89cb322a8fd706d4fb91940737b6642aa36998fe130a9bc96c985eff32", size = 952055, upload-time = "2026-03-19T14:22:25.026Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl", hash = "sha256:c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309", size = 67548, upload-time = "2026-03-19T14:22:23.645Z" },

+]

+

+[[package]]

+name = "certifi"

+version = "2026.5.20"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/f3/ce/ee2ecad540810a79593028e88299baeae54d346cc7a0d94b6199988b89b1/certifi-2026.5.20.tar.gz", hash = "sha256:69dea482ab64caa7b9f6aba1c6bf48bb6a5448d1c0f1b17ab42ad8c763a5344d", size = 135422, upload-time = "2026-05-20T11:46:50.073Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/59/8c/57e832b7af6d7c5abe66eb3fbe3a3a32f4d11ea23a1aa7131371035be991/certifi-2026.5.20-py3-none-any.whl", hash = "sha256:3c52e209ba0a4ad7aebe60436a4ab349c39e1e602e8c134221e546902ad25897", size = 134134, upload-time = "2026-05-20T11:46:48.578Z" },

+]

+

+[[package]]

+name = "click"

+version = "8.4.1"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "colorama", marker = "sys_platform == 'win32'" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/9b/98/518d8e5081007684232226f475082b30087d0f585e8457db087298259f49/click-8.4.1.tar.gz", hash = "sha256:918b5633eddf6b41c32d4f454bf0de810065c74e3f7dbf8ee5452f8be88d3e96", size = 353007, upload-time = "2026-05-22T04:08:37.769Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/c7/0d/67e5b4109ea4a837e80daa87c2c696711955e40449a97e8926672534def2/click-8.4.1-py3-none-any.whl", hash = "sha256:482be17c6991b8c19c5429a1e995d9b0efdbb63172824c41f99965dc0ade8ec2", size = 116639, upload-time = "2026-05-22T04:08:35.26Z" },

+]

+

+[[package]]

+name = "click-plugins"

+version = "1.1.1.2"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "click" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/c3/a4/34847b59150da33690a36da3681d6bbc2ec14ee9a846bc30a6746e5984e4/click_plugins-1.1.1.2.tar.gz", hash = "sha256:d7af3984a99d243c131aa1a828331e7630f4a88a9741fd05c927b204bcf92261", size = 8343, upload-time = "2025-06-25T00:47:37.555Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/3d/9a/2abecb28ae875e39c8cad711eb1186d8d14eab564705325e77e4e6ab9ae5/click_plugins-1.1.1.2-py2.py3-none-any.whl", hash = "sha256:008d65743833ffc1f5417bf0e78e8d2c23aab04d9745ba817bd3e71b0feb6aa6", size = 11051, upload-time = "2025-06-25T00:47:36.731Z" },

+]

+

+[[package]]

+name = "cligj"

+version = "0.7.2"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "click" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/ea/0d/837dbd5d8430fd0f01ed72c4cfb2f548180f4c68c635df84ce87956cff32/cligj-0.7.2.tar.gz", hash = "sha256:a4bc13d623356b373c2c27c53dbd9c68cae5d526270bfa71f6c6fa69669c6b27", size = 9803, upload-time = "2021-05-28T21:23:27.935Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/73/86/43fa9f15c5b9fb6e82620428827cd3c284aa933431405d1bcf5231ae3d3e/cligj-0.7.2-py3-none-any.whl", hash = "sha256:c1ca117dbce1fe20a5809dc96f01e1c2840f6dcc939b3ddbb1111bf330ba82df", size = 7069, upload-time = "2021-05-28T21:23:26.877Z" },

+]

+

+[[package]]

+name = "colorama"

+version = "0.4.6"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz", hash = "sha256:08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44", size = 27697, upload-time = "2022-10-25T02:36:22.414Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl", hash = "sha256:4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6", size = 25335, upload-time = "2022-10-25T02:36:20.889Z" },

+]

+

+[[package]]

+name = "iniconfig"

+version = "2.3.0"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/72/34/14ca021ce8e5dfedc35312d08ba8bf51fdd999c576889fc2c24cb97f4f10/iniconfig-2.3.0.tar.gz", hash = "sha256:c76315c77db068650d49c5b56314774a7804df16fee4402c1f19d6d15d8c4730", size = 20503, upload-time = "2025-10-18T21:55:43.219Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/cb/b1/3846dd7f199d53cb17f49cba7e651e9ce294d8497c8c150530ed11865bb8/iniconfig-2.3.0-py3-none-any.whl", hash = "sha256:f631c04d2c48c52b84d0d0549c99ff3859c98df65b3101406327ecc7d53fbf12", size = 7484, upload-time = "2025-10-18T21:55:41.639Z" },

+]

+

+[[package]]

+name = "lxml"

+version = "6.1.1"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/05/3b/aab6728cae887456f409b4d75e8a01856e4f04bd510de38052a47768b680/lxml-6.1.1.tar.gz", hash = "sha256:ba96ae44888e0185281e937633a743ea90d5a196c6000f82565ebb0580012d40", size = 4197430, upload-time = "2026-05-18T19:19:06.424Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/62/b0/83f481780d1548750b8ce2ec824073deef2f452d9cd1a6faff8507e3d16d/lxml-6.1.1-cp311-cp311-macosx_10_9_universal2.whl", hash = "sha256:53b7d2b7a10b1c35c0a5e21e9224accf60c1bbfba523990732e521b2b73adef2", size = 8526461, upload-time = "2026-05-18T19:17:25.862Z" },

+    { url = "https://files.pythonhosted.org/packages/b9/d5/30fa0f808002c7329397bfbb24e306789c0b29f04aa5842c07b174b4216f/lxml-6.1.1-cp311-cp311-macosx_10_9_x86_64.whl", hash = "sha256:ff3f333630ab480244a1bff72043e511a91eb22e7595dead8653ee5612dd8f3d", size = 4595375, upload-time = "2026-05-18T19:17:34.555Z" },

+    { url = "https://files.pythonhosted.org/packages/4f/d2/edb71cf0e561581a7c5eb2626244320eb04e9f8ce6d563184fd668b45073/lxml-6.1.1-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:a4bbea04c97f6d78a48e3fbc1cb9116d2780b1b39e03a23f6eb9b603fd61f510", size = 4923654, upload-time = "2026-05-18T19:17:42.917Z" },

+    { url = "https://files.pythonhosted.org/packages/4c/77/1bc7eeb0de4577d783fb625aa092cc9357883bba35845a3666bf1259f3dc/lxml-6.1.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:db1d75f6617a49c1c01bc7023713e0ff59ab32c9579ae62a7674c0e34f3b0b0a", size = 5067921, upload-time = "2026-05-18T19:17:49.175Z" },

+    { url = "https://files.pythonhosted.org/packages/1b/3c/c0690d74bd2bc17bc03b5b0d093569ead597dd0bfa088bf99eef8c24e19c/lxml-6.1.1-cp311-cp311-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:3a12689be69a28ddaa0ab99a5a1137da2afd5f8f16df7b5680b66f616d3eda1d", size = 5002456, upload-time = "2026-05-18T19:17:59.715Z" },

+    { url = "https://files.pythonhosted.org/packages/66/8d/d1b3271af0c0f1e27e8472a849e4d2c65bc7766884b9ad2da9e76e145c88/lxml-6.1.1-cp311-cp311-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:18b73c339ae29b90fd2d06e58ebd555a751bde9cd6bbd36cc0281b9a2c94e9d8", size = 5202776, upload-time = "2026-05-18T19:18:08.924Z" },

+    { url = "https://files.pythonhosted.org/packages/7a/45/689824ffb237fd10125ad273f32b28ff04dc6203c2822c85ff65a93df65e/lxml-6.1.1-cp311-cp311-manylinux_2_28_i686.whl", hash = "sha256:752d3bbfe874715ccd0aec7f88d7fc623c0f1fd7aa7b3238a084e017bad2a009", size = 5329945, upload-time = "2026-05-18T19:18:13.673Z" },

+    { url = "https://files.pythonhosted.org/packages/5d/c0/ef73af53767e958fd87d437c170f272e2f6e6c0f854939f133a895f1e711/lxml-6.1.1-cp311-cp311-manylinux_2_31_armv7l.whl", hash = "sha256:6b1761fbf9ec984e2e9d9c589ef5f5fd684b7c19f92aadd567a26c5224958db6", size = 4659237, upload-time = "2026-05-18T19:18:18.657Z" },

+    { url = "https://files.pythonhosted.org/packages/a0/5e/e1158e40397585e91cb0472374a1f63d0926a1ddeaa92f13d1a1ffe306d5/lxml-6.1.1-cp311-cp311-manylinux_2_38_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:d680fbcb768404c601ecb43519ecd8461f6954cb11c06a78962f666832ccfca8", size = 5265904, upload-time = "2026-05-18T19:18:24.883Z" },

+    { url = "https://files.pythonhosted.org/packages/a0/16/8687e5d1400ed1c0bc41dace232ebb7553952b618ea1f2e5fb6e2cfbbe23/lxml-6.1.1-cp311-cp311-musllinux_1_2_aarch64.whl", hash = "sha256:162af1091cd785f2f27e62d3547ae9bc58ec5c86dd314d67021fd02463708d83", size = 5045225, upload-time = "2026-05-18T19:17:20.073Z" },

+    { url = "https://files.pythonhosted.org/packages/ca/18/d877bd1ae2e5ffdfd4836565aba350db31feb2f2656d6ce70316ed66a05e/lxml-6.1.1-cp311-cp311-musllinux_1_2_armv7l.whl", hash = "sha256:e9308ff8241c532df3f3e570f9a5aeed6c853f888512ba4b75638d7c11c95ef6", size = 4712721, upload-time = "2026-05-18T19:17:40.512Z" },

+    { url = "https://files.pythonhosted.org/packages/44/4d/1f44fd1d770b10dacbf6b5c6e520f4d6e0708744930f719dc04e67cab981/lxml-6.1.1-cp311-cp311-musllinux_1_2_riscv64.whl", hash = "sha256:5f6994074ebae6ffb04447268e37dc16edc304f9859cf91acb86e0af6c1b395c", size = 5252549, upload-time = "2026-05-18T19:17:51.236Z" },

+    { url = "https://files.pythonhosted.org/packages/64/5d/1d66b84f850089254c230ef6ea6b267a5a54e2e179a5d960036a05d501d7/lxml-6.1.1-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:80c2dfadb855da477cf73373ad29a333535dedb9b12bad02c9814c8e2b43bf08", size = 5226877, upload-time = "2026-05-18T19:18:00.875Z" },

+    { url = "https://files.pythonhosted.org/packages/ad/00/84c4b5302d42a2d0184f38d538c8a197f33b52a50bd4f7bcfe990bce3036/lxml-6.1.1-cp311-cp311-win32.whl", hash = "sha256:30a89d3ac8faec007453fb541f3f46807eeec88edd5826f6e3fe001752a2c621", size = 3594072, upload-time = "2026-05-18T19:17:12.714Z" },

+    { url = "https://files.pythonhosted.org/packages/61/9d/2e2f7d876349f45e0f3e29f72da311668853d59b58d473a2dea4f0160135/lxml-6.1.1-cp311-cp311-win_amd64.whl", hash = "sha256:abbefa31eee84842140f67acef1c828e28bba8bbf0c3bc6e5492a9af88152c28", size = 4025469, upload-time = "2026-05-18T19:17:50.566Z" },

+    { url = "https://files.pythonhosted.org/packages/b0/d5/570e6390e4110331e6208b2ba83d1482cc9146808ee118b22824a34c1070/lxml-6.1.1-cp311-cp311-win_arm64.whl", hash = "sha256:dcb292aa7fe485ceff7af4f92e46c5af397daec5dff64871a528f0fc47a3cc5b", size = 3667640, upload-time = "2026-05-19T19:22:48.293Z" },

+    { url = "https://files.pythonhosted.org/packages/b5/32/86a3f0f724a3a402d4627937a7fc27b160e45e7012b4adf47f6e1e844511/lxml-6.1.1-pp311-pypy311_pp73-macosx_10_15_x86_64.whl", hash = "sha256:31033dc34636ea6b7d5cc11b1ddbda78a14de858ba9d3e1ed4b69a3085bc521e", size = 3930127, upload-time = "2026-05-18T19:19:02.27Z" },

+    { url = "https://files.pythonhosted.org/packages/40/44/d832e82af08723761556d004b1d04d281c09f9a8cecd7d3148548c9941a3/lxml-6.1.1-pp311-pypy311_pp73-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:3893c14c4b6ac5b2d54ba8cf03e99fe5104e592de491f19bd6b82756c09f8004", size = 4210769, upload-time = "2026-05-18T19:20:41.427Z" },

+    { url = "https://files.pythonhosted.org/packages/6d/39/0dc5949f759ed7d951e0bb8c2f2d9d7aca1908d22352fa84a8afd2ea54af/lxml-6.1.1-pp311-pypy311_pp73-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:c07da4cebf6889f03ebac8d238f62318e29f495de0aa18a51ea14e61ae907e2e", size = 4318163, upload-time = "2026-05-18T19:20:44.702Z" },

+    { url = "https://files.pythonhosted.org/packages/e6/fb/8ab3845fe046ba4cbf74536bcf6801a774b7caf4350de1c5d37f1f0a9e90/lxml-6.1.1-pp311-pypy311_pp73-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:f6f0ce10945fab9c4c06ce14e22af9059d1a87493a9af4501a5b0b9187e21cf2", size = 4250945, upload-time = "2026-05-18T19:20:47.385Z" },

+    { url = "https://files.pythonhosted.org/packages/68/1b/7553ab136894374ffae8851ec06f98f511cd8e66246e41b6be059d0a7289/lxml-6.1.1-pp311-pypy311_pp73-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:f8844cd288697c6425c9beba919302241e3278871dc6519515e72b04e987abcf", size = 4401664, upload-time = "2026-05-18T19:20:50.489Z" },

+    { url = "https://files.pythonhosted.org/packages/db/a4/441aee36c6f6b249823d20fd91f9be9ab89d7c5a8ae542a4a4ca6d342d56/lxml-6.1.1-pp311-pypy311_pp73-win_amd64.whl", hash = "sha256:ed21202aec73cda4d55d1ce57b389aadb90ffb044e6cd1080b8347efe1b1ec84", size = 3508989, upload-time = "2026-05-18T19:18:38.158Z" },

+]

+

+[[package]]

+name = "numpy"

+version = "2.4.6"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/d0/ad/fed0499ce6a338d2a03ebae59cd15093910c8875328855781952abf6c2fe/numpy-2.4.6.tar.gz", hash = "sha256:f3a3570c4a2a16746ac2c31a7c7c7b0c186b95ce902e33db6f28094ed7387dda", size = 20735807, upload-time = "2026-05-18T23:37:14.07Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/b3/49/ec46835a70be8fa6446c495126ac84fdb28cb2558e1620ffb87a10c8b64c/numpy-2.4.6-cp311-cp311-macosx_10_9_x86_64.whl", hash = "sha256:0280e0356c0829a18d9de1cb7eee50ec22ca639878d7240307ca0943d73cd2c4", size = 16969194, upload-time = "2026-05-18T23:33:13.503Z" },

+    { url = "https://files.pythonhosted.org/packages/0e/0d/f5957185c0ee2f3e12f78715aa9e3b353fd83633316c8532b38faa37e3f6/numpy-2.4.6-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:110f8b71aacb688ec69062bb7f6938a0f8acb01b7c1c4beb453c65b6d234584d", size = 14964111, upload-time = "2026-05-18T23:33:17.795Z" },

+    { url = "https://files.pythonhosted.org/packages/ad/40/40a40ee0ddf7ceb782c49af278894b686e586d65d8c1889c8b5da01a3d7d/numpy-2.4.6-cp311-cp311-macosx_14_0_arm64.whl", hash = "sha256:4cfe66903cc32a9921a6733d96b19bb6abf310397581bbad89c228f5abaf0ee8", size = 5469159, upload-time = "2026-05-18T23:33:20.654Z" },

+    { url = "https://files.pythonhosted.org/packages/63/13/f9a8046535cb21deae82f8d03de9617e08882d274fad2539630761888228/numpy-2.4.6-cp311-cp311-macosx_14_0_x86_64.whl", hash = "sha256:8155154c7c691289fe18f510b5d4657c68c67989f293f0535a91360392ff6538", size = 6798936, upload-time = "2026-05-18T23:33:22.987Z" },

+    { url = "https://files.pythonhosted.org/packages/33/a8/6fa8c1a345a8c85dbb21932c447bee07c30a2c2a3f31e369c0a84b300147/numpy-2.4.6-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:0ab0a9c4ffb1a6d95ef519fe4247dba8eb6b18ad93999f76b7f657039acabd47", size = 15966692, upload-time = "2026-05-18T23:33:26.62Z" },

+    { url = "https://files.pythonhosted.org/packages/02/03/74fe2a4cb3817d94d86402f2506554130a2f01414e299b5a843e5a8a957f/numpy-2.4.6-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:89cd468399cfd2504718f0ba50e410dca55a170b61a02ad92bb18c8a65186e93", size = 16918164, upload-time = "2026-05-18T23:33:29.955Z" },

+    { url = "https://files.pythonhosted.org/packages/c5/80/3615be3313f7e7696609bc194b9f0101da809df79e859bdb84e0cd043f46/numpy-2.4.6-cp311-cp311-musllinux_1_2_aarch64.whl", hash = "sha256:c2d37ab77531417474168eb79d6d80b14f821a966818505d03013d0833edb7a8", size = 17322877, upload-time = "2026-05-18T23:33:34.724Z" },

+    { url = "https://files.pythonhosted.org/packages/ca/ac/a691e0fe2675e370d0e08ff905adc49a1c8830e8cae03efe4477e92cd55d/numpy-2.4.6-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:f407cb6b8e9d6d8c626bc73c945db1706035af8fd632295547bf1c9e46d092d6", size = 18651487, upload-time = "2026-05-18T23:33:38.217Z" },

+    { url = "https://files.pythonhosted.org/packages/15/a7/9bc1cd626d7bf6869bfedf27b91b6ab5dd607758bf8e959d6fa80c6a59cb/numpy-2.4.6-cp311-cp311-win32.whl", hash = "sha256:ddea102b48f9e339f3948bf22040944184627a30fdf7f858667673b9c5f033c8", size = 6233945, upload-time = "2026-05-18T23:33:41.331Z" },

+    { url = "https://files.pythonhosted.org/packages/c5/31/7fc6239c12bce7e931463251cca4426c465e1876ba3cc785402ef4dd8f4e/numpy-2.4.6-cp311-cp311-win_amd64.whl", hash = "sha256:1e254a00cdf42b1e4d5b3d68d33af63268d41340d8885df2ab6470f2e1500147", size = 12608406, upload-time = "2026-05-18T23:33:44.131Z" },

+    { url = "https://files.pythonhosted.org/packages/27/83/140f85a466595a16382996a1bf06b2b54bcd597488921b0c9daaeeda72af/numpy-2.4.6-cp311-cp311-win_arm64.whl", hash = "sha256:ed9749eef4cbd126da3dc1d6bcb3a57f5eb7ac6a6484146bdbf743f552dfc577", size = 10479528, upload-time = "2026-05-18T23:33:50.725Z" },

+    { url = "https://files.pythonhosted.org/packages/de/12/b422cc84439adc0d00de605bf4a308890ae5c26f2c71fbd73e5d08fbb0dd/numpy-2.4.6-pp311-pypy311_pp73-macosx_10_15_x86_64.whl", hash = "sha256:55cced7c52e981362f708ad635198e97a752dfba412cc03c23bbf3bd8d5cd662", size = 16847511, upload-time = "2026-05-18T23:36:50.673Z" },

+    { url = "https://files.pythonhosted.org/packages/44/53/f481bef68011740f8849418d82db07230e825013f31f4eef5ba5b805316a/numpy-2.4.6-pp311-pypy311_pp73-macosx_11_0_arm64.whl", hash = "sha256:d6da64deb6b8ed903e7560180a92f2d804ee1ba5eeb849ac2748b8c1aba1f6d7", size = 14889064, upload-time = "2026-05-18T23:36:53.879Z" },

+    { url = "https://files.pythonhosted.org/packages/7f/57/42ed575c10ced8af951d426bc4e1f8aff16fd851db33f067036215a7f860/numpy-2.4.6-pp311-pypy311_pp73-macosx_14_0_arm64.whl", hash = "sha256:68a5124b13fa6cc2086764a20005d30bc0548146f7f5322f02fce212ca14317f", size = 5394157, upload-time = "2026-05-18T23:36:57.194Z" },

+    { url = "https://files.pythonhosted.org/packages/6a/ef/f66cc724fcc36c1e364c67f51ae9146090b8b584f27d58b97fdae3edd737/numpy-2.4.6-pp311-pypy311_pp73-macosx_14_0_x86_64.whl", hash = "sha256:948424b06129ce883307e8cff868c31396d8dc7630a59c61d70d98dbe70f222c", size = 6708728, upload-time = "2026-05-18T23:36:59.575Z" },

+    { url = "https://files.pythonhosted.org/packages/1a/9c/c531f2293b91265d8b48e9b329f54fdd7ffae73cb4134ea10cca4237e9cc/numpy-2.4.6-pp311-pypy311_pp73-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:5dbbdb29840ca3d91ee0fece42fc29278886d908280bfec0a5846c6f901a3eb0", size = 15798374, upload-time = "2026-05-18T23:37:02.674Z" },

+    { url = "https://files.pythonhosted.org/packages/1a/b0/413077f6b1153ed3cba361401c6783bbad6114804a000cc22eb71c13e190/numpy-2.4.6-pp311-pypy311_pp73-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:8ad03c0965fb3c692200e74d458ca28c1dbb4ce96f9a479a8aa041ad5fabca02", size = 16747286, upload-time = "2026-05-18T23:37:06.327Z" },

+    { url = "https://files.pythonhosted.org/packages/15/ce/e5ec180bc41812edcd8daeb8639d205622c0e8c02259d8ab25a0201b3c2a/numpy-2.4.6-pp311-pypy311_pp73-win_amd64.whl", hash = "sha256:2803abfebfc990042cd494d8ce2d5f82e9d847af6d35ec486923aa19dbad5e73", size = 12504263, upload-time = "2026-05-18T23:37:09.715Z" },

+]

+

+[[package]]

+name = "packaging"

+version = "26.2"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/d7/f1/e7a6dd94a8d4a5626c03e4e99c87f241ba9e350cd9e6d75123f992427270/packaging-26.2.tar.gz", hash = "sha256:ff452ff5a3e828ce110190feff1178bb1f2ea2281fa2075aadb987c2fb221661", size = 228134, upload-time = "2026-04-24T20:15:23.917Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/df/b2/87e62e8c3e2f4b32e5fe99e0b86d576da1312593b39f47d8ceef365e95ed/packaging-26.2-py3-none-any.whl", hash = "sha256:5fc45236b9446107ff2415ce77c807cee2862cb6fac22b8a73826d0693b0980e", size = 100195, upload-time = "2026-04-24T20:15:22.081Z" },

+]

+

+[[package]]

+name = "pillow"

+version = "12.2.0"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/8c/21/c2bcdd5906101a30244eaffc1b6e6ce71a31bd0742a01eb89e660ebfac2d/pillow-12.2.0.tar.gz", hash = "sha256:a830b1a40919539d07806aa58e1b114df53ddd43213d9c8b75847eee6c0182b5", size = 46987819, upload-time = "2026-04-01T14:46:17.687Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/68/e1/748f5663efe6edcfc4e74b2b93edfb9b8b99b67f21a854c3ae416500a2d9/pillow-12.2.0-cp311-cp311-macosx_10_10_x86_64.whl", hash = "sha256:8be29e59487a79f173507c30ddf57e733a357f67881430449bb32614075a40ab", size = 5354347, upload-time = "2026-04-01T14:42:44.255Z" },

+    { url = "https://files.pythonhosted.org/packages/47/a1/d5ff69e747374c33a3b53b9f98cca7889fce1fd03d79cdc4e1bccc6c5a87/pillow-12.2.0-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:71cde9a1e1551df7d34a25462fc60325e8a11a82cc2e2f54578e5e9a1e153d65", size = 4695873, upload-time = "2026-04-01T14:42:46.452Z" },

+    { url = "https://files.pythonhosted.org/packages/df/21/e3fbdf54408a973c7f7f89a23b2cb97a7ef30c61ab4142af31eee6aebc88/pillow-12.2.0-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:f490f9368b6fc026f021db16d7ec2fbf7d89e2edb42e8ec09d2c60505f5729c7", size = 6280168, upload-time = "2026-04-01T14:42:49.228Z" },

+    { url = "https://files.pythonhosted.org/packages/d3/f1/00b7278c7dd52b17ad4329153748f87b6756ec195ff786c2bdf12518337d/pillow-12.2.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:8bd7903a5f2a4545f6fd5935c90058b89d30045568985a71c79f5fd6edf9b91e", size = 8088188, upload-time = "2026-04-01T14:42:51.735Z" },

+    { url = "https://files.pythonhosted.org/packages/ad/cf/220a5994ef1b10e70e85748b75649d77d506499352be135a4989c957b701/pillow-12.2.0-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:3997232e10d2920a68d25191392e3a4487d8183039e1c74c2297f00ed1c50705", size = 6394401, upload-time = "2026-04-01T14:42:54.343Z" },

+    { url = "https://files.pythonhosted.org/packages/e9/bd/e51a61b1054f09437acfbc2ff9106c30d1eb76bc1453d428399946781253/pillow-12.2.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:e74473c875d78b8e9d5da2a70f7099549f9eb37ded4e2f6a463e60125bccd176", size = 7079655, upload-time = "2026-04-01T14:42:56.954Z" },

+    { url = "https://files.pythonhosted.org/packages/6b/3d/45132c57d5fb4b5744567c3817026480ac7fc3ce5d4c47902bc0e7f6f853/pillow-12.2.0-cp311-cp311-musllinux_1_2_aarch64.whl", hash = "sha256:56a3f9c60a13133a98ecff6197af34d7824de9b7b38c3654861a725c970c197b", size = 6503105, upload-time = "2026-04-01T14:42:59.847Z" },

+    { url = "https://files.pythonhosted.org/packages/7d/2e/9df2fc1e82097b1df3dce58dc43286aa01068e918c07574711fcc53e6fb4/pillow-12.2.0-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:90e6f81de50ad6b534cab6e5aef77ff6e37722b2f5d908686f4a5c9eba17a909", size = 7203402, upload-time = "2026-04-01T14:43:02.664Z" },

+    { url = "https://files.pythonhosted.org/packages/bd/2e/2941e42858ebb67e50ae741473de81c2984e6eff7b397017623c676e2e8d/pillow-12.2.0-cp311-cp311-win32.whl", hash = "sha256:8c984051042858021a54926eb597d6ee3012393ce9c181814115df4c60b9a808", size = 6378149, upload-time = "2026-04-01T14:43:05.274Z" },

+    { url = "https://files.pythonhosted.org/packages/69/42/836b6f3cd7f3e5fa10a1f1a5420447c17966044c8fbf589cc0452d5502db/pillow-12.2.0-cp311-cp311-win_amd64.whl", hash = "sha256:6e6b2a0c538fc200b38ff9eb6628228b77908c319a005815f2dde585a0664b60", size = 7082626, upload-time = "2026-04-01T14:43:08.557Z" },

+    { url = "https://files.pythonhosted.org/packages/c2/88/549194b5d6f1f494b485e493edc6693c0a16f4ada488e5bd974ed1f42fad/pillow-12.2.0-cp311-cp311-win_arm64.whl", hash = "sha256:9a8a34cc89c67a65ea7437ce257cea81a9dad65b29805f3ecee8c8fe8ff25ffe", size = 2463531, upload-time = "2026-04-01T14:43:10.743Z" },

+    { url = "https://files.pythonhosted.org/packages/4e/b7/2437044fb910f499610356d1352e3423753c98e34f915252aafecc64889f/pillow-12.2.0-pp311-pypy311_pp73-macosx_10_15_x86_64.whl", hash = "sha256:0538bd5e05efec03ae613fd89c4ce0368ecd2ba239cc25b9f9be7ed426b0af1f", size = 5273969, upload-time = "2026-04-01T14:45:55.538Z" },

+    { url = "https://files.pythonhosted.org/packages/f6/f4/8316e31de11b780f4ac08ef3654a75555e624a98db1056ecb2122d008d5a/pillow-12.2.0-pp311-pypy311_pp73-macosx_11_0_arm64.whl", hash = "sha256:394167b21da716608eac917c60aa9b969421b5dcbbe02ae7f013e7b85811c69d", size = 4659674, upload-time = "2026-04-01T14:45:58.093Z" },

+    { url = "https://files.pythonhosted.org/packages/d4/37/664fca7201f8bb2aa1d20e2c3d5564a62e6ae5111741966c8319ca802361/pillow-12.2.0-pp311-pypy311_pp73-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:5d04bfa02cc2d23b497d1e90a0f927070043f6cbf303e738300532379a4b4e0f", size = 5288479, upload-time = "2026-04-01T14:46:01.141Z" },

+    { url = "https://files.pythonhosted.org/packages/49/62/5b0ed78fce87346be7a5cfcfaaad91f6a1f98c26f86bdbafa2066c647ef6/pillow-12.2.0-pp311-pypy311_pp73-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:0c838a5125cee37e68edec915651521191cef1e6aa336b855f495766e77a366e", size = 7032230, upload-time = "2026-04-01T14:46:03.874Z" },

+    { url = "https://files.pythonhosted.org/packages/c3/28/ec0fc38107fc32536908034e990c47914c57cd7c5a3ece4d8d8f7ffd7e27/pillow-12.2.0-pp311-pypy311_pp73-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:4a6c9fa44005fa37a91ebfc95d081e8079757d2e904b27103f4f5fa6f0bf78c0", size = 5355404, upload-time = "2026-04-01T14:46:06.33Z" },

+    { url = "https://files.pythonhosted.org/packages/5e/8b/51b0eddcfa2180d60e41f06bd6d0a62202b20b59c68f5a132e615b75aecf/pillow-12.2.0-pp311-pypy311_pp73-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:25373b66e0dd5905ed63fa3cae13c82fbddf3079f2c8bf15c6fb6a35586324c1", size = 6002215, upload-time = "2026-04-01T14:46:08.83Z" },

+    { url = "https://files.pythonhosted.org/packages/bc/60/5382c03e1970de634027cee8e1b7d39776b778b81812aaf45b694dfe9e28/pillow-12.2.0-pp311-pypy311_pp73-win_amd64.whl", hash = "sha256:bfa9c230d2fe991bed5318a5f119bd6780cda2915cca595393649fc118ab895e", size = 7080946, upload-time = "2026-04-01T14:46:11.734Z" },

+]

+

+[[package]]

+name = "pluggy"

+version = "1.6.0"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/f9/e2/3e91f31a7d2b083fe6ef3fa267035b518369d9511ffab804f839851d2779/pluggy-1.6.0.tar.gz", hash = "sha256:7dcc130b76258d33b90f61b658791dede3486c3e6bfb003ee5c9bfb396dd22f3", size = 69412, upload-time = "2025-05-15T12:30:07.975Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/54/20/4d324d65cc6d9205fabedc306948156824eb9f0ee1633355a8f7ec5c66bf/pluggy-1.6.0-py3-none-any.whl", hash = "sha256:e920276dd6813095e9377c0bc5566d94c932c33b27a3e3945d8389c374dd4746", size = 20538, upload-time = "2025-05-15T12:30:06.134Z" },

+]

+

+[[package]]

+name = "pydantic"

+version = "2.13.4"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "annotated-types" },

+    { name = "pydantic-core" },

+    { name = "typing-extensions" },

+    { name = "typing-inspection" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/18/a5/b60d21ac674192f8ab0ba4e9fd860690f9b4a6e51ca5df118733b487d8d6/pydantic-2.13.4.tar.gz", hash = "sha256:c40756b57adaa8b1efeeced5c196f3f3b7c435f90e84ea7f443901bec8099ef6", size = 844775, upload-time = "2026-05-06T13:43:05.343Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/fd/7b/122376b1fd3c62c1ed9dc80c931ace4844b3c55407b6fb2d199377c9736f/pydantic-2.13.4-py3-none-any.whl", hash = "sha256:45a282cde31d808236fd7ea9d919b128653c8b38b393d1c4ab335c62924d9aba", size = 472262, upload-time = "2026-05-06T13:43:02.641Z" },

+]

+

+[[package]]

+name = "pydantic-core"

+version = "2.46.4"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "typing-extensions" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/9d/56/921726b776ace8d8f5db44c4ef961006580d91dc52b803c489fafd1aa249/pydantic_core-2.46.4.tar.gz", hash = "sha256:62f875393d7f270851f20523dd2e29f082bcc82292d66db2b64ea71f64b6e1c1", size = 471464, upload-time = "2026-05-06T13:37:06.98Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/5c/fa/6d7708d2cfc1a832acb6aeb0cd16e801902df8a0f583bb3b4b527fde022e/pydantic_core-2.46.4-cp311-cp311-macosx_10_12_x86_64.whl", hash = "sha256:0e96592440881c74a213e5ad528e2b24d3d4f940de2766bed9010ab1d9e51594", size = 2111872, upload-time = "2026-05-06T13:40:27.596Z" },

+    { url = "https://files.pythonhosted.org/packages/ae/6f/aa064a3e74b5745afbdf250594f38e7ead05e2d651bcb35994b9417a0d4d/pydantic_core-2.46.4-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:e0d65b8c354be7fb5f720c3caa8bc940bc2d20ce749c8e06135f07f8ed95dd7c", size = 1948255, upload-time = "2026-05-06T13:39:12.574Z" },

+    { url = "https://files.pythonhosted.org/packages/43/3a/41114a9f7569b84b4d84e7a018c57c56347dac30c0d4a872946ec4e36c46/pydantic_core-2.46.4-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:7bfb192b3f4b9e8a89b6277b6ce787564f62cfd272055f6e685726b111dc7826", size = 1972827, upload-time = "2026-05-06T13:38:19.841Z" },

+    { url = "https://files.pythonhosted.org/packages/ef/25/1ab42e8048fe551934d9884e8d64daa7e990ad386f310a15981aeb6a5b08/pydantic_core-2.46.4-cp311-cp311-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:9037063db01f09b09e237c282b6792bd4da634b5402c4e7f0c61effed7701a04", size = 2041051, upload-time = "2026-05-06T13:38:10.447Z" },

+    { url = "https://files.pythonhosted.org/packages/94/c2/1a934597ddf08da410385b3b7aae91956a5a76c635effef456074fad7e88/pydantic_core-2.46.4-cp311-cp311-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:fc010ab034c8c7452522748bf937df58020d256ccae0874463d1f4d01758af8e", size = 2221314, upload-time = "2026-05-06T13:40:13.089Z" },

+    { url = "https://files.pythonhosted.org/packages/02/6d/9e8ad178c9c4df27ad3c8f25d1fe2a7ab0d2ba0559fad4aee5d3d1f16771/pydantic_core-2.46.4-cp311-cp311-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:8c5dac79fa1614d1e06ca695109c6105923bd9c7d1d6c918d4e637b7e6b32fd3", size = 2285146, upload-time = "2026-05-06T13:38:59.224Z" },

+    { url = "https://files.pythonhosted.org/packages/80/50/540cd3aeefc041beb111125c4bff779831a2111fc6b15a9138cda277d32c/pydantic_core-2.46.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:f9fa868638bf362d3d138ea55829cefb3d5f4b0d7f142234382a15e2485dbec4", size = 2089685, upload-time = "2026-05-06T13:38:17.762Z" },

+    { url = "https://files.pythonhosted.org/packages/6b/a4/b440ad35f05f6a38f89fa0f149accb3f0e02be94ca5e15f3c449a61b4bc9/pydantic_core-2.46.4-cp311-cp311-manylinux_2_31_riscv64.whl", hash = "sha256:17299feefe090f2caa5b8e37222bb5f663e4935a8bfa6931d4102e5df1a9f398", size = 2115420, upload-time = "2026-05-06T13:37:58.195Z" },

+    { url = "https://files.pythonhosted.org/packages/99/61/de4f55db8dfd57bfdfa9a12ec90fe1b57c4f41062f7ca86f08586b3e0ac0/pydantic_core-2.46.4-cp311-cp311-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:4c63ebc82684aa89d9a3bcbd13d515b3be44250dc68dd3bd81526c1cb31286c3", size = 2165122, upload-time = "2026-05-06T13:37:01.167Z" },

+    { url = "https://files.pythonhosted.org/packages/f7/52/7c529d7bdb2d1068bd52f51fe32572c8301f9a4febf1948f10639f1436f5/pydantic_core-2.46.4-cp311-cp311-musllinux_1_1_aarch64.whl", hash = "sha256:aaa2a54443eff1950ba5ddc6b6ccda0d9c84a364276a62f969bdf2a390650848", size = 2182573, upload-time = "2026-05-06T13:38:45.04Z" },

+    { url = "https://files.pythonhosted.org/packages/37/b3/7c40325848ba78247f2812dcf9c7274e38cd801820ca6dd9fe63bcfb0eb4/pydantic_core-2.46.4-cp311-cp311-musllinux_1_1_armv7l.whl", hash = "sha256:18e5ceec2ab67e6d5f1a9085e5a24c9c4e2ac4545730bfe668680bca05e555f3", size = 2317139, upload-time = "2026-05-06T13:37:15.539Z" },

+    { url = "https://files.pythonhosted.org/packages/d9/37/f913f81a657c865b75da6c0dbed79876073c2a43b5bd9edbe8da785e4d49/pydantic_core-2.46.4-cp311-cp311-musllinux_1_1_x86_64.whl", hash = "sha256:a0f62d0a58f4e7da165457e995725421e0064f2255d8eccebc49f41bbc23b109", size = 2360433, upload-time = "2026-05-06T13:37:30.099Z" },

+    { url = "https://files.pythonhosted.org/packages/c4/67/6acaa1be2567f9256b056d8477158cac7240813956ce86e49deae8e173b4/pydantic_core-2.46.4-cp311-cp311-win32.whl", hash = "sha256:041bde0a48fd37cf71cab1c9d56d3e8625a3793fef1f7dd232b3ff37e978ecda", size = 1985513, upload-time = "2026-05-06T13:38:15.669Z" },

+    { url = "https://files.pythonhosted.org/packages/aa/e6/c505f83dfeda9a2e5c995cfd872949e4d05e12f7feb3dca72f633daefa94/pydantic_core-2.46.4-cp311-cp311-win_amd64.whl", hash = "sha256:6f2eeda33a839975441c86a4119e1383c50b47faf0cbb5176985565c6bb02c33", size = 2071114, upload-time = "2026-05-06T13:40:35.416Z" },

+    { url = "https://files.pythonhosted.org/packages/0f/da/7a263a96d965d9d0df5e8de8a475f33495451117035b09acb110288c381f/pydantic_core-2.46.4-cp311-cp311-win_arm64.whl", hash = "sha256:14f4c5d6db102bd796a627bbb3a17b4cf4574b9ae861d8b7c9a9661c6dd3362d", size = 2044298, upload-time = "2026-05-06T13:38:29.754Z" },

+    { url = "https://files.pythonhosted.org/packages/ee/a4/73995fd4ebbb46ba0ee51e6fa049b8f02c40daebb762208feda8a6b7894d/pydantic_core-2.46.4-graalpy311-graalpy242_311_native-macosx_10_12_x86_64.whl", hash = "sha256:14d4edf427bdcf950a8a02d7cb44a08614388dd6e1bdcbf4f67504fa7887da9c", size = 2111589, upload-time = "2026-05-06T13:37:10.817Z" },

+    { url = "https://files.pythonhosted.org/packages/fb/7f/f37d3a5e8bfcc2e403f5c57a730f2d815693fb42119e8ea48b3789335af1/pydantic_core-2.46.4-graalpy311-graalpy242_311_native-macosx_11_0_arm64.whl", hash = "sha256:0ce40cd7b21210e99342afafbd4d0f76d784eb5b1d60f3bdc566be4983c6c73b", size = 1944552, upload-time = "2026-05-06T13:36:56.717Z" },

+    { url = "https://files.pythonhosted.org/packages/15/3c/d7eb777b3ff43e8433a4efb39a17aa8fd98a4ee8561a24a67ef5db07b2d6/pydantic_core-2.46.4-graalpy311-graalpy242_311_native-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:90884113d8b48f760e9587002789ddd741e76ab9f89518cd1e43b1f1a52ec44b", size = 1982984, upload-time = "2026-05-06T13:39:06.207Z" },

+    { url = "https://files.pythonhosted.org/packages/63/87/70b9f40170a81afd55ca26c9b2acb25c20d64bcfbf888fafecb3ba077d4c/pydantic_core-2.46.4-graalpy311-graalpy242_311_native-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:66ce7632c22d837c95301830e111ad0128a32b8207533b60896a96c4915192ea", size = 2138417, upload-time = "2026-05-06T13:39:45.476Z" },

+    { url = "https://files.pythonhosted.org/packages/11/cb/428de0385b6c8d44b716feba566abfacfbd23ee3c4439faa789a1456242f/pydantic_core-2.46.4-pp311-pypy311_pp73-macosx_10_12_x86_64.whl", hash = "sha256:0c563b08bca408dc7f65f700633d8442fffb2421fc47b8101377e9fd65051ff0", size = 2112782, upload-time = "2026-05-06T13:37:04.016Z" },

+    { url = "https://files.pythonhosted.org/packages/0b/b5/6a17bdadd0fc1f170adfd05a20d37c832f52b117b4d9131da1f41bb097ce/pydantic_core-2.46.4-pp311-pypy311_pp73-macosx_11_0_arm64.whl", hash = "sha256:db06ffe51636ffe9ca531fe9023dd64bdd794be8754cb5df57c5498ae5b518a7", size = 1952146, upload-time = "2026-05-06T13:39:43.092Z" },

+    { url = "https://files.pythonhosted.org/packages/2a/dc/03734d80e362cd43ef65428e9de77c730ce7f2f11c60d2b1e1b39f0fbf99/pydantic_core-2.46.4-pp311-pypy311_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:133878133d271ade3d41d1bfb2a45ec38dbdbda40bc065921c6b04e4630127e2", size = 2134492, upload-time = "2026-05-06T13:36:58.124Z" },

+    { url = "https://files.pythonhosted.org/packages/de/df/5e5ffc085ed07cc22d298134d3d911c63e91f6a0eb91fe646750a3209910/pydantic_core-2.46.4-pp311-pypy311_pp73-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:9bc519fbf2b7578398853d815009ae5e4d4603d12f4e3f91da8c06852d3da3e9", size = 2156604, upload-time = "2026-05-06T13:37:49.88Z" },

+    { url = "https://files.pythonhosted.org/packages/81/44/6e112a4253e56f5705467cbab7ab5e91ee7398ba3d56d358635958893d3e/pydantic_core-2.46.4-pp311-pypy311_pp73-musllinux_1_1_aarch64.whl", hash = "sha256:c7a7bd4e39e8e4c12c39cd480356842b6a8a06e41b23a55a5e3e191718838ddf", size = 2183828, upload-time = "2026-05-06T13:37:43.053Z" },

+    { url = "https://files.pythonhosted.org/packages/ac/ad/5565071e937d8e752842ac241463944c9eb14c87e2d269f2658a5bd05e98/pydantic_core-2.46.4-pp311-pypy311_pp73-musllinux_1_1_armv7l.whl", hash = "sha256:d396ec2b979760aaf3218e76c24e65bd0aca24983298653b3a9d7a45f9e47b30", size = 2310000, upload-time = "2026-05-06T13:37:56.694Z" },

+    { url = "https://files.pythonhosted.org/packages/4f/c3/66883a5cec183e7fba4d024b4cbbe61851a63750ef606b0afecc46d1f2bf/pydantic_core-2.46.4-pp311-pypy311_pp73-musllinux_1_1_x86_64.whl", hash = "sha256:86e1a4418c6cd97d60c95c71164158eaf7324fae7b0923264016baa993eba6fc", size = 2361286, upload-time = "2026-05-06T13:40:05.667Z" },

+    { url = "https://files.pythonhosted.org/packages/4b/2d/69abac8f838090bbecd5df894befb2c2619e7996a98ddb949db9f3b93225/pydantic_core-2.46.4-pp311-pypy311_pp73-win_amd64.whl", hash = "sha256:d51026d73fcfd93610abc7b27789c26b313920fcfb20e27462d74a7f8b06e983", size = 2193071, upload-time = "2026-05-06T13:38:08.682Z" },

+]

+

+[[package]]

+name = "pygments"

+version = "2.20.0"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/c3/b2/bc9c9196916376152d655522fdcebac55e66de6603a76a02bca1b6414f6c/pygments-2.20.0.tar.gz", hash = "sha256:6757cd03768053ff99f3039c1a36d6c0aa0b263438fcab17520b30a303a82b5f", size = 4955991, upload-time = "2026-03-29T13:29:33.898Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/f4/7e/a72dd26f3b0f4f2bf1dd8923c85f7ceb43172af56d63c7383eb62b332364/pygments-2.20.0-py3-none-any.whl", hash = "sha256:81a9e26dd42fd28a23a2d169d86d7ac03b46e2f8b59ed4698fb4785f946d0176", size = 1231151, upload-time = "2026-03-29T13:29:30.038Z" },

+]

+

+[[package]]

+name = "pyparsing"

+version = "3.3.2"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/f3/91/9c6ee907786a473bf81c5f53cf703ba0957b23ab84c264080fb5a450416f/pyparsing-3.3.2.tar.gz", hash = "sha256:c777f4d763f140633dcb6d8a3eda953bf7a214dc4eff598413c070bcdc117cbc", size = 6851574, upload-time = "2026-01-21T03:57:59.36Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/10/bd/c038d7cc38edc1aa5bf91ab8068b63d4308c66c4c8bb3cbba7dfbc049f9c/pyparsing-3.3.2-py3-none-any.whl", hash = "sha256:850ba148bd908d7e2411587e247a1e4f0327839c40e2e5e6d05a007ecc69911d", size = 122781, upload-time = "2026-01-21T03:57:55.912Z" },

+]

+

+[[package]]

+name = "pyproj"

+version = "3.7.2"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "certifi" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/04/90/67bd7260b4ea9b8b20b4f58afef6c223ecb3abf368eb4ec5bc2cdef81b49/pyproj-3.7.2.tar.gz", hash = "sha256:39a0cf1ecc7e282d1d30f36594ebd55c9fae1fda8a2622cee5d100430628f88c", size = 226279, upload-time = "2025-08-14T12:05:42.18Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/a6/bd/f205552cd1713b08f93b09e39a3ec99edef0b3ebbbca67b486fdf1abe2de/pyproj-3.7.2-cp311-cp311-macosx_13_0_x86_64.whl", hash = "sha256:2514d61f24c4e0bb9913e2c51487ecdaeca5f8748d8313c933693416ca41d4d5", size = 6227022, upload-time = "2025-08-14T12:03:51.474Z" },

+    { url = "https://files.pythonhosted.org/packages/75/4c/9a937e659b8b418ab573c6d340d27e68716928953273e0837e7922fcac34/pyproj-3.7.2-cp311-cp311-macosx_14_0_arm64.whl", hash = "sha256:8693ca3892d82e70de077701ee76dd13d7bca4ae1c9d1e739d72004df015923a", size = 4625810, upload-time = "2025-08-14T12:03:53.808Z" },

+    { url = "https://files.pythonhosted.org/packages/c0/7d/a9f41e814dc4d1dc54e95b2ccaf0b3ebe3eb18b1740df05fe334724c3d89/pyproj-3.7.2-cp311-cp311-manylinux_2_28_aarch64.whl", hash = "sha256:5e26484d80fea56273ed1555abaea161e9661d81a6c07815d54b8e883d4ceb25", size = 9638694, upload-time = "2025-08-14T12:03:55.669Z" },

+    { url = "https://files.pythonhosted.org/packages/ad/ab/9bdb4a6216b712a1f9aab1c0fcbee5d3726f34a366f29c3e8c08a78d6b70/pyproj-3.7.2-cp311-cp311-manylinux_2_28_x86_64.whl", hash = "sha256:281cb92847814e8018010c48b4069ff858a30236638631c1a91dd7bfa68f8a8a", size = 9493977, upload-time = "2025-08-14T12:03:57.937Z" },

+    { url = "https://files.pythonhosted.org/packages/c9/db/2db75b1b6190f1137b1c4e8ef6a22e1c338e46320f6329bfac819143e063/pyproj-3.7.2-cp311-cp311-musllinux_1_2_aarch64.whl", hash = "sha256:9c8577f0b7bb09118ec2e57e3babdc977127dd66326d6c5d755c76b063e6d9dc", size = 10841151, upload-time = "2025-08-14T12:04:00.271Z" },

+    { url = "https://files.pythonhosted.org/packages/89/f7/989643394ba23a286e9b7b3f09981496172f9e0d4512457ffea7dc47ffc7/pyproj-3.7.2-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:a23f59904fac3a5e7364b3aa44d288234af267ca041adb2c2b14a903cd5d3ac5", size = 10751585, upload-time = "2025-08-14T12:04:02.228Z" },

+    { url = "https://files.pythonhosted.org/packages/53/6d/ad928fe975a6c14a093c92e6a319ca18f479f3336bb353a740bdba335681/pyproj-3.7.2-cp311-cp311-win32.whl", hash = "sha256:f2af4ed34b2cf3e031a2d85b067a3ecbd38df073c567e04b52fa7a0202afde8a", size = 5908533, upload-time = "2025-08-14T12:04:04.821Z" },

+    { url = "https://files.pythonhosted.org/packages/79/e0/b95584605cec9ed50b7ebaf7975d1c4ddeec5a86b7a20554ed8b60042bd7/pyproj-3.7.2-cp311-cp311-win_amd64.whl", hash = "sha256:0b7cb633565129677b2a183c4d807c727d1c736fcb0568a12299383056e67433", size = 6320742, upload-time = "2025-08-14T12:04:06.357Z" },

+    { url = "https://files.pythonhosted.org/packages/b7/4d/536e8f93bca808175c2d0a5ac9fdf69b960d8ab6b14f25030dccb07464d7/pyproj-3.7.2-cp311-cp311-win_arm64.whl", hash = "sha256:38b08d85e3a38e455625b80e9eb9f78027c8e2649a21dec4df1f9c3525460c71", size = 6245772, upload-time = "2025-08-14T12:04:08.365Z" },

+]

+

+[[package]]

+name = "pyside6"

+version = "6.11.1"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "pyside6-addons" },

+    { name = "pyside6-essentials" },

+    { name = "shiboken6" },

+]

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/da/a6/27ba5947ed48918f7b74b7c43a1e280aac069e36f25adeb4c9adfac835c4/pyside6-6.11.1-cp310-abi3-macosx_13_0_universal2.whl", hash = "sha256:537682c3b7530817203e667c1f5a2f00486b37bf52c52eeab438544c7a0917f6", size = 571921, upload-time = "2026-05-13T09:47:36.402Z" },

+    { url = "https://files.pythonhosted.org/packages/d8/de/af89d71410c83b10654d86ff9aff2a4f87c30163658f1cc145242e222526/pyside6-6.11.1-cp310-abi3-manylinux_2_34_x86_64.whl", hash = "sha256:b1fc521ba2bb5109425ab8add06bddbdd524abcad06cfa012cc39a22a189feb2", size = 572102, upload-time = "2026-05-13T09:47:38.249Z" },

+    { url = "https://files.pythonhosted.org/packages/b6/0e/d583bd3f7bf5046a4497b36f3902cfb64aa29554489a5a25c18e6b4ac0ac/pyside6-6.11.1-cp310-abi3-manylinux_2_39_aarch64.whl", hash = "sha256:75f0005c3eb95c07cfb65522ec50d0815ac007a96482c21dc3cb4b4c04895d84", size = 572098, upload-time = "2026-05-13T09:47:39.44Z" },

+    { url = "https://files.pythonhosted.org/packages/57/f2/d9d8ce1373dabb37e5919f63cd18446556079631d3f2eea3ada03c29f6b8/pyside6-6.11.1-cp310-abi3-win_amd64.whl", hash = "sha256:0968877ab1fb4ef3587a284da6fe05e8647ada56a6a3750b6395188e01f4aba6", size = 578377, upload-time = "2026-05-13T09:47:40.76Z" },

+    { url = "https://files.pythonhosted.org/packages/96/02/a6057d8bd2bdb1940820fff2d627fdf4013148c9c57adf69fa40d3452ac3/pyside6-6.11.1-cp310-abi3-win_arm64.whl", hash = "sha256:acee467cb5f256cc47ebb9d815a054c1d8416da380c191b247a76d164aa3f805", size = 561765, upload-time = "2026-05-13T09:47:41.9Z" },

+]

+

+[[package]]

+name = "pyside6-addons"

+version = "6.11.1"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "pyside6-essentials" },

+    { name = "shiboken6" },

+]

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/3f/6b/8bc94aff48b63f788f2d84e5467c12362d68906ba742c0942f46cb04c879/pyside6_addons-6.11.1-cp310-abi3-macosx_13_0_universal2.whl", hash = "sha256:54733c77f789bef5f03c6aff4ad3bec8b2eff021f0cfcbc53d5e6c250ded24f9", size = 331714589, upload-time = "2026-05-13T09:39:12.36Z" },

+    { url = "https://files.pythonhosted.org/packages/dd/62/fb1428a523b2a4541e232aab50d9e789e6b4526f37fd9593452a7ea5b6b3/pyside6_addons-6.11.1-cp310-abi3-manylinux_2_34_x86_64.whl", hash = "sha256:8e6c65fbd73a512d6f72cda8d8277444a85a34dc99dd1dae9c21d35b8671bb1f", size = 175063224, upload-time = "2026-05-13T09:39:34.185Z" },

+    { url = "https://files.pythonhosted.org/packages/ee/9b/2ccd52f66db55c06de65d0501170a1935d04d64d0a230c0d892284a02ce3/pyside6_addons-6.11.1-cp310-abi3-manylinux_2_39_aarch64.whl", hash = "sha256:bf1c6c4e954e5eba3d2a7c661ad4b9689e8f09c7f4a16bdf29713371d11af993", size = 170553429, upload-time = "2026-05-13T09:39:54.424Z" },

+    { url = "https://files.pythonhosted.org/packages/9a/bd/8adc4d350b3b363f3dfc8fccdcf5bfed25f7e36c2fff30c64e106f4f1572/pyside6_addons-6.11.1-cp310-abi3-win_amd64.whl", hash = "sha256:0d13c4dfd671b050a48e4f8d8ddc724b7248f9c0437e7fc47fdf316278572923", size = 168816308, upload-time = "2026-05-13T09:40:13.541Z" },

+    { url = "https://files.pythonhosted.org/packages/65/b7/9a840d97f0f0f04e372a87e205dd30ee285b4e3b021b188459a917c9dc76/pyside6_addons-6.11.1-cp310-abi3-win_arm64.whl", hash = "sha256:3494f480dee92f415be2f2d989c0b3f4755ac332b28045cbf4ba0f5c5a22ba37", size = 35759347, upload-time = "2026-05-13T09:40:21.199Z" },

+]

+

+[[package]]

+name = "pyside6-essentials"

+version = "6.11.1"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "shiboken6" },

+]

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/b3/da/10d9197e7370eb4fed8df5fc547b7548dec88e5c5949e2d450db4ae96feb/pyside6_essentials-6.11.1-cp310-abi3-macosx_13_0_universal2.whl", hash = "sha256:228de53c2bc26b07e5021fbe3614fc44ca08e4dab9999af08c2b389d2c239957", size = 110352945, upload-time = "2026-05-13T09:43:08.006Z" },

+    { url = "https://files.pythonhosted.org/packages/5c/49/0e1237c4400bec7e335d2c4eeb49bc40d9fd88a9ac44ca9083ce1abdc308/pyside6_essentials-6.11.1-cp310-abi3-manylinux_2_34_x86_64.whl", hash = "sha256:e3ef7027b41e4e55fadb56e3b3257dc8ee92154b639fe67fc4c8e05e9d976c60", size = 79908535, upload-time = "2026-05-13T09:43:24.836Z" },

+    { url = "https://files.pythonhosted.org/packages/4c/c5/da4c5f23c6540ac5211a1f60177c8dee84b1bf40f2719479587ab8c60731/pyside6_essentials-6.11.1-cp310-abi3-manylinux_2_39_aarch64.whl", hash = "sha256:a039b6da68a3a4b9d243217b2b98d475eed3f617159ef6be925badab53c11b0d", size = 78960051, upload-time = "2026-05-13T09:43:35.423Z" },

+    { url = "https://files.pythonhosted.org/packages/64/0e/b663ecc96ca57b5c91b83b6615d6b174380b0faf30338125c26e053d6aa7/pyside6_essentials-6.11.1-cp310-abi3-win_amd64.whl", hash = "sha256:63311bd48e32c584599ab04b9ef7c324082374cd2c9fa533f978fb893bb47e40", size = 77549267, upload-time = "2026-05-13T09:43:44.92Z" },

+    { url = "https://files.pythonhosted.org/packages/f1/12/eb6723faf5cb7fa581145da1c15f40d641b96e080f0491af2f1859fdeedb/pyside6_essentials-6.11.1-cp310-abi3-win_arm64.whl", hash = "sha256:11253ea52aabecefe9febddbbe78b43a824129e3af1cec98431028fba7fa954f", size = 57964512, upload-time = "2026-05-13T09:43:52.968Z" },

+]

+

+[[package]]

+name = "pytest"

+version = "9.0.3"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "colorama", marker = "sys_platform == 'win32'" },

+    { name = "iniconfig" },

+    { name = "packaging" },

+    { name = "pluggy" },

+    { name = "pygments" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/7d/0d/549bd94f1a0a402dc8cf64563a117c0f3765662e2e668477624baeec44d5/pytest-9.0.3.tar.gz", hash = "sha256:b86ada508af81d19edeb213c681b1d48246c1a91d304c6c81a427674c17eb91c", size = 1572165, upload-time = "2026-04-07T17:16:18.027Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/d4/24/a372aaf5c9b7208e7112038812994107bc65a84cd00e0354a88c2c77a617/pytest-9.0.3-py3-none-any.whl", hash = "sha256:2c5efc453d45394fdd706ade797c0a81091eccd1d6e4bccfcd476e2b8e0ab5d9", size = 375249, upload-time = "2026-04-07T17:16:16.13Z" },

+]

+

+[[package]]

+name = "python-pptx"

+version = "1.0.2"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "lxml" },

+    { name = "pillow" },

+    { name = "typing-extensions" },

+    { name = "xlsxwriter" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/52/a9/0c0db8d37b2b8a645666f7fd8accea4c6224e013c42b1d5c17c93590cd06/python_pptx-1.0.2.tar.gz", hash = "sha256:479a8af0eaf0f0d76b6f00b0887732874ad2e3188230315290cd1f9dd9cc7095", size = 10109297, upload-time = "2024-08-07T17:33:37.772Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/d9/4f/00be2196329ebbff56ce564aa94efb0fbc828d00de250b1980de1a34ab49/python_pptx-1.0.2-py3-none-any.whl", hash = "sha256:160838e0b8565a8b1f67947675886e9fea18aa5e795db7ae531606d68e785cba", size = 472788, upload-time = "2024-08-07T17:33:28.192Z" },

+]

+

+[[package]]

+name = "rasterio"

+version = "1.4.4"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "affine" },

+    { name = "attrs" },

+    { name = "certifi" },

+    { name = "click" },

+    { name = "click-plugins" },

+    { name = "cligj" },

+    { name = "numpy" },

+    { name = "pyparsing" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/ec/fa/fce8dc9f09e5bc6520b6fc1b4ecfa510af9ca06eb42ad7bdff9c9b8989d0/rasterio-1.4.4.tar.gz", hash = "sha256:c95424e2c7f009b8f7df1095d645c52895cd332c0c2e1b4c2e073ea28b930320", size = 445004, upload-time = "2025-12-12T18:01:08.971Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/c6/0d/d3859e49ab94464de2623fec82c6798d8d7c8bea2473cd2696fc5e09f717/rasterio-1.4.4-cp311-cp311-macosx_14_0_arm64.whl", hash = "sha256:b8eea428b5f0c78a963f6003a19b60777df83a0aba8c28231d65431e32ac160e", size = 21144125, upload-time = "2025-12-12T17:58:59.511Z" },

+    { url = "https://files.pythonhosted.org/packages/aa/3c/97ba4b146309cdc0e36f289b02ac69465b026a21afc828e4e4e1dc39466a/rasterio-1.4.4-cp311-cp311-macosx_15_0_x86_64.whl", hash = "sha256:1cc0ea5aa0d22f5f349aa221674481de689b7b3a99607ce6bb58a29e5be54d17", size = 25746406, upload-time = "2025-12-12T17:59:02.902Z" },

+    { url = "https://files.pythonhosted.org/packages/ce/33/75f81bd837ac2336b24456fdb249597a4b9af2a212b7151f64d09022be36/rasterio-1.4.4-cp311-cp311-manylinux_2_28_aarch64.whl", hash = "sha256:7eb25b23666b29dadfc49a59206cead62c99190584b61771bba0e95f7da06801", size = 34587242, upload-time = "2025-12-12T17:59:05.848Z" },

+    { url = "https://files.pythonhosted.org/packages/f9/77/3869a426f6e752dde13f3868cdf16253ca0214f92107db79c1583c9aa07b/rasterio-1.4.4-cp311-cp311-manylinux_2_28_x86_64.whl", hash = "sha256:e24b7b8c2df801dde2a1dffb44c58902bd76b5cab740dc11de4ff9963992a71a", size = 35881871, upload-time = "2025-12-12T17:59:09.779Z" },

+    { url = "https://files.pythonhosted.org/packages/66/d0/3818859ddbd3750d0ef5a6580a3272e81764286d943c689dd41e49b8b786/rasterio-1.4.4-cp311-cp311-win_amd64.whl", hash = "sha256:0718630f607be2f5742d8e4b34b434746fd788a192d77eefc9bb924399fea802", size = 25716477, upload-time = "2025-12-12T17:59:13.519Z" },

+    { url = "https://files.pythonhosted.org/packages/4b/02/039eb4970c93aaef4c9eb1ee159abad18e6e7f932c2eed575c95f78d94f6/rasterio-1.4.4-cp311-cp311-win_arm64.whl", hash = "sha256:0308ff4762ae9eb40a991f12d758626b59af4376b13675480391dd7295d17bbf", size = 24075993, upload-time = "2025-12-12T17:59:16.407Z" },

+]

+

+[[package]]

+name = "ruff"

+version = "0.15.14"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/dc/8a/8bce2894573e9dae6ff4d77fe34ad727d79b9e6238ad288c5638990d90f6/ruff-0.15.14.tar.gz", hash = "sha256:48e866b165be4a9bdbf310f7d3c9a07edef2fe8cd63ffeb4e00bb590506ebf9f", size = 4700910, upload-time = "2026-05-21T14:34:55.177Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/b9/c8/74a92c6ff9fcfb4f1f947126d3ebee8389276e161ecc85de5bda7cda51bd/ruff-0.15.14-py3-none-linux_armv6l.whl", hash = "sha256:8dd2db9416e487c8d4b01fa7056bb02c4d05969d4f8d17a08c229c2f4ff3c108", size = 10739177, upload-time = "2026-05-21T14:34:37.332Z" },

+    { url = "https://files.pythonhosted.org/packages/45/91/254a35c20acc38a7223c9d2d594af12e794432464f2cdeb52af1dc4a892d/ruff-0.15.14-py3-none-macosx_10_12_x86_64.whl", hash = "sha256:be4ff55af755bd71a00ab3dc6bd7ffc467bd76e0df6881e286c2e3d23e8fb43b", size = 11144969, upload-time = "2026-05-21T14:34:43.978Z" },

+    { url = "https://files.pythonhosted.org/packages/56/9e/d13e40f83b8d0a94430e6778ce1d94a43b38cf2efe63278bdd2b4c65abbf/ruff-0.15.14-py3-none-macosx_11_0_arm64.whl", hash = "sha256:48d5909d7d06276ce7dde6d32bfa4b0d4cb2651145cd8ee4b440722cbc77832f", size = 10478207, upload-time = "2026-05-21T14:34:48.378Z" },

+    { url = "https://files.pythonhosted.org/packages/8d/f1/b15a7839fa4f332f8acec78e20564f26bb2d866e3d21710b877fd0263000/ruff-0.15.14-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:ca8cbfa94c4f90984a67561978602746d4cd27103568f745fa90eee3f0d4107d", size = 10818459, upload-time = "2026-05-21T14:34:22.318Z" },

+    { url = "https://files.pythonhosted.org/packages/45/33/53d651177f84f94b400a0e27f8824eeada3dddc9d5ee8aeb048f4352a520/ruff-0.15.14-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:9a6bbc0333f1ab053423bcbf6226477d266ca7cec7738c4c8e3f55647803f3c4", size = 10541800, upload-time = "2026-05-21T14:34:20.209Z" },

+    { url = "https://files.pythonhosted.org/packages/b8/a6/868f87e0bf9786ed24b5d0d0ad8676b8a94fd1912f42cddf9cfc7857818a/ruff-0.15.14-py3-none-manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:8a24a4f7605d7003a6674d4387651effd939dead3fddd0f36561eb77a9a2e542", size = 11342149, upload-time = "2026-05-21T14:34:46.365Z" },

+    { url = "https://files.pythonhosted.org/packages/a7/8b/38cd5c19faffdcc05a408d2b78edccc69492ab9720eadb49ea15ef80d768/ruff-0.15.14-py3-none-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:049b5326e53ed80978f2fc041a280603f69dd6b0c95464342a2bb4572d9d9e2f", size = 12212563, upload-time = "2026-05-21T14:34:28.579Z" },

+    { url = "https://files.pythonhosted.org/packages/3e/4d/a3c5b874a556d5731e3e657aaf04311bb76f0a5c3ec220ed43051be6b64b/ruff-0.15.14-py3-none-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:d4ed42e6696c8dfa5f06728e6441993901f548eb92d73bc472cb5a38d1395fbf", size = 11493299, upload-time = "2026-05-21T14:34:41.836Z" },

+    { url = "https://files.pythonhosted.org/packages/1e/c0/56472c251d09858a53e51efbd485b09e1995d8731668b76d52e5dd6ee0f1/ruff-0.15.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:715c543cf450c4888251f91c52f1942a800541d9bddd7ac060aa4e6b77ae7cba", size = 11455931, upload-time = "2026-05-21T14:34:57.276Z" },

+    { url = "https://files.pythonhosted.org/packages/2c/4a/e2e7b4d8dbf233d4eace59c75bc3435fa6d8bd3bae82d351d4e4300c0fd1/ruff-0.15.14-py3-none-manylinux_2_31_riscv64.whl", hash = "sha256:72ebab6013ec887d439d8b7593737a0a4ffb06d45d209d4e4bf2e92813082d3f", size = 11400794, upload-time = "2026-05-21T14:34:39.773Z" },

+    { url = "https://files.pythonhosted.org/packages/97/c7/83c0539fe34c3e09136204d1e75d6052492364e0b3cb05e9465423f567d7/ruff-0.15.14-py3-none-musllinux_1_2_aarch64.whl", hash = "sha256:49072d36abdbe97a8dd7f480afe9c675699c0c495d4c84076e2c1203c4550581", size = 10804759, upload-time = "2026-05-21T14:34:31.045Z" },

+    { url = "https://files.pythonhosted.org/packages/86/a6/18f2bfc095a2ab4a78745644e428205532ce6653a5d0fa8501572891534d/ruff-0.15.14-py3-none-musllinux_1_2_armv7l.whl", hash = "sha256:958522aee105068640c2c2ceae08f413ae44d922f52a1374ac13d6a96032fc93", size = 10539517, upload-time = "2026-05-21T14:34:53.064Z" },

+    { url = "https://files.pythonhosted.org/packages/54/3a/5a8b3b69c654d4e4bf1d246ac5b49cbcdac6eaab6905925f8915f31e3b80/ruff-0.15.14-py3-none-musllinux_1_2_i686.whl", hash = "sha256:f3707da619a143a2e8830e2abab8224478d69ace2d28cb6c20543ae97c36bf61", size = 11065169, upload-time = "2026-05-21T14:34:24.484Z" },

+    { url = "https://files.pythonhosted.org/packages/ed/c5/8864e4e7925b836ea354b31d57641ec03830564e281a8b6f061f8c3e0ec1/ruff-0.15.14-py3-none-musllinux_1_2_x86_64.whl", hash = "sha256:bb01d645694e3ec0102105d07ef2d53703970407d59c04e59d3ba0b7a1d53553", size = 11560214, upload-time = "2026-05-21T14:34:50.975Z" },

+    { url = "https://files.pythonhosted.org/packages/36/38/012bf76752e1f89ed50b77b99532d90f3a3e287bc7918e1fc0948ac866ac/ruff-0.15.14-py3-none-win32.whl", hash = "sha256:6d0c1ad2a0ab718d39b6d8fd2217981ce4d625cd96a720095f798fb47d8b13e6", size = 10805548, upload-time = "2026-05-21T14:34:33.453Z" },

+    { url = "https://files.pythonhosted.org/packages/d1/b7/4ea2c170f10ad760fff2a5250beb18897719dc8b52b53a24cddbb9dd3f19/ruff-0.15.14-py3-none-win_amd64.whl", hash = "sha256:802342981e056db3851a7836e5b070f8f15f67d4a685ae2a6160939d364b2902", size = 11939523, upload-time = "2026-05-21T14:34:18.077Z" },

+    { url = "https://files.pythonhosted.org/packages/62/d5/bc97ff895ec35cf3925d4bd60f3b39d822f377a446906ec9bcc87405e59b/ruff-0.15.14-py3-none-win_arm64.whl", hash = "sha256:ff47b90a9ef6a40c9e2f3b479c1fb78531adf055b94c1eba0a7ba04b31951826", size = 11208607, upload-time = "2026-05-21T14:34:26.525Z" },

+]

+

+[[package]]

+name = "shapely"

+version = "2.1.2"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "numpy" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/4d/bc/0989043118a27cccb4e906a46b7565ce36ca7b57f5a18b78f4f1b0f72d9d/shapely-2.1.2.tar.gz", hash = "sha256:2ed4ecb28320a433db18a5bf029986aa8afcfd740745e78847e330d5d94922a9", size = 315489, upload-time = "2025-09-24T13:51:41.432Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/8f/8d/1ff672dea9ec6a7b5d422eb6d095ed886e2e523733329f75fdcb14ee1149/shapely-2.1.2-cp311-cp311-macosx_10_9_x86_64.whl", hash = "sha256:91121757b0a36c9aac3427a651a7e6567110a4a67c97edf04f8d55d4765f6618", size = 1820038, upload-time = "2025-09-24T13:50:15.628Z" },

+    { url = "https://files.pythonhosted.org/packages/4f/ce/28fab8c772ce5db23a0d86bf0adaee0c4c79d5ad1db766055fa3dab442e2/shapely-2.1.2-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:16a9c722ba774cf50b5d4541242b4cce05aafd44a015290c82ba8a16931ff63d", size = 1626039, upload-time = "2025-09-24T13:50:16.881Z" },

+    { url = "https://files.pythonhosted.org/packages/70/8b/868b7e3f4982f5006e9395c1e12343c66a8155c0374fdc07c0e6a1ab547d/shapely-2.1.2-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:cc4f7397459b12c0b196c9efe1f9d7e92463cbba142632b4cc6d8bbbbd3e2b09", size = 3001519, upload-time = "2025-09-24T13:50:18.606Z" },

+    { url = "https://files.pythonhosted.org/packages/13/02/58b0b8d9c17c93ab6340edd8b7308c0c5a5b81f94ce65705819b7416dba5/shapely-2.1.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:136ab87b17e733e22f0961504d05e77e7be8c9b5a8184f685b4a91a84efe3c26", size = 3110842, upload-time = "2025-09-24T13:50:21.77Z" },

+    { url = "https://files.pythonhosted.org/packages/af/61/8e389c97994d5f331dcffb25e2fa761aeedfb52b3ad9bcdd7b8671f4810a/shapely-2.1.2-cp311-cp311-musllinux_1_2_aarch64.whl", hash = "sha256:16c5d0fc45d3aa0a69074979f4f1928ca2734fb2e0dde8af9611e134e46774e7", size = 4021316, upload-time = "2025-09-24T13:50:23.626Z" },

+    { url = "https://files.pythonhosted.org/packages/d3/d4/9b2a9fe6039f9e42ccf2cb3e84f219fd8364b0c3b8e7bbc857b5fbe9c14c/shapely-2.1.2-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:6ddc759f72b5b2b0f54a7e7cde44acef680a55019eb52ac63a7af2cf17cb9cd2", size = 4178586, upload-time = "2025-09-24T13:50:25.443Z" },

+    { url = "https://files.pythonhosted.org/packages/16/f6/9840f6963ed4decf76b08fd6d7fed14f8779fb7a62cb45c5617fa8ac6eab/shapely-2.1.2-cp311-cp311-win32.whl", hash = "sha256:2fa78b49485391224755a856ed3b3bd91c8455f6121fee0db0e71cefb07d0ef6", size = 1543961, upload-time = "2025-09-24T13:50:26.968Z" },

+    { url = "https://files.pythonhosted.org/packages/38/1e/3f8ea46353c2a33c1669eb7327f9665103aa3a8dfe7f2e4ef714c210b2c2/shapely-2.1.2-cp311-cp311-win_amd64.whl", hash = "sha256:c64d5c97b2f47e3cd9b712eaced3b061f2b71234b3fc263e0fcf7d889c6559dc", size = 1722856, upload-time = "2025-09-24T13:50:28.497Z" },

+]

+

+[[package]]

+name = "shiboken6"

+version = "6.11.1"

+source = { registry = "https://pypi.org/simple" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/17/f3/f2b63df0251e7cd3172ea28e32ede52739de9566bcefcd0178681538ac81/shiboken6-6.11.1-cp310-abi3-macosx_13_0_universal2.whl", hash = "sha256:1a16867f103ef1c662a5f09dfed03273a9f81688b174555162c58e83650a3f02", size = 476874, upload-time = "2026-05-13T09:47:01.091Z" },

+    { url = "https://files.pythonhosted.org/packages/c7/9b/e0355d8897b5c150770f1d95718aad17d432fcc9c035c04f3f58427d4693/shiboken6-6.11.1-cp310-abi3-manylinux_2_34_x86_64.whl", hash = "sha256:9a8bccfafc8805254cabcfa1edfaf55cd52889f4998c91ad0d9a4433fb1bcdbe", size = 272222, upload-time = "2026-05-13T09:47:02.653Z" },

+    { url = "https://files.pythonhosted.org/packages/57/d5/dd4f1defed400be03340f2ede34b61f846776650b4e7ed9ebaf4c71979a2/shiboken6-6.11.1-cp310-abi3-manylinux_2_39_aarch64.whl", hash = "sha256:1bd2f4314414df2d122d9f646e03b731bc6d6b5f77a5f53f99a4fe4e97d84e6f", size = 270350, upload-time = "2026-05-13T09:47:04.02Z" },

+    { url = "https://files.pythonhosted.org/packages/52/b5/3f6fb2ee65b534193fb4ef713dd619dc31dadff5d12c16979a7699ad58be/shiboken6-6.11.1-cp310-abi3-win_amd64.whl", hash = "sha256:c2c6863aa80ec18c0f82cea3417837b279cdc60024ac17123461dc9042577df7", size = 1223647, upload-time = "2026-05-13T09:47:05.924Z" },

+    { url = "https://files.pythonhosted.org/packages/98/d1/f15ca0e1666faae02c945f48e745ea35f8fcd8243b176109b4e2c4251f47/shiboken6-6.11.1-cp310-abi3-win_arm64.whl", hash = "sha256:7c8d9af17db4495d4fa5b1c393f218311c4855546b9dfa6a0bd21bcd66b55e9d", size = 1784170, upload-time = "2026-05-13T09:47:07.617Z" },

+]

+

+[[package]]

+name = "thucthengay"

+version = "0.1.0"

+source = { editable = "." }

+dependencies = [

+    { name = "numpy" },

+    { name = "pillow" },

+    { name = "pydantic" },

+    { name = "pyproj" },

+    { name = "pyside6" },

+    { name = "python-pptx" },

+    { name = "rasterio" },

+    { name = "shapely" },

+]

+

+[package.dev-dependencies]

+dev = [

+    { name = "pytest" },

+    { name = "ruff" },

+]

+

+[package.metadata]

+requires-dist = [

+    { name = "numpy", specifier = ">=1.26" },

+    { name = "pillow", specifier = ">=10.0" },

+    { name = "pydantic", specifier = ">=2.7" },

+    { name = "pyproj", specifier = ">=3.6" },

+    { name = "pyside6", specifier = ">=6.7" },

+    { name = "python-pptx", specifier = ">=1.0" },

+    { name = "rasterio", specifier = ">=1.3" },

+    { name = "shapely", specifier = ">=2.0" },

+]

+

+[package.metadata.requires-dev]

+dev = [

+    { name = "pytest", specifier = ">=8.0" },

+    { name = "ruff", specifier = ">=0.4" },

+]

+

+[[package]]

+name = "typing-extensions"

+version = "4.15.0"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/72/94/1a15dd82efb362ac84269196e94cf00f187f7ed21c242792a923cdb1c61f/typing_extensions-4.15.0.tar.gz", hash = "sha256:0cea48d173cc12fa28ecabc3b837ea3cf6f38c6d1136f85cbaaf598984861466", size = 109391, upload-time = "2025-08-25T13:49:26.313Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/18/67/36e9267722cc04a6b9f15c7f3441c2363321a3ea07da7ae0c0707beb2a9c/typing_extensions-4.15.0-py3-none-any.whl", hash = "sha256:f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548", size = 44614, upload-time = "2025-08-25T13:49:24.86Z" },

+]

+

+[[package]]

+name = "typing-inspection"

+version = "0.4.2"

+source = { registry = "https://pypi.org/simple" }

+dependencies = [

+    { name = "typing-extensions" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/55/e3/70399cb7dd41c10ac53367ae42139cf4b1ca5f36bb3dc6c9d33acdb43655/typing_inspection-0.4.2.tar.gz", hash = "sha256:ba561c48a67c5958007083d386c3295464928b01faa735ab8547c5692e87f464", size = 75949, upload-time = "2025-10-01T02:14:41.687Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/dc/9b/47798a6c91d8bdb567fe2698fe81e0c6b7cb7ef4d13da4114b41d239f65d/typing_inspection-0.4.2-py3-none-any.whl", hash = "sha256:4ed1cacbdc298c220f1bd249ed5287caa16f34d44ef4e9c3d0cbad5b521545e7", size = 14611, upload-time = "2025-10-01T02:14:40.154Z" },

+]

+

+[[package]]

+name = "xlsxwriter"

+version = "3.2.9"

+source = { registry = "https://pypi.org/simple" }

+sdist = { url = "https://files.pythonhosted.org/packages/46/2c/c06ef49dc36e7954e55b802a8b231770d286a9758b3d936bd1e04ce5ba88/xlsxwriter-3.2.9.tar.gz", hash = "sha256:254b1c37a368c444eac6e2f867405cc9e461b0ed97a3233b2ac1e574efb4140c", size = 215940, upload-time = "2025-09-16T00:16:21.63Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/3a/0c/3662f4a66880196a590b202f0db82d919dd2f89e99a27fadef91c4a33d41/xlsxwriter-3.2.9-py3-none-any.whl", hash = "sha256:9a5db42bc5dff014806c58a20b9eae7322a134abb6fce3c92c181bfb275ec5b3", size = 175315, upload-time = "2025-09-16T00:16:20.108Z" },

+]



--- a/src/thucthengay/__init__.py
+++ b/src/thucthengay/__init__.py
@@ -0,0 +1,3 @@
+"""Application package for 3.ThucTheNgay."""

+

+__version__ = "0.1.0"



--- a/src/thucthengay/__main__.py
+++ b/src/thucthengay/__main__.py
@@ -0,0 +1,5 @@
+"""Module entrypoint for ``python -m thucthengay``."""

+

+from thucthengay.app import main

+

+raise SystemExit(main())



--- a/src/thucthengay/app.py
+++ b/src/thucthengay/app.py
@@ -0,0 +1,12 @@
+"""Minimal command-line entrypoint for the application scaffold."""

+

+from __future__ import annotations

+

+import sys

+

+

+def main(argv: list[str] | None = None) -> int:

+    """Run the placeholder app shell without requiring GUI or project data."""

+    _ = sys.argv[1:] if argv is None else argv

+    print("3.ThucTheNgay scaffold ready.")

+    return 0



--- a/src/thucthengay/models/__init__.py
+++ b/src/thucthengay/models/__init__.py
@@ -0,0 +1 @@
+"""Core domain model package."""



--- a/src/thucthengay/config/__init__.py
+++ b/src/thucthengay/config/__init__.py
@@ -0,0 +1 @@
+"""Configuration loading package."""



--- a/src/thucthengay/workspace/__init__.py
+++ b/src/thucthengay/workspace/__init__.py
@@ -0,0 +1 @@
+"""Workspace management package."""



--- a/src/thucthengay/ingestion/__init__.py
+++ b/src/thucthengay/ingestion/__init__.py
@@ -0,0 +1 @@
+"""Imagery ingestion package."""



--- a/src/thucthengay/gis/__init__.py
+++ b/src/thucthengay/gis/__init__.py
@@ -0,0 +1 @@
+"""GIS processing package."""



--- a/src/thucthengay/render/__init__.py
+++ b/src/thucthengay/render/__init__.py
@@ -0,0 +1 @@
+"""Rendering package."""



--- a/src/thucthengay/validation/__init__.py
+++ b/src/thucthengay/validation/__init__.py
@@ -0,0 +1 @@
+"""Validation package."""



--- a/src/thucthengay/export/__init__.py
+++ b/src/thucthengay/export/__init__.py
@@ -0,0 +1 @@
+"""Export package."""



--- a/src/thucthengay/jobs/__init__.py
+++ b/src/thucthengay/jobs/__init__.py
@@ -0,0 +1 @@
+"""Background job orchestration package."""



--- a/src/thucthengay/editor/__init__.py
+++ b/src/thucthengay/editor/__init__.py
@@ -0,0 +1 @@
+"""Qt editor package."""



--- a/src/thucthengay/editor/modes/__init__.py
+++ b/src/thucthengay/editor/modes/__init__.py
@@ -0,0 +1 @@
+"""Editor mode package."""



--- a/src/thucthengay/editor/models/__init__.py
+++ b/src/thucthengay/editor/models/__init__.py
@@ -0,0 +1 @@
+"""Editor model package."""



--- a/src/thucthengay/editor/widgets/__init__.py
+++ b/src/thucthengay/editor/widgets/__init__.py
@@ -0,0 +1 @@
+"""Editor widget package."""



--- a/src/thucthengay/editor/delegates/__init__.py
+++ b/src/thucthengay/editor/delegates/__init__.py
@@ -0,0 +1 @@
+"""Editor delegate package."""



--- a/src/thucthengay/utils/__init__.py
+++ b/src/thucthengay/utils/__init__.py
@@ -0,0 +1 @@
+"""Shared utility package."""



--- a/tests/unit/test_package_import.py
+++ b/tests/unit/test_package_import.py
@@ -0,0 +1,9 @@
+from __future__ import annotations

+

+import importlib

+

+

+def test_package_imports_without_runtime_side_effects() -> None:

+    package = importlib.import_module("thucthengay")

+

+    assert package.__version__ == "0.1.0"



--- a/tests/unit/test_core_import_boundaries.py
+++ b/tests/unit/test_core_import_boundaries.py
@@ -0,0 +1,82 @@
+from __future__ import annotations

+

+import ast

+from pathlib import Path

+

+PACKAGE_ROOT = "thucthengay"

+CORE_PACKAGES = {

+    "models",

+    "config",

+    "workspace",

+    "ingestion",

+    "gis",

+    "render",

+    "validation",

+    "export",

+    "jobs",

+    "utils",

+}

+

+

+def module_path_for_source(package_root: Path, source: Path) -> str:

+    relative = source.relative_to(package_root).with_suffix("")

+    parts = relative.parts[:-1] if relative.name == "__init__" else relative.parts

+    return ".".join((PACKAGE_ROOT, *parts))

+

+

+def resolve_import_from(module_path: str, node: ast.ImportFrom) -> set[str]:

+    if node.level == 0:

+        return {node.module} if node.module else set()

+

+    package_parts = module_path.split(".")

+    base_parts = package_parts[: max(len(package_parts) - node.level, 0)]

+    if node.module:

+        base_parts.extend(node.module.split("."))

+

+    resolved = ".".join(base_parts)

+    modules = {resolved} if resolved else set()

+    modules.update(f"{resolved}.{alias.name}" for alias in node.names if resolved)

+    return modules

+

+

+def imported_modules(package_root: Path, source: Path) -> set[str]:

+    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))

+    imports: set[str] = set()

+    module_path = module_path_for_source(package_root, source)

+

+    for node in ast.walk(tree):

+        if isinstance(node, ast.Import):

+            imports.update(alias.name for alias in node.names)

+        elif isinstance(node, ast.ImportFrom):

+            imports.update(resolve_import_from(module_path, node))

+

+    return imports

+

+

+def test_relative_imports_are_resolved_to_absolute_module_names() -> None:

+    tree = ast.parse("from ..editor import widgets\nfrom .. import editor\n")

+    import_from_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]

+

+    modules = set()

+    for node in import_from_nodes:

+        modules.update(resolve_import_from("thucthengay.models.service", node))

+

+    assert "thucthengay.editor" in modules

+    assert "thucthengay.editor.widgets" in modules

+

+

+def test_core_packages_do_not_import_qt_or_editor_modules() -> None:

+    package_root = Path(__file__).parents[2] / "src" / "thucthengay"

+    violations: list[str] = []

+

+    for package_name in sorted(CORE_PACKAGES):

+        for source in (package_root / package_name).rglob("*.py"):

+            for module_name in imported_modules(package_root, source):

+                if module_name == "PySide6" or module_name.startswith("PySide6."):

+                    violations.append(f"{source}: imports {module_name}")

+                if module_name == "thucthengay.editor" or module_name.startswith(

+                    "thucthengay.editor."

+                ):

+                    violations.append(f"{source}: imports {module_name}")

+

+    assert violations == []



--- a/tests/integration/.gitkeep
+++ b/tests/integration/.gitkeep
@@ -0,0 +1 @@
+



--- a/tests/fixtures/configs/.gitkeep
+++ b/tests/fixtures/configs/.gitkeep
@@ -0,0 +1 @@
+



--- a/tests/fixtures/geojson/.gitkeep
+++ b/tests/fixtures/geojson/.gitkeep
@@ -0,0 +1 @@
+



--- a/tests/fixtures/geotiff/.gitkeep
+++ b/tests/fixtures/geotiff/.gitkeep
@@ -0,0 +1 @@
+



--- a/tests/fixtures/templates/.gitkeep
+++ b/tests/fixtures/templates/.gitkeep
@@ -0,0 +1 @@
+



--- a/tests/fixtures/workspaces/.gitkeep
+++ b/tests/fixtures/workspaces/.gitkeep
@@ -0,0 +1 @@
+



```
