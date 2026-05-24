# Blind Hunter Prompt - Story 1.1

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
@@ -0,0 +1,24 @@
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

+and shapely are resolved together by conda-forge before running the same `uv run ...` commands.



--- a/pyproject.toml
+++ b/pyproject.toml
@@ -0,0 +1,57 @@
+[project]

+name = "thucthengay"

+version = "0.1.0"

+description = "Desktop workflow for preparing satellite imagery reports."

+readme = "README.md"

+requires-python = ">=3.11"

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
@@ -0,0 +1,935 @@
+version = 1

+revision = 3

+requires-python = ">=3.11"

+resolution-markers = [

+    "python_full_version >= '3.12'",

+    "python_full_version < '3.12'",

+]

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

+    { name = "click", marker = "python_full_version < '3.12'" },

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

+    { url = "https://files.pythonhosted.org/packages/6a/6e/c4add832b6fc1e887125b96f880d7b9b70aae5248718e046b1704bcac4b9/lxml-6.1.1-cp312-cp312-macosx_10_13_universal2.whl", hash = "sha256:104c09bda8d2a562824c0e319d0768ce26a779b7601e0931d33b09b53c392ef7", size = 8570821, upload-time = "2026-05-18T19:17:42.068Z" },

+    { url = "https://files.pythonhosted.org/packages/22/00/ff3009c88e65de8011630acf8ab5a09cb2becd2aaf47fba2f3449f6224e9/lxml-6.1.1-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:25c6997a9a534e016695a0ba06b2f07945de682731ff01065b6d5a4474179da1", size = 4624252, upload-time = "2026-05-18T19:17:47.897Z" },

+    { url = "https://files.pythonhosted.org/packages/42/95/bb63f0fd62e554fe078e1fb3c8fe9083c14ddc7ad7fa178d10e57e071ac7/lxml-6.1.1-cp312-cp312-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:c921ba5c51e4e9f63b8b00267d06566e1f63407408a0496da2d1d0bfc819c7fc", size = 4930746, upload-time = "2026-05-18T19:18:29.637Z" },

+    { url = "https://files.pythonhosted.org/packages/eb/99/0013e8d9b5960f4f041cf0b73e2f80c23eb5205b1f7bfb20203243651359/lxml-6.1.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:54a7f95e4de5fb94e2f9f4b9055c6ba33bf3d628fd77a1d647c5923caa2cdcdc", size = 5093723, upload-time = "2026-05-18T19:18:34.168Z" },

+    { url = "https://files.pythonhosted.org/packages/29/91/317b332636bfc7bddcff828d41b3307f50043f4b237e40849c333d80fa1a/lxml-6.1.1-cp312-cp312-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:96f2ec43df44b1f76249ee0a615334f9b5b060e1c8bd90e706dad2d14d02f383", size = 5005557, upload-time = "2026-05-18T19:18:39.798Z" },

+    { url = "https://files.pythonhosted.org/packages/42/2f/cc9bf06afe70f9c9093ae60855d9759da9db601ec4080f7473319666ffd7/lxml-6.1.1-cp312-cp312-manylinux_2_26_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:70ef8a7e102a1508f8121aae5b0867abd663f72c14f0a9c937e6554cb4587b7b", size = 5631036, upload-time = "2026-05-18T19:18:44.858Z" },

+    { url = "https://files.pythonhosted.org/packages/08/f6/af32e23e563971ffb0fb86be52bc5be5c2c118858ffc119bf6a9039b173d/lxml-6.1.1-cp312-cp312-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:ebe6af670449830d6d9b752c256a983291c766a1365ba5d5460048f9e33a7818", size = 5240367, upload-time = "2026-05-18T19:18:49.217Z" },

+    { url = "https://files.pythonhosted.org/packages/78/83/8555d40948b09ce86f1bd0c68a7ac31d07b1929f92cc1b074006c97ef2d2/lxml-6.1.1-cp312-cp312-manylinux_2_28_i686.whl", hash = "sha256:27acc820660aaffa4f7c087f29120e12980f7779d56d8492d263170111284740", size = 5350171, upload-time = "2026-05-18T19:18:52.779Z" },

+    { url = "https://files.pythonhosted.org/packages/63/75/5d92da93729b7bad783689e6496049fa40927b45bec7bf183c981de3ca70/lxml-6.1.1-cp312-cp312-manylinux_2_31_armv7l.whl", hash = "sha256:1db753c9115ec7100d073b744d17e25e88a8f90f5c39b2f5dd878149af59671f", size = 4694874, upload-time = "2026-05-18T19:18:55.139Z" },

+    { url = "https://files.pythonhosted.org/packages/c5/b5/3aad415a9a25b822e783f15deeb4dffccf5113030f1afa2222dd929313d9/lxml-6.1.1-cp312-cp312-manylinux_2_38_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:c4f469aebd783bb741c2ecb2a681008fd26bfe5c16a9a72ed5467f834e810df2", size = 5244492, upload-time = "2026-05-18T19:19:01.28Z" },

+    { url = "https://files.pythonhosted.org/packages/f1/a1/5fcf7eb9904b80086aa47dcf0027de07b1bb990afad2e6823144c368ae04/lxml-6.1.1-cp312-cp312-musllinux_1_2_aarch64.whl", hash = "sha256:766b010012d59470072c1816b5b6c69f1d243e5db36ea5968e94accf430a4635", size = 5048232, upload-time = "2026-05-18T19:18:12.67Z" },

+    { url = "https://files.pythonhosted.org/packages/77/74/1f601b63c7a69fcdf10fa9b148c81da8442204194f6c55509cc485c786b9/lxml-6.1.1-cp312-cp312-musllinux_1_2_armv7l.whl", hash = "sha256:b8d812c6011c08b8111a15e54dd990b8923692d80adf35488bee34026c35accf", size = 4777023, upload-time = "2026-05-18T19:18:15.928Z" },

+    { url = "https://files.pythonhosted.org/packages/a2/b9/7a78f51aec95b1bf780d78e12705a9f6533284f8693dc5c0e6724fa53d3f/lxml-6.1.1-cp312-cp312-musllinux_1_2_ppc64le.whl", hash = "sha256:fe0306bd29505a9177aac19f1877174b0e7422c222a59f70b2cd41633448c3dc", size = 5645773, upload-time = "2026-05-18T19:18:23.223Z" },

+    { url = "https://files.pythonhosted.org/packages/a5/6e/98a7b7ad54e4e74fa1f20fff776913980619d0ebe5558232d7da6580bdd8/lxml-6.1.1-cp312-cp312-musllinux_1_2_riscv64.whl", hash = "sha256:5ba186ad207446c65d3bb3d3e0412b032b1d9f595e59861e2354798c5703d955", size = 5233088, upload-time = "2026-05-18T19:18:31.433Z" },

+    { url = "https://files.pythonhosted.org/packages/65/d1/bc0ed2427bf609f2ee10da303a6a226f9c8bce94f945dc29a32ce55de6e4/lxml-6.1.1-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:aa366a1e55b8ebfe8ca8ddc3cfe75c8ebade181aeb0f661d0cb05986b647f72a", size = 5260995, upload-time = "2026-05-18T19:18:37.091Z" },

+    { url = "https://files.pythonhosted.org/packages/69/8b/6772e1a4b513fc50a8d931f19edde0e13ae6918510a1e13ff67864f3e5ed/lxml-6.1.1-cp312-cp312-win32.whl", hash = "sha256:126c93f7f56f0eda92f6d8c619edc463a4f23d9252f1c9d0405a76f25fa9f11a", size = 3596382, upload-time = "2026-05-18T19:17:18.37Z" },

+    { url = "https://files.pythonhosted.org/packages/1b/89/45198e9624762af2dfd2cb8782598477ceb29f6e59caab560388ae1f4ec1/lxml-6.1.1-cp312-cp312-win_amd64.whl", hash = "sha256:26e6eda8d38c1fcab1090dd196ee87cbd13788e531937610e2589085de074e77", size = 3997255, upload-time = "2026-05-18T19:17:56.781Z" },

+    { url = "https://files.pythonhosted.org/packages/90/a9/7a54b6834088d9ae528a7b780584ba6a39a9457b0ac330479f20ffbc9449/lxml-6.1.1-cp312-cp312-win_arm64.whl", hash = "sha256:6540377fbd53fe1b629172288c464fb18db11ce1fa7dc15891da10aa9dcc3e7f", size = 3659610, upload-time = "2026-05-19T19:22:50.843Z" },

+    { url = "https://files.pythonhosted.org/packages/a5/eb/7e6f37c5584ccbb2ff267f56fd0339016938c1c8684cfefab9b33ffc2f36/lxml-6.1.1-cp313-cp313-macosx_10_13_universal2.whl", hash = "sha256:68a9198d0fc122d14bb76837de9aa80cf84caed990b5b237f532ed87d3706736", size = 8559780, upload-time = "2026-05-18T19:17:57.661Z" },

+    { url = "https://files.pythonhosted.org/packages/a1/36/587c2521cf23a2cd6c9c22108aa7528f683a1f195ed7ccd23a4b1786ad36/lxml-6.1.1-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:7d47866cb32fb503450b6edc9df355d10dc49836af2e89901bd6ac6b0896d9d9", size = 4618006, upload-time = "2026-05-18T19:18:04.452Z" },

+    { url = "https://files.pythonhosted.org/packages/6e/ca/ab7bfe2bf4c972af5e7878262845ead3a24a929a9b04bc11c7c1ece6c82a/lxml-6.1.1-cp313-cp313-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:eb7c9811bfaa8b1ed5ed319f5d370dfbcaa59d52ea64be2a5a85e18195930354", size = 4924139, upload-time = "2026-05-18T19:19:04.873Z" },

+    { url = "https://files.pythonhosted.org/packages/6b/55/a0c72851dfee5ecc689f949723a73dea457758912542cb955b108eaf0d8f/lxml-6.1.1-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:762ff394d5bd56da0cf034a23dcce4e13923f15321a2adfa2ac00201dc6d3fca", size = 5082329, upload-time = "2026-05-18T19:19:09.728Z" },

+    { url = "https://files.pythonhosted.org/packages/f0/b6/0608f7d61a3b96cc67e5648a3d906e31a5082093e10e7be65b3886289938/lxml-6.1.1-cp313-cp313-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:a088f287f7d8275a33c07f2cac6c50b9319309a0200a39e7e75d80c707723099", size = 4993564, upload-time = "2026-05-18T19:19:13.608Z" },

+    { url = "https://files.pythonhosted.org/packages/4c/66/ae227524b066d29d55bf0b453d93d2d793c40218657d643dcbbca13b8faf/lxml-6.1.1-cp313-cp313-manylinux_2_26_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:e902da4b04e6b52e5893900d4b8ab46068f75f3561f01bf1080957f9fd932ed6", size = 5613467, upload-time = "2026-05-18T19:19:16.228Z" },

+    { url = "https://files.pythonhosted.org/packages/a6/76/dbe4a00b50385e40194231dcfe5a12c059de7cf90e89c83407d2b085b719/lxml-6.1.1-cp313-cp313-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:1d4962d4c66bf830a7e59ed6cfc17d148149898a3aefa8ec6e59763e6e3ed085", size = 5228304, upload-time = "2026-05-18T19:19:19.354Z" },

+    { url = "https://files.pythonhosted.org/packages/1c/01/00b1b8442ed2041793336868ba0b9ea4b13d7da7c085c6404c207a63bf79/lxml-6.1.1-cp313-cp313-manylinux_2_28_i686.whl", hash = "sha256:581d4c8ae690a6609e64862dd6b7c2489635c2d13907fc2b20f2bc200ff1d21e", size = 5341607, upload-time = "2026-05-18T19:19:22.297Z" },

+    { url = "https://files.pythonhosted.org/packages/63/36/1ad29931e9a4638bb707869f01d423a6c815f82152138d1a40dfcfde2b95/lxml-6.1.1-cp313-cp313-manylinux_2_31_armv7l.whl", hash = "sha256:876e1ff5930ed8bf295ec5ef9a8155e9b6b1876bbf1deed8b3a8069311875a8f", size = 4700168, upload-time = "2026-05-18T19:19:25.133Z" },

+    { url = "https://files.pythonhosted.org/packages/3c/d1/a9536cecf9be18a0dc72d32bead283a2332d1ffebd2dd3ac70ce444686e5/lxml-6.1.1-cp313-cp313-manylinux_2_38_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:9eb9b5a968f6e0f6d640092a567e14529ff8cea2e29d00da6f78a79fa49f013c", size = 5232487, upload-time = "2026-05-18T19:19:28.603Z" },

+    { url = "https://files.pythonhosted.org/packages/0e/77/b4fb1e03bf5d130e879214d3100092e386418807fb74dd0adc4b0a48f351/lxml-6.1.1-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:aa49e06d94aba782c6a02eecb7e507969e7e7a41b267f1b359bb35585f295d5b", size = 5044231, upload-time = "2026-05-18T19:18:42.246Z" },

+    { url = "https://files.pythonhosted.org/packages/26/4c/d00daeeb0a5530c4028a9232aa1b93db3ef4ed2158c116ea73c79a9765b3/lxml-6.1.1-cp313-cp313-musllinux_1_2_armv7l.whl", hash = "sha256:70cdfd80589d59e43e18005dd7244e8895e93db8ab6a620b7e23df5445a4e3d2", size = 4769450, upload-time = "2026-05-18T19:18:48.013Z" },

+    { url = "https://files.pythonhosted.org/packages/ed/6a/715a3a8d156ce42f29cf014706f5410c2ff3b02267774110fc23266409fe/lxml-6.1.1-cp313-cp313-musllinux_1_2_ppc64le.whl", hash = "sha256:aad9aa39483ed8ec44d6d2e59e5b98a0d80676ef0d92f44bfc374836111f62f5", size = 5635874, upload-time = "2026-05-18T19:18:51.914Z" },

+    { url = "https://files.pythonhosted.org/packages/45/37/0544bc21dde2a88f3a17b504e6fc79c0e01d25a33c2f6079724e9e72b9c7/lxml-6.1.1-cp313-cp313-musllinux_1_2_riscv64.whl", hash = "sha256:d49514be2f28d895c38cf9d2b72d7b9a07d00314519f456c0b50b53cfcf4c785", size = 5223987, upload-time = "2026-05-18T19:18:59.715Z" },

+    { url = "https://files.pythonhosted.org/packages/4d/f8/f6a5e8185bcb28c2befae3d31f8e3df3b811cb0f47746517a81279fcafe1/lxml-6.1.1-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:47402e62c52ff5988c1e8c6c63177f5708bccf48e366dea4e3dcf1e645e04947", size = 5250276, upload-time = "2026-05-18T19:19:03.834Z" },

+    { url = "https://files.pythonhosted.org/packages/c7/f2/1a2b9f1b7a49d45495369be7ef9ad05b262930f2eab3e3145706fca8083f/lxml-6.1.1-cp313-cp313-win32.whl", hash = "sha256:3483644525531e1d5762b0c44a8e18b6efba321b6dcf8a8952de10b037618bca", size = 3596903, upload-time = "2026-05-18T19:17:29.863Z" },

+    { url = "https://files.pythonhosted.org/packages/e6/99/f4ffb024f238eec2131aaa09f3278fb6129cf892741bf68e1fc1afb8c100/lxml-6.1.1-cp313-cp313-win_amd64.whl", hash = "sha256:a10bd2fd62e8ce916ececb342f348f190724a098c1faa056fdfb2a22ad5e8660", size = 3995869, upload-time = "2026-05-18T19:18:02.596Z" },

+    { url = "https://files.pythonhosted.org/packages/d1/53/70eb8c5c6037f27448f1e3c54ebede9545a801ae63f0a7254afca4fe8e45/lxml-6.1.1-cp313-cp313-win_arm64.whl", hash = "sha256:424aa57aca0897eb922aef34395bd1289b3b6f04e6bae20ea123c0c7e333cffc", size = 3658490, upload-time = "2026-05-19T19:22:53.846Z" },

+    { url = "https://files.pythonhosted.org/packages/13/e2/2e325795566de01d0d7c3bb57d3c370616b2d07b01214e84eec5d3b10963/lxml-6.1.1-cp314-cp314-macosx_10_15_universal2.whl", hash = "sha256:19b7ab10b210b0b3ad7985d9ac4eb66ab09a90b20fe6e2f7ba55d01a234345d0", size = 8577146, upload-time = "2026-05-18T19:18:17.765Z" },

+    { url = "https://files.pythonhosted.org/packages/93/cf/5630b5e4be7d2e6bee8efe83865c925221103cf0221303b104ce134b01e2/lxml-6.1.1-cp314-cp314-macosx_10_15_x86_64.whl", hash = "sha256:c08e5c694306507275f2290073350c4f32e383db15213b2c69e7ff39c1193840", size = 4623866, upload-time = "2026-05-18T19:18:30.669Z" },

+    { url = "https://files.pythonhosted.org/packages/d2/51/3904907c063451cf8d4a5c9fe0cad95fa1f4ec57f4e3884fa0731bd7a305/lxml-6.1.1-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:74a9717fd0d82effef5c2854f0d917231d5324b5a3eb7275c43ac9fa32f97a14", size = 4950022, upload-time = "2026-05-18T19:19:31.958Z" },

+    { url = "https://files.pythonhosted.org/packages/94/cd/9c7611a51c37a2830928405817cc5d56a97f64fab83cc3f628748b135749/lxml-6.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:efe0374196335f93b53269acd811b944f2e6bdc88e8894f214bd636455484909", size = 5086695, upload-time = "2026-05-18T19:19:34.764Z" },

+    { url = "https://files.pythonhosted.org/packages/da/d6/24e3b5906abb0b674ff2ae195bc3ce59708df2bcd17cf17703b2d7dd643a/lxml-6.1.1-cp314-cp314-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:ac931cdc9442c1763b8a8f6cd62c0c938737eafc5be75eff88df55fc73bc0d00", size = 5031642, upload-time = "2026-05-18T19:19:37.771Z" },

+    { url = "https://files.pythonhosted.org/packages/2d/db/6ec54f99019838bff54785c51da07f189eb4676861c5f2730962b0d8d665/lxml-6.1.1-cp314-cp314-manylinux_2_26_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:aee395f5d0927f947758b4ec119fd5fc8ec71f07a1c5c52077b30b04c0fa6955", size = 5647338, upload-time = "2026-05-18T19:19:40.553Z" },

+    { url = "https://files.pythonhosted.org/packages/42/3d/ef4dcfffd22d27a61805d8ed9f7fb888495bc6aa88648fa07c1eaa5586b6/lxml-6.1.1-cp314-cp314-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:9395002973c827b3ed67db77e6ec09f092919a587022174554096a269378fb13", size = 5239528, upload-time = "2026-05-18T19:19:43.657Z" },

+    { url = "https://files.pythonhosted.org/packages/62/bb/37fb3f0dff146bdcfa78eec47879273820b2a0bf350ec236ce14bd0b1c26/lxml-6.1.1-cp314-cp314-manylinux_2_28_i686.whl", hash = "sha256:73bc2086f141224ebddb7fc5c6a36ca58b31b94b561e1dfe8e073e3270fad1e7", size = 5350730, upload-time = "2026-05-18T19:19:46.307Z" },

+    { url = "https://files.pythonhosted.org/packages/90/42/43253f168388df4fae1f38c01df36ddb9bee39e2048167b54cdcbae85ea3/lxml-6.1.1-cp314-cp314-manylinux_2_31_armv7l.whl", hash = "sha256:3779def59032b81e44a5f70096ef6bf2082f8d901937dca354474ba09782e245", size = 4697530, upload-time = "2026-05-18T19:19:49.889Z" },

+    { url = "https://files.pythonhosted.org/packages/eb/a8/c5a8504f81bbdfc8e7094c2c850cdb4ed6777fc4d5ddd9e5ab819f3b0d54/lxml-6.1.1-cp314-cp314-manylinux_2_38_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:86c89b9d55ebf820ad7c90bc533410f0d098054f293351f10603c0c46ff598f5", size = 5250670, upload-time = "2026-05-18T19:19:53.199Z" },

+    { url = "https://files.pythonhosted.org/packages/77/b7/c7e76ab18744d75e21f320ebf9ff9d1ceae2b54dd431ea5a64caf26c9672/lxml-6.1.1-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:19607c6bbff2a44cf3fe8250abccd20942d3462473e0a721d01d379ed017e462", size = 5084485, upload-time = "2026-05-18T19:19:08.422Z" },

+    { url = "https://files.pythonhosted.org/packages/31/31/b35c53f8ef7b7c31cacd23d3638652fff7bcd1deb6eedb709ab43b685908/lxml-6.1.1-cp314-cp314-musllinux_1_2_armv7l.whl", hash = "sha256:c6ed5141a5c7507cf3ee76bd363b0d6f801e3321adc35b5d825a23115faa5465", size = 4737635, upload-time = "2026-05-18T19:19:12.321Z" },

+    { url = "https://files.pythonhosted.org/packages/d9/06/31f23c813a7fe8e0cb1b175e915b08c9bf4e86d225b210feadbdbe519667/lxml-6.1.1-cp314-cp314-musllinux_1_2_ppc64le.whl", hash = "sha256:62aeb7e85b5d60320b9d77eef2e773994e2c0ce10121b277e0a19804e1654a5a", size = 5670681, upload-time = "2026-05-18T19:19:15.001Z" },

+    { url = "https://files.pythonhosted.org/packages/1a/bc/ce619bccc89b1fd9ad8a8e1330ee3f3beff9f2ff95b712d7bbcdd6e22fc3/lxml-6.1.1-cp314-cp314-musllinux_1_2_riscv64.whl", hash = "sha256:b1b963fd8f5caa68e99dfae060d54de1fe9cba899b8718b44a00cdca53c3e590", size = 5238229, upload-time = "2026-05-18T19:19:18.131Z" },

+    { url = "https://files.pythonhosted.org/packages/2f/5d/b329acbbedc0b619ebc2be6cf7ee9ed07e80892c88d4dfd612c33805789a/lxml-6.1.1-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:63876be28efefa04a1df615b46770e82042cce445cfdce55160522f57b231ccb", size = 5264191, upload-time = "2026-05-18T19:19:21.118Z" },

+    { url = "https://files.pythonhosted.org/packages/d6/85/be36fb1425b30db3c3f9df75fe86343ebffb79e6320bd7f588e25bfeac39/lxml-6.1.1-cp314-cp314-win32.whl", hash = "sha256:7f7a92e8583f06b1fd49d01158143b8461cfcd135dcb10ec807270a3051bd603", size = 3657202, upload-time = "2026-05-18T19:17:39.509Z" },

+    { url = "https://files.pythonhosted.org/packages/b8/ce/3cf9a827342269f54d405a6202397de63f07c69cbd6ce7d183a3f0cba1e9/lxml-6.1.1-cp314-cp314-win_amd64.whl", hash = "sha256:b2d444f2e66624d68e9c6b211e28a76e22fff5fcabcfff4deac18b529b7d4137", size = 4064497, upload-time = "2026-05-18T19:18:14.662Z" },

+    { url = "https://files.pythonhosted.org/packages/d9/3e/1a957bde8f0760039e627f94699f82caa782c9d838d86c3d28245ee67212/lxml-6.1.1-cp314-cp314-win_arm64.whl", hash = "sha256:3fd9728a2735fda14f4e8235830c86b539e9661e849665bf926d3f867943b4bf", size = 3741991, upload-time = "2026-05-19T19:22:59.111Z" },

+    { url = "https://files.pythonhosted.org/packages/78/b2/00ed55b3a2efa4658fb795c38d1090ec9b3e8a6c3683d4441fa517f09c3b/lxml-6.1.1-cp314-cp314t-macosx_10_15_universal2.whl", hash = "sha256:787b2496d0dbe8cd180984e8d29e3a6f76e7ea34db781cb3bd55e4ba1ef8b4ee", size = 8827545, upload-time = "2026-05-18T19:18:41.193Z" },

+    { url = "https://files.pythonhosted.org/packages/c0/73/74573db19baa618d5f266f2407898b087ff6927115b00b71e5fc1b700847/lxml-6.1.1-cp314-cp314t-macosx_10_15_x86_64.whl", hash = "sha256:2c8daa471358dc2d6fcf02165e80ec68f77871a286df95bc5cc3816153b0fd2c", size = 4735736, upload-time = "2026-05-18T19:18:46.761Z" },

+    { url = "https://files.pythonhosted.org/packages/16/02/6f7061f4f95f51e545d48e87647c54791d204a4e881be4156e7a26ba5338/lxml-6.1.1-cp314-cp314t-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:acd7d70b64c0aae0c7922cca83d288a16f5f6da523637697872253415269baef", size = 4970291, upload-time = "2026-05-18T19:19:56.215Z" },

+    { url = "https://files.pythonhosted.org/packages/b0/02/55fc057d8283427dea7d6edb102e7a840239c77a64a983d92f62a304c0e9/lxml-6.1.1-cp314-cp314t-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:4f0dd2f01f9f8a89f565d000e03abcf0a13d692a346c8d22f628d49af098777a", size = 5102822, upload-time = "2026-05-18T19:19:59.223Z" },

+    { url = "https://files.pythonhosted.org/packages/e4/48/8e1cf78d89d66850121d9255a2a24414c98f775da93b90cf976956c24b14/lxml-6.1.1-cp314-cp314t-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:0b7e8a14c8634bf6f7a568634cb395305a6d964aeb5b7ee32248094bed3a7e2c", size = 5027923, upload-time = "2026-05-18T19:20:01.549Z" },

+    { url = "https://files.pythonhosted.org/packages/ed/00/0632a0647612c8af24d26997b3b961397daa9d5b2581444805933629a4cb/lxml-6.1.1-cp314-cp314t-manylinux_2_26_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:86281fbdd6a8162756f8d603f37e3435bfa38043adb79c6dc6a2dfee065e7525", size = 5595843, upload-time = "2026-05-18T19:20:03.93Z" },

+    { url = "https://files.pythonhosted.org/packages/bc/86/ab008a7dc360711b66858d61c80a5979a70a09f2aa2b05d9698df80b803d/lxml-6.1.1-cp314-cp314t-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:c5d7152ec39ca7c402d8fb9bad86140a15b9503bd0c54484e3f1bbe3dd37ceca", size = 5224515, upload-time = "2026-05-18T19:20:06.381Z" },

+    { url = "https://files.pythonhosted.org/packages/75/c6/2702ff375e728e34f56d9a45339a9cf7e4427e917f542225242d63a05afa/lxml-6.1.1-cp314-cp314t-manylinux_2_28_i686.whl", hash = "sha256:88d8cb75b9d82858497a5393e3c63cfbf03035225e4b35a49ed7ccb151e4dc0e", size = 5312511, upload-time = "2026-05-18T19:20:09.308Z" },

+    { url = "https://files.pythonhosted.org/packages/b7/57/a5807c98f87a86f10ef9ffab35516df7c0f0c4b6d5d33e9f608ab9c04a31/lxml-6.1.1-cp314-cp314t-manylinux_2_31_armv7l.whl", hash = "sha256:f64ec5397ea6a41fc1b4af0380d79b44a755b5531dcaccd9940fb260dca93038", size = 4639206, upload-time = "2026-05-18T19:20:11.704Z" },

+    { url = "https://files.pythonhosted.org/packages/1f/e1/8a0a2c35734812395f4da4eaf33748a7e5705bfb2a58b128da764339d5ec/lxml-6.1.1-cp314-cp314t-manylinux_2_38_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:d34bbf07dbc7ca5970671b1512e928991fb5e9d95365636c9b2d8b4f53af405e", size = 5232404, upload-time = "2026-05-18T19:20:14.064Z" },

+    { url = "https://files.pythonhosted.org/packages/c2/e2/0e6a4dd5ad84d01d99aa7bae7cfefd4a760a0e0f8176818241de17d9b6c0/lxml-6.1.1-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:17e0e18d4ad8adbd0399291bc44845b69d9dd68439a3cdebdf35ff902ec05072", size = 5083769, upload-time = "2026-05-18T19:19:23.758Z" },

+    { url = "https://files.pythonhosted.org/packages/a0/7e/161f33d463f6ffc1c7679104b65086dea120080d49dde4d238f015aaee2f/lxml-6.1.1-cp314-cp314t-musllinux_1_2_armv7l.whl", hash = "sha256:3ab541146f1f6968c462d6c2ac495148e8cdba2f8347700b2141b6ec5a75bf52", size = 4758936, upload-time = "2026-05-18T19:19:27.256Z" },

+    { url = "https://files.pythonhosted.org/packages/f1/fb/2369825e3f6ca99305bf9f7b7085fda91c8b0922a89e54d900974aa3ef85/lxml-6.1.1-cp314-cp314t-musllinux_1_2_ppc64le.whl", hash = "sha256:2a0217714657e023ef4293500f65aa20fce6164c8fd6b08fa5bd4a859fb14b9b", size = 5620296, upload-time = "2026-05-18T19:19:29.993Z" },

+    { url = "https://files.pythonhosted.org/packages/30/90/d61e383146f74c5ab683947ea14dc7b82778838ab9b95ea73a23b60d0191/lxml-6.1.1-cp314-cp314t-musllinux_1_2_riscv64.whl", hash = "sha256:05a82eb6e1530a64f26225b55cbd178113bd0b5af1c2b625f25e5296742c26d2", size = 5228598, upload-time = "2026-05-18T19:19:33.523Z" },

+    { url = "https://files.pythonhosted.org/packages/76/2d/2dafd8149e94b05bb070690efd5bb2680720681e03ff03fc57d2b70a1105/lxml-6.1.1-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:9e36f163528fc50cbef305f02a5fd66d404edf7049cdaff211dbc2cba5a7013e", size = 5247845, upload-time = "2026-05-18T19:19:36.649Z" },

+    { url = "https://files.pythonhosted.org/packages/ce/68/b30e913340c380ddac9580c6e6230991fc37240ec4f64704833e4f3e2769/lxml-6.1.1-cp314-cp314t-win32.whl", hash = "sha256:649dda677cf3bd6ac9ae14007ba0c824ded8ce5808b53fc7431d9140399118c1", size = 3897345, upload-time = "2026-05-18T19:17:33.562Z" },

+    { url = "https://files.pythonhosted.org/packages/3c/4e/9eb2af5335545f9fbcd7af57bcf87c6025d31eaa31b14ec184a6c8675328/lxml-6.1.1-cp314-cp314t-win_amd64.whl", hash = "sha256:793033d6c5cdf33a573f910d9bea14ef8f5771820411d118da8e1182edb53d5e", size = 4393350, upload-time = "2026-05-18T19:18:10.076Z" },

+    { url = "https://files.pythonhosted.org/packages/7f/2c/0f1e93c636720e8a3eb59af2bfda99d98b55891e1c53bc30c2e0e865f01b/lxml-6.1.1-cp314-cp314t-win_arm64.whl", hash = "sha256:58bb955caba94e467d2a96da17660d2d704e0675894cba21ab8a775b8621fd1c", size = 3817223, upload-time = "2026-05-19T19:22:56.823Z" },

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

+    { url = "https://files.pythonhosted.org/packages/95/2a/3d7b5ac8aac24feaf9ad7ed58f45b0bbc06d37e4338ae84c9f2298b570f9/numpy-2.4.6-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:001fbb8e08d942dd57599e781f2472269ee7f2755fae407b4f67b2f0b17da3f1", size = 16689119, upload-time = "2026-05-18T23:33:54.065Z" },

+    { url = "https://files.pythonhosted.org/packages/ea/12/92c4c131527599e8288d6918e888d88726f84d805d784b771f32408aeaef/numpy-2.4.6-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:ebfb099f8dcf083deef3ac1ca4c1503f387cf76296fcb3816b66f5ecb5f54fdb", size = 14699246, upload-time = "2026-05-18T23:33:57.621Z" },

+    { url = "https://files.pythonhosted.org/packages/ad/fe/c0a6b7b2ca128a8fb228575147073b660656734b8ebe4d76c8fd748dcc79/numpy-2.4.6-cp312-cp312-macosx_14_0_arm64.whl", hash = "sha256:3213d622a0283a39a93d188f3cf72b26862df52fbb4ca3697f51705016523d41", size = 5204410, upload-time = "2026-05-18T23:34:00.302Z" },

+    { url = "https://files.pythonhosted.org/packages/f3/d4/9770d14ba719432bb90a421bfd443872ed0f70f7264b64bec12ea363d5fd/numpy-2.4.6-cp312-cp312-macosx_14_0_x86_64.whl", hash = "sha256:357cc07a6d7b0b182ff02249616a03742827ebb1277546b5c7cd7f7620a45698", size = 6551240, upload-time = "2026-05-18T23:34:02.852Z" },

+    { url = "https://files.pythonhosted.org/packages/c9/c6/50a46a6205feba2343f1d6d17438107c5dc491ed1c736e6ea68689fd906b/numpy-2.4.6-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:5f9fb9157b4ce2971008323afe46053787b526ef624fea915b261468a8421a0f", size = 15671012, upload-time = "2026-05-18T23:34:05.485Z" },

+    { url = "https://files.pythonhosted.org/packages/99/60/14115e6364fa676c5397c2ad3004e527e9aa487abf5d0706ec81bbd08529/numpy-2.4.6-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:90f9849678c75fe7afa2d348ac842c168b0a4d3d61919687216dfc547976d853", size = 16645538, upload-time = "2026-05-18T23:34:09.265Z" },

+    { url = "https://files.pythonhosted.org/packages/ae/c5/693cbe59e57db94d2231fa519ca3978dc9e19da5a8f088588f5c6e947ff2/numpy-2.4.6-cp312-cp312-musllinux_1_2_aarch64.whl", hash = "sha256:c1a2af6c6ef86344a6b0db6b97834208bf598db514f2b155042439b62605601a", size = 17020706, upload-time = "2026-05-18T23:34:13.053Z" },

+    { url = "https://files.pythonhosted.org/packages/ef/fc/85b7c4eff9b4966ade25c2273cf7e7012e92366c032058653934b37de044/numpy-2.4.6-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:e5805d5a22fd19c8ccff10a9561f9df94436b0545619ea579db2d3c35294bce2", size = 18368541, upload-time = "2026-05-18T23:34:17.024Z" },

+    { url = "https://files.pythonhosted.org/packages/f6/81/e1b27545deedce7f4a0b348618c6b62d74e36a4dc9ccd42f3eb2f85eee32/numpy-2.4.6-cp312-cp312-win32.whl", hash = "sha256:e3eeb0aabd6bd5ce64faae67e9935203a6991b4bc2a485a767fbafb2c5125f45", size = 5962825, upload-time = "2026-05-18T23:34:20.3Z" },

+    { url = "https://files.pythonhosted.org/packages/ab/ca/feab00bd44aa5fe1ad2c18f08b4d3bb92e26484b0b1d1443897809ed528c/numpy-2.4.6-cp312-cp312-win_amd64.whl", hash = "sha256:d8e8286dd7cea7895157318d1b91cdacac64c479f3cbc8dce548331728484751", size = 12321687, upload-time = "2026-05-18T23:34:23.095Z" },

+    { url = "https://files.pythonhosted.org/packages/63/cf/5a6d34850a39d1093558564f77ee8e8e0bee5061151b8f05a55711001ec7/numpy-2.4.6-cp312-cp312-win_arm64.whl", hash = "sha256:4081eb135ac24158bd51cdfbef16f1c64df7063b1143f24731387137c092bec8", size = 10221482, upload-time = "2026-05-18T23:34:25.876Z" },

+    { url = "https://files.pythonhosted.org/packages/fb/82/bdab26d7438c6791ca31b7c024ca37c1eab8b726ba236129005cd4a06e45/numpy-2.4.6-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:511dbaf848decaaaf4b4ca48032619fb3138710c4bf7da7617765edad1ef96b0", size = 16684648, upload-time = "2026-05-18T23:34:29.41Z" },

+    { url = "https://files.pythonhosted.org/packages/1b/30/a80189bcc7f5e4258b3fbc3968d909d1756f54d023299ecc39ad6fdb9ef8/numpy-2.4.6-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:bf162abab1c1a736333192707cef898e735a5ca00f38f27eeedf44b39d9e85eb", size = 14693902, upload-time = "2026-05-18T23:34:33.013Z" },

+    { url = "https://files.pythonhosted.org/packages/97/12/70b5d0d7c15e1ebb8a6a84a8caa1d19e181d84fb58bb6d70aca29099dec1/numpy-2.4.6-cp313-cp313-macosx_14_0_arm64.whl", hash = "sha256:043191bfa8eab18c776647b62723ac9dddece59743b13f49b2016094129c2b3f", size = 5198992, upload-time = "2026-05-18T23:34:36.132Z" },

+    { url = "https://files.pythonhosted.org/packages/ba/8c/ebd2a8f8a83541f8d38cc5667e8c2b69cecfd30da6e45693e8158857d44b/numpy-2.4.6-cp313-cp313-macosx_14_0_x86_64.whl", hash = "sha256:6180d8b35af935aed8ece3a85e0a43f87393ae0ac87c8d2c8bd2c993f7270ef3", size = 6546944, upload-time = "2026-05-18T23:34:38.484Z" },

+    { url = "https://files.pythonhosted.org/packages/bb/c5/7b863a97a91671a0338f4253bd3b5a3d3852f0692dae91711c9f4a10e787/numpy-2.4.6-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:72fbe16c6fac95aedf5937fa873445cec2110be35d8a4e9433d7501fd98dae6b", size = 15669392, upload-time = "2026-05-18T23:34:41.257Z" },

+    { url = "https://files.pythonhosted.org/packages/a5/9d/3584b9984ca4c047aea75214ce1a4c4c73d849bd71b604264b7f5653f8a8/numpy-2.4.6-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:a7830bab239b79cda9c08c2da014761cafb48da6150e1da17ac06283f43b6089", size = 16633220, upload-time = "2026-05-18T23:34:45.075Z" },

+    { url = "https://files.pythonhosted.org/packages/05/ae/7c67fba23bd98caec7c99261f3a16072ade14813486b0282cb29846de832/numpy-2.4.6-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:ef4aea96ce4d3b074422cb4f2f64e216bf9e213004bb58ecfdf50ea02ea8eb9a", size = 17020800, upload-time = "2026-05-18T23:34:49.065Z" },

+    { url = "https://files.pythonhosted.org/packages/d9/5d/3b6725cb31d983c5e66916f5d36f6d7e5521129e4c4404d64f918292a5b6/numpy-2.4.6-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:dfa20cc6ca228e6b155b11da03825975ce66aea520985dbbddf0f2a5a495c605", size = 18357600, upload-time = "2026-05-18T23:34:52.709Z" },

+    { url = "https://files.pythonhosted.org/packages/f7/da/2ccc6c2fe8898dee01d90c75c5f5f914a23daf99e3e0f59516a08760c8b5/numpy-2.4.6-cp313-cp313-win32.whl", hash = "sha256:56b39e5e0622a09a25bf5baf62f4bcf0cb8a41ae6e2819cf49bbc5a74c083f91", size = 5961134, upload-time = "2026-05-18T23:34:55.618Z" },

+    { url = "https://files.pythonhosted.org/packages/b5/cd/9cc4dc876fb065d5c220aae4d5e14826b2715331bb7618ce1fb07a679d99/numpy-2.4.6-cp313-cp313-win_amd64.whl", hash = "sha256:c4fc99836233ea196540b17ab0983aff60ed07941751930f5f4d05bc3b3b7359", size = 12318598, upload-time = "2026-05-18T23:34:58.928Z" },

+    { url = "https://files.pythonhosted.org/packages/39/1e/c0bcba1f8694116485fe28fd1be698c278fcda4141c5b0e53a2aed8b12a8/numpy-2.4.6-cp313-cp313-win_arm64.whl", hash = "sha256:a7c711e21628b52034bb5ab8d1bce291f752fcc5e92accc615778acee1ff4778", size = 10222272, upload-time = "2026-05-18T23:35:02.167Z" },

+    { url = "https://files.pythonhosted.org/packages/63/6d/cc5619247c8f4204e507f5883528372e4ac4bb189e579fb859a12e480b1f/numpy-2.4.6-cp313-cp313t-macosx_11_0_arm64.whl", hash = "sha256:112b06a867b235ef466ed3508ddf0238050df9c727cafb5301ac385b899189a1", size = 14821197, upload-time = "2026-05-18T23:35:05.468Z" },

+    { url = "https://files.pythonhosted.org/packages/00/58/f1c39161c87d9e9bed660f1ed4bafc0e403d5ec9650b6dd77aead07d489b/numpy-2.4.6-cp313-cp313t-macosx_14_0_arm64.whl", hash = "sha256:eaf7fa2de5c0be8ae6ff8e9bea2ccd725e980541244521d8d4b5f3354a27babe", size = 5326287, upload-time = "2026-05-18T23:35:08.693Z" },

+    { url = "https://files.pythonhosted.org/packages/af/57/3917ab0fd97f271a8694513581b8a36c655f111c446852c302f04ccdb6fc/numpy-2.4.6-cp313-cp313t-macosx_14_0_x86_64.whl", hash = "sha256:7265a2f3d436e54ef9f2b52b5c937e6be778781bd97a590319d7348f1c1ca997", size = 6646763, upload-time = "2026-05-18T23:35:11.459Z" },

+    { url = "https://files.pythonhosted.org/packages/eb/0f/037e64c494b67581ae18193d770adef354c41f3f2c8ebf865602d949bf8f/numpy-2.4.6-cp313-cp313t-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:f74a575920ab21fe304421a3fc28793d82e299cae9eccb37084e9fc7f3617c20", size = 15728070, upload-time = "2026-05-18T23:35:14.79Z" },

+    { url = "https://files.pythonhosted.org/packages/21/a6/5d2bae9c9542eb4df16dc9c46dc79c186e9bad53805dfa5399a6023c6db0/numpy-2.4.6-cp313-cp313t-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:ede83e07a75dd06bc501566c1eca2afc0d61677c1472ac9ad93fdee6e638a48d", size = 16681752, upload-time = "2026-05-18T23:35:18.836Z" },

+    { url = "https://files.pythonhosted.org/packages/92/14/23d1dfb410ae362cd59ce53e936b1513d545eb40db3949ced632e19a459e/numpy-2.4.6-cp313-cp313t-musllinux_1_2_aarch64.whl", hash = "sha256:68bb27509ac1b9a3443094260f6326150663b06abe40b73a2f81160623da5b67", size = 17086024, upload-time = "2026-05-18T23:35:22.52Z" },

+    { url = "https://files.pythonhosted.org/packages/4b/6e/23595a2c642cdf3bc567877064bdd7f91c8b0038a4453cf2daf7248eafe9/numpy-2.4.6-cp313-cp313t-musllinux_1_2_x86_64.whl", hash = "sha256:a0df0043bdb289bde1f62da130d20df23d58b45429f752bc7a8fc5325a225ecd", size = 18403398, upload-time = "2026-05-18T23:35:26.398Z" },

+    { url = "https://files.pythonhosted.org/packages/8a/90/0ac3bc947217e66dec77e7cbc6a1979d1af70b6461b82f620d3bccd5e4c8/numpy-2.4.6-cp313-cp313t-win32.whl", hash = "sha256:29a287e0cf63ff528da061de6b9f64a4618da591ca1046aafc54062e40ca7eab", size = 6084971, upload-time = "2026-05-18T23:35:29.387Z" },

+    { url = "https://files.pythonhosted.org/packages/77/71/5673e351671a1d2bd6063b91b44f70c0affea7d1516fa7a6572941ba4aa1/numpy-2.4.6-cp313-cp313t-win_amd64.whl", hash = "sha256:25c692919ac5a01f170a3bfcd62d745b24fd095c353d50812637d6fcab442e75", size = 12458532, upload-time = "2026-05-18T23:35:32.175Z" },

+    { url = "https://files.pythonhosted.org/packages/3f/88/19d3503c5046e688f049274b27a3ef3d771152fa80d3ba3d01a3dff61abe/numpy-2.4.6-cp313-cp313t-win_arm64.whl", hash = "sha256:1e978ec1e8bd0e0e4de6bb75de9d30cbb74db6b6a2bb727618613703ca0167dd", size = 10291881, upload-time = "2026-05-18T23:35:35.465Z" },

+    { url = "https://files.pythonhosted.org/packages/f8/91/3ab2044d05fd16d343c5ac2e69b127f1b2854040dd20b193257c78028bd3/numpy-2.4.6-cp314-cp314-macosx_10_15_x86_64.whl", hash = "sha256:06ca2f61ec4385a07a6977c55ba998a4466c123642b4a32694d3128fce18c079", size = 16683458, upload-time = "2026-05-18T23:35:38.353Z" },

+    { url = "https://files.pythonhosted.org/packages/8e/62/764ce66fa4147ae6d73071a3abf804ffe606f174618697c571acdf26a7c9/numpy-2.4.6-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:38efbc8de75c7a0fc1ac190162d892787f3f47b57cc291231aafee36b80982b7", size = 14704559, upload-time = "2026-05-18T23:35:42.14Z" },

+    { url = "https://files.pythonhosted.org/packages/60/61/23f27c172f022e04025b7dc2367f4d63c1a398120607ec896228649a6f48/numpy-2.4.6-cp314-cp314-macosx_14_0_arm64.whl", hash = "sha256:d581b735e177fdcdce6fed8e7e8880a3fb6ee4e3653a3ac6af01c6f4c03effc5", size = 5209716, upload-time = "2026-05-18T23:35:45.377Z" },

+    { url = "https://files.pythonhosted.org/packages/03/71/21cf70dc6ea3e3acb95fc53a265b2fc248b981f0194ceb5b475271b8809d/numpy-2.4.6-cp314-cp314-macosx_14_0_x86_64.whl", hash = "sha256:0a041d3d761dc3c35cc56ce0351506a02bcbc25f7b169f652435141a17db9096", size = 6543947, upload-time = "2026-05-18T23:35:47.926Z" },

+    { url = "https://files.pythonhosted.org/packages/d5/91/64288395ee1799bd2e0b04a305dce9666da90c961e1f3fe982a05ee1c036/numpy-2.4.6-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:40fdc1ae7125e518ea98e53e69a4ebc27e1fd50510c47b7ea130cf21e5e1d42b", size = 15685197, upload-time = "2026-05-18T23:35:50.863Z" },

+    { url = "https://files.pythonhosted.org/packages/f3/eb/ebffaa97dc55502df69584a8f0dcf07f69a3e0b3e2323670a2722db9aa39/numpy-2.4.6-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:a2c306dea656c12c68f51f4cea133cbe78ca7435eb28c735eac1d3ebe73be6e8", size = 16638245, upload-time = "2026-05-18T23:35:54.752Z" },

+    { url = "https://files.pythonhosted.org/packages/b8/0b/54f9da33128d7e350fab89c7455902eeae70349ee52bddb448dc4a576f45/numpy-2.4.6-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:33111801a01c12a8a1e3721f0a9232f8cfc8ae2c6b7098167e6f623c6073f402", size = 17036587, upload-time = "2026-05-18T23:35:58.355Z" },

+    { url = "https://files.pythonhosted.org/packages/b6/f0/fdebc1052db1cc37c64beb22072d67cd6d1c71adca1299f53dec2b5e20d3/numpy-2.4.6-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:ae506e6902902557576a26ff33eda8695e7ecb3cb36c3b573a0765dee114ebdb", size = 18363226, upload-time = "2026-05-18T23:36:02.845Z" },

+    { url = "https://files.pythonhosted.org/packages/aa/b4/298628d98c72b57e57f7165ae6a481a1deaf6f3c28262a6e4c739c275930/numpy-2.4.6-cp314-cp314-win32.whl", hash = "sha256:aaf159caa35993cb1f56fb9b8e4610d35758e7ca005412eb1daa856a78c9c4b1", size = 6010196, upload-time = "2026-05-18T23:36:05.92Z" },

+    { url = "https://files.pythonhosted.org/packages/df/ac/46de6dda46478f7942f839e094970be2d4a861e005c4b3bf07c92e291a09/numpy-2.4.6-cp314-cp314-win_amd64.whl", hash = "sha256:b507f5c4c1d508876d1819b6bf9a49d365b96320b5d4993426b33a23ca4b8261", size = 12450334, upload-time = "2026-05-18T23:36:09.107Z" },

+    { url = "https://files.pythonhosted.org/packages/78/92/b8b798ac784102c0da830d2257d59358e3d3d90d1e2b3f2575dad976c5cf/numpy-2.4.6-cp314-cp314-win_arm64.whl", hash = "sha256:6f41ae150c4e32db4f3310cdaf64b1593a03dbabe29eec77fc9b50fe64061df6", size = 10495678, upload-time = "2026-05-18T23:36:12.766Z" },

+    { url = "https://files.pythonhosted.org/packages/30/34/ec28d1aa8115971537c01469ab2011ee96827930f0a124de1000cc2a7ed7/numpy-2.4.6-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:ece3d2cfe132e7d51f44a832b303895e6f2d499c5e74dfbdb06ee246147a304a", size = 14823672, upload-time = "2026-05-18T23:36:16.473Z" },

+    { url = "https://files.pythonhosted.org/packages/16/bd/f6d1fede4e54e8042a7ff97bb495510f3c220f94bcd9e8b228e87c92cc0d/numpy-2.4.6-cp314-cp314t-macosx_14_0_arm64.whl", hash = "sha256:e3e5193ef5a3dc73bceee50f7fdc2c90dbb76c42df8d8fae3d1067a583df579e", size = 5328731, upload-time = "2026-05-18T23:36:19.767Z" },

+    { url = "https://files.pythonhosted.org/packages/f4/f0/e105b9e2fd728a9910103884decd6951d9dd73896b914a98d9a231de02ee/numpy-2.4.6-cp314-cp314t-macosx_14_0_x86_64.whl", hash = "sha256:17f9ade344e7d9b464a084d69bcf18fc691cb1db67c62ed80820bf4926d78f0e", size = 6649805, upload-time = "2026-05-18T23:36:22.266Z" },

+    { url = "https://files.pythonhosted.org/packages/82/dd/1206a7ca6ab15e3f02069707ca96222e202af681bb73756da7527f3cb837/numpy-2.4.6-cp314-cp314t-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:9cd5ffd25db4e7ba6a375693b3fc0fc1791ec636c17db3720da19bde7180ec43", size = 15730496, upload-time = "2026-05-18T23:36:25.713Z" },

+    { url = "https://files.pythonhosted.org/packages/51/e7/38d3ea825dcab85a591734decb2f6c67caa7c8367d374df1a1c3842f9b07/numpy-2.4.6-cp314-cp314t-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:7d92c3819208a60205a12a245c91ad70cb0a85336659b19b834205573ac8456e", size = 16679616, upload-time = "2026-05-18T23:36:29.652Z" },

+    { url = "https://files.pythonhosted.org/packages/93/b7/caabfdf53edf663e0b4eb74d7d405d83baef09eb5e83bcd32d601d72b93e/numpy-2.4.6-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:e85b752a1e912b70eaad4fafbd4d1238007ab221de2009b9a2f5ae7461239895", size = 17085145, upload-time = "2026-05-18T23:36:33.449Z" },

+    { url = "https://files.pythonhosted.org/packages/f9/45/68d7c33a6bcf3e5aa3bdbd57a367e6f615286dfd6482f97e8ffeb734306e/numpy-2.4.6-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:29cb7f67d10b479ff07c17d33e39f78c07f71c40ef30d63c153d340e96cd3fb4", size = 18403813, upload-time = "2026-05-18T23:36:37.369Z" },

+    { url = "https://files.pythonhosted.org/packages/9c/50/0753655aa844c99cd9e018aacf76f130f1bd81d881bb74bc0aef5d73a8ba/numpy-2.4.6-cp314-cp314t-win32.whl", hash = "sha256:260a5d70215b61ab4fadf5c7baacd64821842975eea312125ed3c39a6391b063", size = 6156982, upload-time = "2026-05-18T23:36:40.817Z" },

+    { url = "https://files.pythonhosted.org/packages/b2/d4/7c67becf668f973cb490cec3e98dfd799d866f9c989a54d355672cfa0db6/numpy-2.4.6-cp314-cp314t-win_amd64.whl", hash = "sha256:81a1cca95ed5bb92aa8b10dd2cdc9a0d3853a50fad926c28b5d7e8ea54389627", size = 12638908, upload-time = "2026-05-18T23:36:43.996Z" },

+    { url = "https://files.pythonhosted.org/packages/43/bb/e1c71a4295b1b1d1393d50dbb4f2a36283c6859d9d3892e84f00ec5a91d5/numpy-2.4.6-cp314-cp314t-win_arm64.whl", hash = "sha256:0c9136e14ed34a9e343a31c533d78a9813a69a3148332bce5e9821cb2f996e66", size = 10565867, upload-time = "2026-05-18T23:36:47.114Z" },

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

+    { url = "https://files.pythonhosted.org/packages/58/be/7482c8a5ebebbc6470b3eb791812fff7d5e0216c2be3827b30b8bb6603ed/pillow-12.2.0-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:2d192a155bbcec180f8564f693e6fd9bccff5a7af9b32e2e4bf8c9c69dbad6b5", size = 5308279, upload-time = "2026-04-01T14:43:13.246Z" },

+    { url = "https://files.pythonhosted.org/packages/d8/95/0a351b9289c2b5cbde0bacd4a83ebc44023e835490a727b2a3bd60ddc0f4/pillow-12.2.0-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:f3f40b3c5a968281fd507d519e444c35f0ff171237f4fdde090dd60699458421", size = 4695490, upload-time = "2026-04-01T14:43:15.584Z" },

+    { url = "https://files.pythonhosted.org/packages/de/af/4e8e6869cbed569d43c416fad3dc4ecb944cb5d9492defaed89ddd6fe871/pillow-12.2.0-cp312-cp312-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:03e7e372d5240cc23e9f07deca4d775c0817bffc641b01e9c3af208dbd300987", size = 6284462, upload-time = "2026-04-01T14:43:18.268Z" },

+    { url = "https://files.pythonhosted.org/packages/e9/9e/c05e19657fd57841e476be1ab46c4d501bffbadbafdc31a6d665f8b737b6/pillow-12.2.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:b86024e52a1b269467a802258c25521e6d742349d760728092e1bc2d135b4d76", size = 8094744, upload-time = "2026-04-01T14:43:20.716Z" },

+    { url = "https://files.pythonhosted.org/packages/2b/54/1789c455ed10176066b6e7e6da1b01e50e36f94ba584dc68d9eebfe9156d/pillow-12.2.0-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:7371b48c4fa448d20d2714c9a1f775a81155050d383333e0a6c15b1123dda005", size = 6398371, upload-time = "2026-04-01T14:43:23.443Z" },

+    { url = "https://files.pythonhosted.org/packages/43/e3/fdc657359e919462369869f1c9f0e973f353f9a9ee295a39b1fea8ee1a77/pillow-12.2.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:62f5409336adb0663b7caa0da5c7d9e7bdbaae9ce761d34669420c2a801b2780", size = 7087215, upload-time = "2026-04-01T14:43:26.758Z" },

+    { url = "https://files.pythonhosted.org/packages/8b/f8/2f6825e441d5b1959d2ca5adec984210f1ec086435b0ed5f52c19b3b8a6e/pillow-12.2.0-cp312-cp312-musllinux_1_2_aarch64.whl", hash = "sha256:01afa7cf67f74f09523699b4e88c73fb55c13346d212a59a2db1f86b0a63e8c5", size = 6509783, upload-time = "2026-04-01T14:43:29.56Z" },

+    { url = "https://files.pythonhosted.org/packages/67/f9/029a27095ad20f854f9dba026b3ea6428548316e057e6fc3545409e86651/pillow-12.2.0-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:fc3d34d4a8fbec3e88a79b92e5465e0f9b842b628675850d860b8bd300b159f5", size = 7212112, upload-time = "2026-04-01T14:43:32.091Z" },

+    { url = "https://files.pythonhosted.org/packages/be/42/025cfe05d1be22dbfdb4f264fe9de1ccda83f66e4fc3aac94748e784af04/pillow-12.2.0-cp312-cp312-win32.whl", hash = "sha256:58f62cc0f00fd29e64b29f4fd923ffdb3859c9f9e6105bfc37ba1d08994e8940", size = 6378489, upload-time = "2026-04-01T14:43:34.601Z" },

+    { url = "https://files.pythonhosted.org/packages/5d/7b/25a221d2c761c6a8ae21bfa3874988ff2583e19cf8a27bf2fee358df7942/pillow-12.2.0-cp312-cp312-win_amd64.whl", hash = "sha256:7f84204dee22a783350679a0333981df803dac21a0190d706a50475e361c93f5", size = 7084129, upload-time = "2026-04-01T14:43:37.213Z" },

+    { url = "https://files.pythonhosted.org/packages/10/e1/542a474affab20fd4a0f1836cb234e8493519da6b76899e30bcc5d990b8b/pillow-12.2.0-cp312-cp312-win_arm64.whl", hash = "sha256:af73337013e0b3b46f175e79492d96845b16126ddf79c438d7ea7ff27783a414", size = 2463612, upload-time = "2026-04-01T14:43:39.421Z" },

+    { url = "https://files.pythonhosted.org/packages/4a/01/53d10cf0dbad820a8db274d259a37ba50b88b24768ddccec07355382d5ad/pillow-12.2.0-cp313-cp313-ios_13_0_arm64_iphoneos.whl", hash = "sha256:8297651f5b5679c19968abefd6bb84d95fe30ef712eb1b2d9b2d31ca61267f4c", size = 4100837, upload-time = "2026-04-01T14:43:41.506Z" },

+    { url = "https://files.pythonhosted.org/packages/0f/98/f3a6657ecb698c937f6c76ee564882945f29b79bad496abcba0e84659ec5/pillow-12.2.0-cp313-cp313-ios_13_0_arm64_iphonesimulator.whl", hash = "sha256:50d8520da2a6ce0af445fa6d648c4273c3eeefbc32d7ce049f22e8b5c3daecc2", size = 4176528, upload-time = "2026-04-01T14:43:43.773Z" },

+    { url = "https://files.pythonhosted.org/packages/69/bc/8986948f05e3ea490b8442ea1c1d4d990b24a7e43d8a51b2c7d8b1dced36/pillow-12.2.0-cp313-cp313-ios_13_0_x86_64_iphonesimulator.whl", hash = "sha256:766cef22385fa1091258ad7e6216792b156dc16d8d3fa607e7545b2b72061f1c", size = 3640401, upload-time = "2026-04-01T14:43:45.87Z" },

+    { url = "https://files.pythonhosted.org/packages/34/46/6c717baadcd62bc8ed51d238d521ab651eaa74838291bda1f86fe1f864c9/pillow-12.2.0-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:5d2fd0fa6b5d9d1de415060363433f28da8b1526c1c129020435e186794b3795", size = 5308094, upload-time = "2026-04-01T14:43:48.438Z" },

+    { url = "https://files.pythonhosted.org/packages/71/43/905a14a8b17fdb1ccb58d282454490662d2cb89a6bfec26af6d3520da5ec/pillow-12.2.0-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:56b25336f502b6ed02e889f4ece894a72612fe885889a6e8c4c80239ff6e5f5f", size = 4695402, upload-time = "2026-04-01T14:43:51.292Z" },

+    { url = "https://files.pythonhosted.org/packages/73/dd/42107efcb777b16fa0393317eac58f5b5cf30e8392e266e76e51cff28c3d/pillow-12.2.0-cp313-cp313-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:f1c943e96e85df3d3478f7b691f229887e143f81fedab9b20205349ab04d73ed", size = 6280005, upload-time = "2026-04-01T14:43:54.242Z" },

+    { url = "https://files.pythonhosted.org/packages/a8/68/b93e09e5e8549019e61acf49f65b1a8530765a7f812c77a7461bca7e4494/pillow-12.2.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:03f6fab9219220f041c74aeaa2939ff0062bd5c364ba9ce037197f4c6d498cd9", size = 8090669, upload-time = "2026-04-01T14:43:57.335Z" },

+    { url = "https://files.pythonhosted.org/packages/4b/6e/3ccb54ce8ec4ddd1accd2d89004308b7b0b21c4ac3d20fa70af4760a4330/pillow-12.2.0-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:5cdfebd752ec52bf5bb4e35d9c64b40826bc5b40a13df7c3cda20a2c03a0f5ed", size = 6395194, upload-time = "2026-04-01T14:43:59.864Z" },

+    { url = "https://files.pythonhosted.org/packages/67/ee/21d4e8536afd1a328f01b359b4d3997b291ffd35a237c877b331c1c3b71c/pillow-12.2.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:eedf4b74eda2b5a4b2b2fb4c006d6295df3bf29e459e198c90ea48e130dc75c3", size = 7082423, upload-time = "2026-04-01T14:44:02.74Z" },

+    { url = "https://files.pythonhosted.org/packages/78/5f/e9f86ab0146464e8c133fe85df987ed9e77e08b29d8d35f9f9f4d6f917ba/pillow-12.2.0-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:00a2865911330191c0b818c59103b58a5e697cae67042366970a6b6f1b20b7f9", size = 6505667, upload-time = "2026-04-01T14:44:05.381Z" },

+    { url = "https://files.pythonhosted.org/packages/ed/1e/409007f56a2fdce61584fd3acbc2bbc259857d555196cedcadc68c015c82/pillow-12.2.0-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:1e1757442ed87f4912397c6d35a0db6a7b52592156014706f17658ff58bbf795", size = 7208580, upload-time = "2026-04-01T14:44:08.39Z" },

+    { url = "https://files.pythonhosted.org/packages/23/c4/7349421080b12fb35414607b8871e9534546c128a11965fd4a7002ccfbee/pillow-12.2.0-cp313-cp313-win32.whl", hash = "sha256:144748b3af2d1b358d41286056d0003f47cb339b8c43a9ea42f5fea4d8c66b6e", size = 6375896, upload-time = "2026-04-01T14:44:11.197Z" },

+    { url = "https://files.pythonhosted.org/packages/3f/82/8a3739a5e470b3c6cbb1d21d315800d8e16bff503d1f16b03a4ec3212786/pillow-12.2.0-cp313-cp313-win_amd64.whl", hash = "sha256:390ede346628ccc626e5730107cde16c42d3836b89662a115a921f28440e6a3b", size = 7081266, upload-time = "2026-04-01T14:44:13.947Z" },

+    { url = "https://files.pythonhosted.org/packages/c3/25/f968f618a062574294592f668218f8af564830ccebdd1fa6200f598e65c5/pillow-12.2.0-cp313-cp313-win_arm64.whl", hash = "sha256:8023abc91fba39036dbce14a7d6535632f99c0b857807cbbbf21ecc9f4717f06", size = 2463508, upload-time = "2026-04-01T14:44:16.312Z" },

+    { url = "https://files.pythonhosted.org/packages/4d/a4/b342930964e3cb4dce5038ae34b0eab4653334995336cd486c5a8c25a00c/pillow-12.2.0-cp313-cp313t-macosx_10_13_x86_64.whl", hash = "sha256:042db20a421b9bafecc4b84a8b6e444686bd9d836c7fd24542db3e7df7baad9b", size = 5309927, upload-time = "2026-04-01T14:44:18.89Z" },

+    { url = "https://files.pythonhosted.org/packages/9f/de/23198e0a65a9cf06123f5435a5d95cea62a635697f8f03d134d3f3a96151/pillow-12.2.0-cp313-cp313t-macosx_11_0_arm64.whl", hash = "sha256:dd025009355c926a84a612fecf58bb315a3f6814b17ead51a8e48d3823d9087f", size = 4698624, upload-time = "2026-04-01T14:44:21.115Z" },

+    { url = "https://files.pythonhosted.org/packages/01/a6/1265e977f17d93ea37aa28aa81bad4fa597933879fac2520d24e021c8da3/pillow-12.2.0-cp313-cp313t-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:88ddbc66737e277852913bd1e07c150cc7bb124539f94c4e2df5344494e0a612", size = 6321252, upload-time = "2026-04-01T14:44:23.663Z" },

+    { url = "https://files.pythonhosted.org/packages/3c/83/5982eb4a285967baa70340320be9f88e57665a387e3a53a7f0db8231a0cd/pillow-12.2.0-cp313-cp313t-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:d362d1878f00c142b7e1a16e6e5e780f02be8195123f164edf7eddd911eefe7c", size = 8126550, upload-time = "2026-04-01T14:44:26.772Z" },

+    { url = "https://files.pythonhosted.org/packages/4e/48/6ffc514adce69f6050d0753b1a18fd920fce8cac87620d5a31231b04bfc5/pillow-12.2.0-cp313-cp313t-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:2c727a6d53cb0018aadd8018c2b938376af27914a68a492f59dfcaca650d5eea", size = 6433114, upload-time = "2026-04-01T14:44:29.615Z" },

+    { url = "https://files.pythonhosted.org/packages/36/a3/f9a77144231fb8d40ee27107b4463e205fa4677e2ca2548e14da5cf18dce/pillow-12.2.0-cp313-cp313t-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:efd8c21c98c5cc60653bcb311bef2ce0401642b7ce9d09e03a7da87c878289d4", size = 7115667, upload-time = "2026-04-01T14:44:32.773Z" },

+    { url = "https://files.pythonhosted.org/packages/c1/fc/ac4ee3041e7d5a565e1c4fd72a113f03b6394cc72ab7089d27608f8aaccb/pillow-12.2.0-cp313-cp313t-musllinux_1_2_aarch64.whl", hash = "sha256:9f08483a632889536b8139663db60f6724bfcb443c96f1b18855860d7d5c0fd4", size = 6538966, upload-time = "2026-04-01T14:44:35.252Z" },

+    { url = "https://files.pythonhosted.org/packages/c0/a8/27fb307055087f3668f6d0a8ccb636e7431d56ed0750e07a60547b1e083e/pillow-12.2.0-cp313-cp313t-musllinux_1_2_x86_64.whl", hash = "sha256:dac8d77255a37e81a2efcbd1fc05f1c15ee82200e6c240d7e127e25e365c39ea", size = 7238241, upload-time = "2026-04-01T14:44:37.875Z" },

+    { url = "https://files.pythonhosted.org/packages/ad/4b/926ab182c07fccae9fcb120043464e1ff1564775ec8864f21a0ebce6ac25/pillow-12.2.0-cp313-cp313t-win32.whl", hash = "sha256:ee3120ae9dff32f121610bb08e4313be87e03efeadfc6c0d18f89127e24d0c24", size = 6379592, upload-time = "2026-04-01T14:44:40.336Z" },

+    { url = "https://files.pythonhosted.org/packages/c2/c4/f9e476451a098181b30050cc4c9a3556b64c02cf6497ea421ac047e89e4b/pillow-12.2.0-cp313-cp313t-win_amd64.whl", hash = "sha256:325ca0528c6788d2a6c3d40e3568639398137346c3d6e66bb61db96b96511c98", size = 7085542, upload-time = "2026-04-01T14:44:43.251Z" },

+    { url = "https://files.pythonhosted.org/packages/00/a4/285f12aeacbe2d6dc36c407dfbbe9e96d4a80b0fb710a337f6d2ad978c75/pillow-12.2.0-cp313-cp313t-win_arm64.whl", hash = "sha256:2e5a76d03a6c6dcef67edabda7a52494afa4035021a79c8558e14af25313d453", size = 2465765, upload-time = "2026-04-01T14:44:45.996Z" },

+    { url = "https://files.pythonhosted.org/packages/bf/98/4595daa2365416a86cb0d495248a393dfc84e96d62ad080c8546256cb9c0/pillow-12.2.0-cp314-cp314-ios_13_0_arm64_iphoneos.whl", hash = "sha256:3adc9215e8be0448ed6e814966ecf3d9952f0ea40eb14e89a102b87f450660d8", size = 4100848, upload-time = "2026-04-01T14:44:48.48Z" },

+    { url = "https://files.pythonhosted.org/packages/0b/79/40184d464cf89f6663e18dfcf7ca21aae2491fff1a16127681bf1fa9b8cf/pillow-12.2.0-cp314-cp314-ios_13_0_arm64_iphonesimulator.whl", hash = "sha256:6a9adfc6d24b10f89588096364cc726174118c62130c817c2837c60cf08a392b", size = 4176515, upload-time = "2026-04-01T14:44:51.353Z" },

+    { url = "https://files.pythonhosted.org/packages/b0/63/703f86fd4c422a9cf722833670f4f71418fb116b2853ff7da722ea43f184/pillow-12.2.0-cp314-cp314-ios_13_0_x86_64_iphonesimulator.whl", hash = "sha256:6a6e67ea2e6feda684ed370f9a1c52e7a243631c025ba42149a2cc5934dec295", size = 3640159, upload-time = "2026-04-01T14:44:53.588Z" },

+    { url = "https://files.pythonhosted.org/packages/71/e0/fb22f797187d0be2270f83500aab851536101b254bfa1eae10795709d283/pillow-12.2.0-cp314-cp314-macosx_10_15_x86_64.whl", hash = "sha256:2bb4a8d594eacdfc59d9e5ad972aa8afdd48d584ffd5f13a937a664c3e7db0ed", size = 5312185, upload-time = "2026-04-01T14:44:56.039Z" },

+    { url = "https://files.pythonhosted.org/packages/ba/8c/1a9e46228571de18f8e28f16fabdfc20212a5d019f3e3303452b3f0a580d/pillow-12.2.0-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:80b2da48193b2f33ed0c32c38140f9d3186583ce7d516526d462645fd98660ae", size = 4695386, upload-time = "2026-04-01T14:44:58.663Z" },

+    { url = "https://files.pythonhosted.org/packages/70/62/98f6b7f0c88b9addd0e87c217ded307b36be024d4ff8869a812b241d1345/pillow-12.2.0-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:22db17c68434de69d8ecfc2fe821569195c0c373b25cccb9cbdacf2c6e53c601", size = 6280384, upload-time = "2026-04-01T14:45:01.5Z" },

+    { url = "https://files.pythonhosted.org/packages/5e/03/688747d2e91cfbe0e64f316cd2e8005698f76ada3130d0194664174fa5de/pillow-12.2.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:7b14cc0106cd9aecda615dd6903840a058b4700fcb817687d0ee4fc8b6e389be", size = 8091599, upload-time = "2026-04-01T14:45:04.5Z" },

+    { url = "https://files.pythonhosted.org/packages/f6/35/577e22b936fcdd66537329b33af0b4ccfefaeabd8aec04b266528cddb33c/pillow-12.2.0-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:8cbeb542b2ebc6fcdacabf8aca8c1a97c9b3ad3927d46b8723f9d4f033288a0f", size = 6396021, upload-time = "2026-04-01T14:45:07.117Z" },

+    { url = "https://files.pythonhosted.org/packages/11/8d/d2532ad2a603ca2b93ad9f5135732124e57811d0168155852f37fbce2458/pillow-12.2.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:4bfd07bc812fbd20395212969e41931001fd59eb55a60658b0e5710872e95286", size = 7083360, upload-time = "2026-04-01T14:45:09.763Z" },

+    { url = "https://files.pythonhosted.org/packages/5e/26/d325f9f56c7e039034897e7380e9cc202b1e368bfd04d4cbe6a441f02885/pillow-12.2.0-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:9aba9a17b623ef750a4d11b742cbafffeb48a869821252b30ee21b5e91392c50", size = 6507628, upload-time = "2026-04-01T14:45:12.378Z" },

+    { url = "https://files.pythonhosted.org/packages/5f/f7/769d5632ffb0988f1c5e7660b3e731e30f7f8ec4318e94d0a5d674eb65a4/pillow-12.2.0-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:deede7c263feb25dba4e82ea23058a235dcc2fe1f6021025dc71f2b618e26104", size = 7209321, upload-time = "2026-04-01T14:45:15.122Z" },

+    { url = "https://files.pythonhosted.org/packages/6a/7a/c253e3c645cd47f1aceea6a8bacdba9991bf45bb7dfe927f7c893e89c93c/pillow-12.2.0-cp314-cp314-win32.whl", hash = "sha256:632ff19b2778e43162304d50da0181ce24ac5bb8180122cbe1bf4673428328c7", size = 6479723, upload-time = "2026-04-01T14:45:17.797Z" },

+    { url = "https://files.pythonhosted.org/packages/cd/8b/601e6566b957ca50e28725cb6c355c59c2c8609751efbecd980db44e0349/pillow-12.2.0-cp314-cp314-win_amd64.whl", hash = "sha256:4e6c62e9d237e9b65fac06857d511e90d8461a32adcc1b9065ea0c0fa3a28150", size = 7217400, upload-time = "2026-04-01T14:45:20.529Z" },

+    { url = "https://files.pythonhosted.org/packages/d6/94/220e46c73065c3e2951bb91c11a1fb636c8c9ad427ac3ce7d7f3359b9b2f/pillow-12.2.0-cp314-cp314-win_arm64.whl", hash = "sha256:b1c1fbd8a5a1af3412a0810d060a78b5136ec0836c8a4ef9aa11807f2a22f4e1", size = 2554835, upload-time = "2026-04-01T14:45:23.162Z" },

+    { url = "https://files.pythonhosted.org/packages/b6/ab/1b426a3974cb0e7da5c29ccff4807871d48110933a57207b5a676cccc155/pillow-12.2.0-cp314-cp314t-macosx_10_15_x86_64.whl", hash = "sha256:57850958fe9c751670e49b2cecf6294acc99e562531f4bd317fa5ddee2068463", size = 5314225, upload-time = "2026-04-01T14:45:25.637Z" },

+    { url = "https://files.pythonhosted.org/packages/19/1e/dce46f371be2438eecfee2a1960ee2a243bbe5e961890146d2dee1ff0f12/pillow-12.2.0-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:d5d38f1411c0ed9f97bcb49b7bd59b6b7c314e0e27420e34d99d844b9ce3b6f3", size = 4698541, upload-time = "2026-04-01T14:45:28.355Z" },

+    { url = "https://files.pythonhosted.org/packages/55/c3/7fbecf70adb3a0c33b77a300dc52e424dc22ad8cdc06557a2e49523b703d/pillow-12.2.0-cp314-cp314t-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:5c0a9f29ca8e79f09de89293f82fc9b0270bb4af1d58bc98f540cc4aedf03166", size = 6322251, upload-time = "2026-04-01T14:45:30.924Z" },

+    { url = "https://files.pythonhosted.org/packages/1c/3c/7fbc17cfb7e4fe0ef1642e0abc17fc6c94c9f7a16be41498e12e2ba60408/pillow-12.2.0-cp314-cp314t-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:1610dd6c61621ae1cf811bef44d77e149ce3f7b95afe66a4512f8c59f25d9ebe", size = 8127807, upload-time = "2026-04-01T14:45:33.908Z" },

+    { url = "https://files.pythonhosted.org/packages/ff/c3/a8ae14d6defd2e448493ff512fae903b1e9bd40b72efb6ec55ce0048c8ce/pillow-12.2.0-cp314-cp314t-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:0a34329707af4f73cf1782a36cd2289c0368880654a2c11f027bcee9052d35dd", size = 6433935, upload-time = "2026-04-01T14:45:36.623Z" },

+    { url = "https://files.pythonhosted.org/packages/6e/32/2880fb3a074847ac159d8f902cb43278a61e85f681661e7419e6596803ed/pillow-12.2.0-cp314-cp314t-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:8e9c4f5b3c546fa3458a29ab22646c1c6c787ea8f5ef51300e5a60300736905e", size = 7116720, upload-time = "2026-04-01T14:45:39.258Z" },

+    { url = "https://files.pythonhosted.org/packages/46/87/495cc9c30e0129501643f24d320076f4cc54f718341df18cc70ec94c44e1/pillow-12.2.0-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:fb043ee2f06b41473269765c2feae53fc2e2fbf96e5e22ca94fb5ad677856f06", size = 6540498, upload-time = "2026-04-01T14:45:41.879Z" },

+    { url = "https://files.pythonhosted.org/packages/18/53/773f5edca692009d883a72211b60fdaf8871cbef075eaa9d577f0a2f989e/pillow-12.2.0-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:f278f034eb75b4e8a13a54a876cc4a5ab39173d2cdd93a638e1b467fc545ac43", size = 7239413, upload-time = "2026-04-01T14:45:44.705Z" },

+    { url = "https://files.pythonhosted.org/packages/c9/e4/4b64a97d71b2a83158134abbb2f5bd3f8a2ea691361282f010998f339ec7/pillow-12.2.0-cp314-cp314t-win32.whl", hash = "sha256:6bb77b2dcb06b20f9f4b4a8454caa581cd4dd0643a08bacf821216a16d9c8354", size = 6482084, upload-time = "2026-04-01T14:45:47.568Z" },

+    { url = "https://files.pythonhosted.org/packages/ba/13/306d275efd3a3453f72114b7431c877d10b1154014c1ebbedd067770d629/pillow-12.2.0-cp314-cp314t-win_amd64.whl", hash = "sha256:6562ace0d3fb5f20ed7290f1f929cae41b25ae29528f2af1722966a0a02e2aa1", size = 7225152, upload-time = "2026-04-01T14:45:50.032Z" },

+    { url = "https://files.pythonhosted.org/packages/ff/6e/cf826fae916b8658848d7b9f38d88da6396895c676e8086fc0988073aaf8/pillow-12.2.0-cp314-cp314t-win_arm64.whl", hash = "sha256:aa88ccfe4e32d362816319ed727a004423aab09c5cea43c01a4b435643fa34eb", size = 2556579, upload-time = "2026-04-01T14:45:52.529Z" },

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

+    { url = "https://files.pythonhosted.org/packages/ce/8c/af022f0af448d7747c5154288d46b5f2bc5f17366eaa0e23e9aa04d59f3b/pydantic_core-2.46.4-cp312-cp312-macosx_10_12_x86_64.whl", hash = "sha256:3245406455a5d98187ec35530fd772b1d799b26667980872c8d4614991e2c4a2", size = 2106158, upload-time = "2026-05-06T13:38:57.215Z" },

+    { url = "https://files.pythonhosted.org/packages/19/95/6195171e385007300f0f5574592e467c568becce2d937a0b6804f218bc49/pydantic_core-2.46.4-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:962ccbab7b642487b1d8b7df90ef677e03134cf1fd8880bf698649b22a69371f", size = 1951724, upload-time = "2026-05-06T13:37:02.697Z" },

+    { url = "https://files.pythonhosted.org/packages/8e/bc/f47d1ff9cbb1620e1b5b697eef06010035735f07820180e74178226b27b3/pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:8233f2947cf85404441fd7e0085f53b10c93e0ee78611099b5c7237e36aacbf7", size = 1975742, upload-time = "2026-05-06T13:37:09.448Z" },

+    { url = "https://files.pythonhosted.org/packages/5b/11/9b9a5b0306345664a2da6410877af6e8082481b5884b3ddd78d47c6013ce/pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:3a233125ac121aa3ffba9a2b59edfc4a985a76092dc8279586ab4b71390875e7", size = 2052418, upload-time = "2026-05-06T13:37:38.234Z" },

+    { url = "https://files.pythonhosted.org/packages/f1/b7/a65fec226f5d78fc39f4a13c4cc0c768c22b113438f60c14adc9d2865038/pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:5b712b53160b79a5850310b912a5ef8e57e56947c8ad690c227f5c9d7e561712", size = 2232274, upload-time = "2026-05-06T13:38:27.753Z" },

+    { url = "https://files.pythonhosted.org/packages/68/f0/92039db98b907ef49269a8271f67db9cb78ae2fc68062ef7e4e77adb5f61/pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:9401557acd873c3a7f3eb9383edef8ac4968f9510e340f4808d427e75667e7b4", size = 2309940, upload-time = "2026-05-06T13:38:05.353Z" },

+    { url = "https://files.pythonhosted.org/packages/5f/97/2aab507d3d00ca626e8e57c1eac6a79e4e5fbcc63eb99733ff55d1717f65/pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:926c9541b14b12b1681dca8a0b75feb510b06c6341b70a8e500c2fdcff837cce", size = 2094516, upload-time = "2026-05-06T13:39:10.577Z" },

+    { url = "https://files.pythonhosted.org/packages/22/37/a8aca44d40d737dde2bc05b3c6c07dff0de07ce6f82e9f3167aeaf4d5dea/pydantic_core-2.46.4-cp312-cp312-manylinux_2_31_riscv64.whl", hash = "sha256:56cb4851bcaf3d117eddcef4fe66afd750a50274b0da8e22be256d10e5611987", size = 2136854, upload-time = "2026-05-06T13:40:22.59Z" },

+    { url = "https://files.pythonhosted.org/packages/24/99/fcef1b79238c06a8cbec70819ac722ba76e02bc8ada9b0fd66eba40da01b/pydantic_core-2.46.4-cp312-cp312-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:c68fcd102d71ea85c5b2dfac3f4f8476eff42a9e078fd5faefff6d145063536b", size = 2180306, upload-time = "2026-05-06T13:40:10.666Z" },

+    { url = "https://files.pythonhosted.org/packages/ae/6c/fc44000918855b42779d007ae63b0532794739027b2f417321cddbc44f6a/pydantic_core-2.46.4-cp312-cp312-musllinux_1_1_aarch64.whl", hash = "sha256:b2f69dec1725e79a012d920df1707de5caf7ed5e08f3be4435e25803efc47458", size = 2190044, upload-time = "2026-05-06T13:40:43.231Z" },

+    { url = "https://files.pythonhosted.org/packages/6b/65/d9cadc9f1920d7a127ad2edba16c1db7916e59719285cd6c94600b0080ba/pydantic_core-2.46.4-cp312-cp312-musllinux_1_1_armv7l.whl", hash = "sha256:8d0820e8192167f80d88d64038e609c31452eeca865b4e1d9950a27a4609b00b", size = 2329133, upload-time = "2026-05-06T13:39:57.365Z" },

+    { url = "https://files.pythonhosted.org/packages/d0/cf/c873d91679f3a30bcf5e7ac280ce5573483e72295307685120d0d5ad3416/pydantic_core-2.46.4-cp312-cp312-musllinux_1_1_x86_64.whl", hash = "sha256:fbdb89b3e1c94a30cc5edfce477c6e6a5dc4d8f84665b455c27582f211a1c72c", size = 2374464, upload-time = "2026-05-06T13:38:06.976Z" },

+    { url = "https://files.pythonhosted.org/packages/47/bd/6f2fc8188f31bf10590f1e98e7b306336161fac930a8c514cd7bd828c7dc/pydantic_core-2.46.4-cp312-cp312-win32.whl", hash = "sha256:9aa768456404a8bf48a4406685ac2bec8e72b62c69313734fa3b73cf33b3a894", size = 1974823, upload-time = "2026-05-06T13:40:47.985Z" },

+    { url = "https://files.pythonhosted.org/packages/40/8c/985c1d41ea1107c2534abd9870e4ed5c8e7669b5c308297835c001e7a1c4/pydantic_core-2.46.4-cp312-cp312-win_amd64.whl", hash = "sha256:e9c26f834c65f5752f3f06cb08cb86a913ceb7274d0db6e267808a708b46bc89", size = 2072919, upload-time = "2026-05-06T13:39:21.153Z" },

+    { url = "https://files.pythonhosted.org/packages/c4/ba/f463d006e0c47373ca7ec5e1a261c59dc01ef4d62b2657af925fb0deee3a/pydantic_core-2.46.4-cp312-cp312-win_arm64.whl", hash = "sha256:4fc73cb559bdb54b1134a706a2802a4cddd27a0633f5abb7e53056268751ac6a", size = 2027604, upload-time = "2026-05-06T13:39:03.753Z" },

+    { url = "https://files.pythonhosted.org/packages/51/a2/5d30b469c5267a17b39dec53208222f76a8d351dfac4af661888c5aee77d/pydantic_core-2.46.4-cp313-cp313-macosx_10_12_x86_64.whl", hash = "sha256:5d5902252db0d3cedf8d4a1bc68f70eeb430f7e4c7104c8c476753519b423008", size = 2106306, upload-time = "2026-05-06T13:37:48.029Z" },

+    { url = "https://files.pythonhosted.org/packages/c1/81/4fa520eaffa8bd7d1525e644cd6d39e7d60b1592bc5b516693c7340b50f1/pydantic_core-2.46.4-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:c94f0688e7b8d0a67abf40e57a7eaaecd17cc9586706a31b76c031f63df052b4", size = 1951906, upload-time = "2026-05-06T13:37:17.012Z" },

+    { url = "https://files.pythonhosted.org/packages/03/d5/fd02da45b659668b05923b17ba3a0100a0a3d5541e3bd8fcc4ecb711309e/pydantic_core-2.46.4-cp313-cp313-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:f027324c56cd5406ca49c124b0db10e56c69064fec039acc571c29020cc87c76", size = 1976802, upload-time = "2026-05-06T13:37:35.113Z" },

+    { url = "https://files.pythonhosted.org/packages/21/f2/95727e1368be3d3ed485eaab7adbd7dda408f33f7a36e8b48e0144002b91/pydantic_core-2.46.4-cp313-cp313-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:e739fee756ba1010f8bcccb534252e85a35fe45ae92c295a06059ce58b74ccd3", size = 2052446, upload-time = "2026-05-06T13:37:12.313Z" },

+    { url = "https://files.pythonhosted.org/packages/9c/86/5d99feea3f77c7234b8718075b23db11532773c1a0dbd9b9490215dc2eeb/pydantic_core-2.46.4-cp313-cp313-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:9d56801be94b86a9da183e5f3766e6310752b99ff647e38b09a9500d88e46e76", size = 2232757, upload-time = "2026-05-06T13:39:01.149Z" },

+    { url = "https://files.pythonhosted.org/packages/d2/3a/508ac615935ef7588cf6d9e9b91309fdc2da751af865e02a9098de88258c/pydantic_core-2.46.4-cp313-cp313-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:2412e734dcb48da14d4e4006b82b46b74f2518b8a26ee7e58c6844a6cd6d03c4", size = 2309275, upload-time = "2026-05-06T13:37:41.406Z" },

+    { url = "https://files.pythonhosted.org/packages/07/f8/41db9de19d7987d6b04715a02b3b40aea467000275d9d758ffaa31af7d50/pydantic_core-2.46.4-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:9551187363ffc0de2a00b2e47c25aeaeb1020b69b668762966df15fc5659dd5a", size = 2094467, upload-time = "2026-05-06T13:39:18.847Z" },

+    { url = "https://files.pythonhosted.org/packages/2c/e2/f35033184cb11d0052daf4416e8e10a502ea2ac006fc4f459aee872727d1/pydantic_core-2.46.4-cp313-cp313-manylinux_2_31_riscv64.whl", hash = "sha256:0186750b482eefa11d7f435892b09c5c606193ef3375bcf94aa00ae6bfb66262", size = 2134417, upload-time = "2026-05-06T13:40:17.944Z" },

+    { url = "https://files.pythonhosted.org/packages/7e/7b/6ceeb1cc90e193862f444ebe373d8fdf613f0a82572dde03fb10734c6c71/pydantic_core-2.46.4-cp313-cp313-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:5855698a4856556d86e8e6cd8434bc3ac0314ee8e12089ae0e143f64c6256e4e", size = 2179782, upload-time = "2026-05-06T13:40:32.618Z" },

+    { url = "https://files.pythonhosted.org/packages/5a/f2/c8d7773ede6af08036423a00ae0ceffce266c3c52a096c435d68c896083f/pydantic_core-2.46.4-cp313-cp313-musllinux_1_1_aarch64.whl", hash = "sha256:cbaf13819775b7f769bf4a1f066cb6df7a28d4480081a589828ef190226881cd", size = 2188782, upload-time = "2026-05-06T13:36:51.018Z" },

+    { url = "https://files.pythonhosted.org/packages/59/31/0c864784e31f09f05cdd87606f08923b9c9e7f6e51dd27f20f62f975ce9f/pydantic_core-2.46.4-cp313-cp313-musllinux_1_1_armv7l.whl", hash = "sha256:633147d34cf4550417f12e2b1a0383973bdf5cdfde212cb09e9a581cf10820be", size = 2328334, upload-time = "2026-05-06T13:40:37.764Z" },

+    { url = "https://files.pythonhosted.org/packages/c2/eb/4f6c8a41efa30baa755590f4141abf3a8c370fab610915733e74134a7270/pydantic_core-2.46.4-cp313-cp313-musllinux_1_1_x86_64.whl", hash = "sha256:82cf5301172168103724d49a1444d3378cb20cdee30b116a1bd6031236298a5d", size = 2372986, upload-time = "2026-05-06T13:39:34.152Z" },

+    { url = "https://files.pythonhosted.org/packages/5b/24/b375a480d53113860c299764bfe9f349a3dc9108b3adc0d7f0d786492ebf/pydantic_core-2.46.4-cp313-cp313-win32.whl", hash = "sha256:9fa8ae11da9e2b3126c6426f147e0fba88d96d65921799bb30c6abd1cb2c97fb", size = 1973693, upload-time = "2026-05-06T13:37:55.072Z" },

+    { url = "https://files.pythonhosted.org/packages/7e/e8/cff247591966f2d22ec8c003cd7587e27b7ba7b81ab2fb888e3ab75dc285/pydantic_core-2.46.4-cp313-cp313-win_amd64.whl", hash = "sha256:6b3ace8194b0e5204818c92802dcdca7fc6d88aabbb799d7c795540d9cd6d292", size = 2071819, upload-time = "2026-05-06T13:38:49.139Z" },

+    { url = "https://files.pythonhosted.org/packages/c6/1a/f4aee670d5670e9e148e0c82c7db98d780be566c6e6a97ee8035528ca0b3/pydantic_core-2.46.4-cp313-cp313-win_arm64.whl", hash = "sha256:184c081504d17f1c1066e430e117142b2c77d9448a97f7b65c6ac9fd9aee238d", size = 2027411, upload-time = "2026-05-06T13:40:45.796Z" },

+    { url = "https://files.pythonhosted.org/packages/8d/74/228a26ddad29c6672b805d9fd78e8d251cd04004fa7eed0e622096cd0250/pydantic_core-2.46.4-cp314-cp314-macosx_10_12_x86_64.whl", hash = "sha256:428e04521a40150c85216fc8b85e8d39fece235a9cf5e383761238c7fa9b96fb", size = 2102079, upload-time = "2026-05-06T13:38:41.019Z" },

+    { url = "https://files.pythonhosted.org/packages/ad/1f/8970b150a4b4365623ae00fc88603491f763c627311ae8031e3111356d6e/pydantic_core-2.46.4-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:23ace664830ee0bfe014a0c7bc248b1f7f25ed7ad103852c317624a1083af462", size = 1952179, upload-time = "2026-05-06T13:36:59.812Z" },

+    { url = "https://files.pythonhosted.org/packages/95/30/5211a831ae054928054b2f79731661087a2bc5c01e825c672b3a4a8f1b3e/pydantic_core-2.46.4-cp314-cp314-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:ce5c1d2a8b27468f433ca974829c44060b8097eedc39933e3c206a90ee49c4a9", size = 1978926, upload-time = "2026-05-06T13:37:39.933Z" },

+    { url = "https://files.pythonhosted.org/packages/57/e9/689668733b1eb67adeef047db3c2e8788fcf65a7fd9c9e2b46b7744fe245/pydantic_core-2.46.4-cp314-cp314-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:7283d57845ecf5a163403eb0702dfc220cc4fbdd18919cb5ccea4f95ee1cdab4", size = 2046785, upload-time = "2026-05-06T13:38:01.995Z" },

+    { url = "https://files.pythonhosted.org/packages/60/d9/6715260422ff50a2109878fd24d948a6c3446bb2664f34ee78cd972b3acd/pydantic_core-2.46.4-cp314-cp314-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:8daafc69c93ee8a0204506a3b6b30f586ef54028f52aeeeb5c4cfc5184fd5914", size = 2228733, upload-time = "2026-05-06T13:40:50.371Z" },

+    { url = "https://files.pythonhosted.org/packages/18/ae/fdb2f64316afca925640f8e70bb1a564b0ec2721c1389e25b8eb4bf9a299/pydantic_core-2.46.4-cp314-cp314-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:cd2213145bcc2ba85884d0ac63d222fece9209678f77b9b4d76f054c561adb28", size = 2307534, upload-time = "2026-05-06T13:37:21.531Z" },

+    { url = "https://files.pythonhosted.org/packages/89/1d/8eff589b45bb8190a9d12c49cfad0f176a5cbd1534908a6b5125e2886239/pydantic_core-2.46.4-cp314-cp314-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:7a5f930472650a82629163023e630d160863fce524c616f4e5186e5de9d9a49b", size = 2099732, upload-time = "2026-05-06T13:39:31.942Z" },

+    { url = "https://files.pythonhosted.org/packages/06/d5/ee5a3366637fee41dee51a1fc91562dcf12ddbc68fda34e6b253da2324bb/pydantic_core-2.46.4-cp314-cp314-manylinux_2_31_riscv64.whl", hash = "sha256:c1b3f518abeca3aa13c712fd202306e145abf59a18b094a6bafb2d2bbf59192c", size = 2129627, upload-time = "2026-05-06T13:37:25.033Z" },

+    { url = "https://files.pythonhosted.org/packages/94/33/2414be571d2c6a6c4d08be21f9292b6d3fdb08949a97b6dfe985017821db/pydantic_core-2.46.4-cp314-cp314-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:1a7dd0b3ee80d90150e3495a3a13ac34dbcbfd4f012996a6a1d8900e91b5c0fb", size = 2179141, upload-time = "2026-05-06T13:37:14.046Z" },

+    { url = "https://files.pythonhosted.org/packages/7b/79/7daa95be995be0eecc4cf75064cb33f9bbbfe3fe0158caf2f0d4a996a5c7/pydantic_core-2.46.4-cp314-cp314-musllinux_1_1_aarch64.whl", hash = "sha256:3fb702cd90b0446a3a1c5e470bfa0dd23c0233b676a9099ddcc964fa6ca13898", size = 2184325, upload-time = "2026-05-06T13:36:53.615Z" },

+    { url = "https://files.pythonhosted.org/packages/9f/cb/d0a382f5c0de8a222dc61c65348e0ce831b1f68e0a018450d31c2cace3a5/pydantic_core-2.46.4-cp314-cp314-musllinux_1_1_armv7l.whl", hash = "sha256:b8458003118a712e66286df6a707db01c52c0f52f7db8e4a38f0da1d3b94fc4e", size = 2323990, upload-time = "2026-05-06T13:40:29.971Z" },

+    { url = "https://files.pythonhosted.org/packages/05/db/d9ba624cc4a5aced1598e88c04fdbd8310c8a69b9d38b9a3d39ce3a61ed7/pydantic_core-2.46.4-cp314-cp314-musllinux_1_1_x86_64.whl", hash = "sha256:372429a130e469c9cd698925ce5fc50940b7a1336b0d82038e63d5bbc4edc519", size = 2369978, upload-time = "2026-05-06T13:37:23.027Z" },

+    { url = "https://files.pythonhosted.org/packages/f2/20/d15df15ba918c423461905802bfd2981c3af0bfa0e40d05e13edbfa48bc3/pydantic_core-2.46.4-cp314-cp314-win32.whl", hash = "sha256:85bb3611ff1802f3ee7fdd7dbff26b56f343fb432d57a4728fdd49b6ef35e2f4", size = 1966354, upload-time = "2026-05-06T13:38:03.499Z" },

+    { url = "https://files.pythonhosted.org/packages/fc/b6/6b8de4c0a7d7ab3004c439c80c5c1e0a3e8d78bbae19379b01960383d9e5/pydantic_core-2.46.4-cp314-cp314-win_amd64.whl", hash = "sha256:811ff8e9c313ab425368bcbb36e5c4ebd7108c2bbf4e4089cfbb0b01eff63fac", size = 2072238, upload-time = "2026-05-06T13:39:40.807Z" },

+    { url = "https://files.pythonhosted.org/packages/32/36/51eb763beec1f4cf59b1db243a7dcc39cbb41230f050a09b9d69faaf0a48/pydantic_core-2.46.4-cp314-cp314-win_arm64.whl", hash = "sha256:bfec22eab3c8cc2ceec0248aec886624116dc079afa027ecc8ad4a7e62010f8a", size = 2018251, upload-time = "2026-05-06T13:37:26.72Z" },

+    { url = "https://files.pythonhosted.org/packages/e8/91/855af51d625b23aa987116a19e231d2aaef9c4a415273ddc189b79a45fee/pydantic_core-2.46.4-cp314-cp314t-macosx_10_12_x86_64.whl", hash = "sha256:af8244b2bef6aaad6d92cda81372de7f8c8d36c9f0c3ea36e827c60e7d9467a0", size = 2099593, upload-time = "2026-05-06T13:39:47.682Z" },

+    { url = "https://files.pythonhosted.org/packages/fb/1b/8784a54c65edb5f49f0a14d6977cf1b209bba85a4c77445b255c2de58ab3/pydantic_core-2.46.4-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:5a4330cdbc57162e4b3aa303f588ba752257694c9c9be3e7ebb11b4aca659b5d", size = 1935226, upload-time = "2026-05-06T13:40:40.428Z" },

+    { url = "https://files.pythonhosted.org/packages/e8/e7/1955d28d1afc56dd4b3ad7cc0cf39df1b9852964cf16e5d13912756d6d6b/pydantic_core-2.46.4-cp314-cp314t-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:29c61fc04a3d840155ff08e475a04809278972fe6aef51e2720554e96367e34b", size = 1974605, upload-time = "2026-05-06T13:37:32.029Z" },

+    { url = "https://files.pythonhosted.org/packages/93/e2/3fedbf0ba7a22850e6e9fd78117f1c0f10f950182344d8a6c535d468fdd8/pydantic_core-2.46.4-cp314-cp314t-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:c50f2528cf200c5eed56faf3f4e22fcd5f38c157a8b78576e6ba3168ec35f000", size = 2030777, upload-time = "2026-05-06T13:38:55.239Z" },

+    { url = "https://files.pythonhosted.org/packages/f8/61/46be275fcaaba0b4f5b9669dd852267ce1ff616592dccf7a7845588df091/pydantic_core-2.46.4-cp314-cp314t-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:0cbe8b01f948de4286c74cdd6c667aceb38f5c1e26f0693b3983d9d74887c65e", size = 2236641, upload-time = "2026-05-06T13:37:08.096Z" },

+    { url = "https://files.pythonhosted.org/packages/60/db/12e93e46a8bac9988be3c016860f83293daea8c716c029c9ace279036f2f/pydantic_core-2.46.4-cp314-cp314t-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:617d7e2ca7dcb8c5cf6bcb8c59b8832c94b36196bbf1cbd1bfb56ed341905edd", size = 2286404, upload-time = "2026-05-06T13:40:20.221Z" },

+    { url = "https://files.pythonhosted.org/packages/e2/4a/4d8b19008f38d31c53b8219cfedc2e3d5de5fe99d90076b7e767de29274f/pydantic_core-2.46.4-cp314-cp314t-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:7027560ee92211647d0d34e3f7cd6f50da56399d26a9c8ad0da286d3869a53f3", size = 2109219, upload-time = "2026-05-06T13:38:12.153Z" },

+    { url = "https://files.pythonhosted.org/packages/88/70/3cbc40978fefb7bb09c6708d40d4ad1a5d70fd7213c3d17f971de868ec1f/pydantic_core-2.46.4-cp314-cp314t-manylinux_2_31_riscv64.whl", hash = "sha256:f99626688942fb746e545232e7726926f3be91b5975f8b55327665fafda991c7", size = 2110594, upload-time = "2026-05-06T13:40:02.971Z" },

+    { url = "https://files.pythonhosted.org/packages/9d/20/b8d36736216e29491125531685b2f9e61aa5b4b2599893f8268551da3338/pydantic_core-2.46.4-cp314-cp314t-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:fc3e9034a63de20e15e8ade85358bc6efc614008cab72898b4b4952bea0509ff", size = 2159542, upload-time = "2026-05-06T13:39:27.506Z" },

+    { url = "https://files.pythonhosted.org/packages/1d/a2/367df868eb584dacf6bf82a389272406d7178e301c4ac82545ab98bc2dd9/pydantic_core-2.46.4-cp314-cp314t-musllinux_1_1_aarch64.whl", hash = "sha256:97e7cf2be5c77b7d1a9713a05605d49460d02c6078d38d8bef3cbe323c548424", size = 2168146, upload-time = "2026-05-06T13:38:31.93Z" },

+    { url = "https://files.pythonhosted.org/packages/c1/b8/4460f77f7e201893f649a29ab355dddd3beee8a97bcb1a320db414f9a06e/pydantic_core-2.46.4-cp314-cp314t-musllinux_1_1_armv7l.whl", hash = "sha256:3bf92c5d0e00fefaab325a4d27828fe6b6e2a21848686b5b60d2d9eeb09d76c6", size = 2306309, upload-time = "2026-05-06T13:37:44.717Z" },

+    { url = "https://files.pythonhosted.org/packages/64/c4/be2639293acd87dc8ddbcec41a73cee9b2ebf996fe6d892a1a74e88ad3f7/pydantic_core-2.46.4-cp314-cp314t-musllinux_1_1_x86_64.whl", hash = "sha256:3ecbc122d18468d06ca279dc26a8c2e2d5acb10943bb35e36ae92096dc3b5565", size = 2369736, upload-time = "2026-05-06T13:37:05.645Z" },

+    { url = "https://files.pythonhosted.org/packages/30/a6/9f9f380dbb301f67023bf8f707aaa75daadf84f7152d95c410fd7e81d994/pydantic_core-2.46.4-cp314-cp314t-win32.whl", hash = "sha256:e846ae7835bf0703ae43f534ab79a867146dadd59dc9ca5c8b53d5c8f7c9ef02", size = 1955575, upload-time = "2026-05-06T13:38:51.116Z" },

+    { url = "https://files.pythonhosted.org/packages/40/1f/f1eb9eb350e795d1af8586289746f5c5677d16043040d63710e22abc43c9/pydantic_core-2.46.4-cp314-cp314t-win_amd64.whl", hash = "sha256:2108ba5c1c1eca18030634489dc544844144ee36357f2f9f780b93e7ddbb44b5", size = 2051624, upload-time = "2026-05-06T13:38:21.672Z" },

+    { url = "https://files.pythonhosted.org/packages/f6/d2/42dd53d0a85c27606f316d3aa5d2869c4e8470a5ed6dec30e4a1abe19192/pydantic_core-2.46.4-cp314-cp314t-win_arm64.whl", hash = "sha256:4fcbe087dbc2068af7eda3aa87634eba216dbda64d1ae73c8684b621d33f6596", size = 2017325, upload-time = "2026-05-06T13:40:52.723Z" },

+    { url = "https://files.pythonhosted.org/packages/ee/a4/73995fd4ebbb46ba0ee51e6fa049b8f02c40daebb762208feda8a6b7894d/pydantic_core-2.46.4-graalpy311-graalpy242_311_native-macosx_10_12_x86_64.whl", hash = "sha256:14d4edf427bdcf950a8a02d7cb44a08614388dd6e1bdcbf4f67504fa7887da9c", size = 2111589, upload-time = "2026-05-06T13:37:10.817Z" },

+    { url = "https://files.pythonhosted.org/packages/fb/7f/f37d3a5e8bfcc2e403f5c57a730f2d815693fb42119e8ea48b3789335af1/pydantic_core-2.46.4-graalpy311-graalpy242_311_native-macosx_11_0_arm64.whl", hash = "sha256:0ce40cd7b21210e99342afafbd4d0f76d784eb5b1d60f3bdc566be4983c6c73b", size = 1944552, upload-time = "2026-05-06T13:36:56.717Z" },

+    { url = "https://files.pythonhosted.org/packages/15/3c/d7eb777b3ff43e8433a4efb39a17aa8fd98a4ee8561a24a67ef5db07b2d6/pydantic_core-2.46.4-graalpy311-graalpy242_311_native-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:90884113d8b48f760e9587002789ddd741e76ab9f89518cd1e43b1f1a52ec44b", size = 1982984, upload-time = "2026-05-06T13:39:06.207Z" },

+    { url = "https://files.pythonhosted.org/packages/63/87/70b9f40170a81afd55ca26c9b2acb25c20d64bcfbf888fafecb3ba077d4c/pydantic_core-2.46.4-graalpy311-graalpy242_311_native-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:66ce7632c22d837c95301830e111ad0128a32b8207533b60896a96c4915192ea", size = 2138417, upload-time = "2026-05-06T13:39:45.476Z" },

+    { url = "https://files.pythonhosted.org/packages/9d/1d/8987ad40f65ae1432753072f214fb5c74fe47ffbd0698bb9cbbb585664f8/pydantic_core-2.46.4-graalpy312-graalpy250_312_native-macosx_10_12_x86_64.whl", hash = "sha256:1d8ba486450b14f3b1d63bc521d410ec7565e52f887b9fb671791886436a42f7", size = 2095527, upload-time = "2026-05-06T13:39:52.283Z" },

+    { url = "https://files.pythonhosted.org/packages/64/d3/84c282a7eee1d3ac4c0377546ef5a1ea436ce26840d9ac3b7ed54a377507/pydantic_core-2.46.4-graalpy312-graalpy250_312_native-macosx_11_0_arm64.whl", hash = "sha256:3009f12e4e90b7f88b4f9adb1b0c4a3d58fe7820f3238c190047209d148026df", size = 1936024, upload-time = "2026-05-06T13:40:15.671Z" },

+    { url = "https://files.pythonhosted.org/packages/d7/ca/eac61596cdeb4d7e174d3dc0bd8a6238f14f75f97a24e7b7db4c7e7340a0/pydantic_core-2.46.4-graalpy312-graalpy250_312_native-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:ad785e92e6dc634c21555edc8bd6b64957ab844541bcb96a1366c202951ae526", size = 1990696, upload-time = "2026-05-06T13:38:34.717Z" },

+    { url = "https://files.pythonhosted.org/packages/fa/c3/7c8b240552251faf6b3a957db200fcfbbcec36763c050428b601e0c9b83b/pydantic_core-2.46.4-graalpy312-graalpy250_312_native-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:00c603d540afdd6b80eb39f078f33ebd46211f02f33e34a32d9f053bba711de0", size = 2147590, upload-time = "2026-05-06T13:39:29.883Z" },

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

+    { url = "https://files.pythonhosted.org/packages/8d/ab/9893ea9fb066be70ed9074ae543914a618c131ed8dff2da1e08b3a4df4db/pyproj-3.7.2-cp312-cp312-macosx_13_0_x86_64.whl", hash = "sha256:0a9bb26a6356fb5b033433a6d1b4542158fb71e3c51de49b4c318a1dff3aeaab", size = 6219832, upload-time = "2025-08-14T12:04:10.264Z" },

+    { url = "https://files.pythonhosted.org/packages/53/78/4c64199146eed7184eb0e85bedec60a4aa8853b6ffe1ab1f3a8b962e70a0/pyproj-3.7.2-cp312-cp312-macosx_14_0_arm64.whl", hash = "sha256:567caa03021178861fad27fabde87500ec6d2ee173dd32f3e2d9871e40eebd68", size = 4620650, upload-time = "2025-08-14T12:04:11.978Z" },

+    { url = "https://files.pythonhosted.org/packages/b6/ac/14a78d17943898a93ef4f8c6a9d4169911c994e3161e54a7cedeba9d8dde/pyproj-3.7.2-cp312-cp312-manylinux_2_28_aarch64.whl", hash = "sha256:c203101d1dc3c038a56cff0447acc515dd29d6e14811406ac539c21eed422b2a", size = 9667087, upload-time = "2025-08-14T12:04:13.964Z" },

+    { url = "https://files.pythonhosted.org/packages/b8/be/212882c450bba74fc8d7d35cbd57e4af84792f0a56194819d98106b075af/pyproj-3.7.2-cp312-cp312-manylinux_2_28_x86_64.whl", hash = "sha256:1edc34266c0c23ced85f95a1ee8b47c9035eae6aca5b6b340327250e8e281630", size = 9552797, upload-time = "2025-08-14T12:04:16.624Z" },

+    { url = "https://files.pythonhosted.org/packages/ba/c0/c0f25c87b5d2a8686341c53c1792a222a480d6c9caf60311fec12c99ec26/pyproj-3.7.2-cp312-cp312-musllinux_1_2_aarch64.whl", hash = "sha256:aa9f26c21bc0e2dc3d224cb1eb4020cf23e76af179a7c66fea49b828611e4260", size = 10837036, upload-time = "2025-08-14T12:04:18.733Z" },

+    { url = "https://files.pythonhosted.org/packages/5d/37/5cbd6772addde2090c91113332623a86e8c7d583eccb2ad02ea634c4a89f/pyproj-3.7.2-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:f9428b318530625cb389b9ddc9c51251e172808a4af79b82809376daaeabe5e9", size = 10775952, upload-time = "2025-08-14T12:04:20.709Z" },

+    { url = "https://files.pythonhosted.org/packages/69/a1/dc250e3cf83eb4b3b9a2cf86fdb5e25288bd40037ae449695550f9e96b2f/pyproj-3.7.2-cp312-cp312-win32.whl", hash = "sha256:b3d99ed57d319da042f175f4554fc7038aa4bcecc4ac89e217e350346b742c9d", size = 5898872, upload-time = "2025-08-14T12:04:22.485Z" },

+    { url = "https://files.pythonhosted.org/packages/4a/a6/6fe724b72b70f2b00152d77282e14964d60ab092ec225e67c196c9b463e5/pyproj-3.7.2-cp312-cp312-win_amd64.whl", hash = "sha256:11614a054cd86a2ed968a657d00987a86eeb91fdcbd9ad3310478685dc14a128", size = 6312176, upload-time = "2025-08-14T12:04:24.736Z" },

+    { url = "https://files.pythonhosted.org/packages/5d/68/915cc32c02a91e76d02c8f55d5a138d6ef9e47a0d96d259df98f4842e558/pyproj-3.7.2-cp312-cp312-win_arm64.whl", hash = "sha256:509a146d1398bafe4f53273398c3bb0b4732535065fa995270e52a9d3676bca3", size = 6233452, upload-time = "2025-08-14T12:04:27.287Z" },

+    { url = "https://files.pythonhosted.org/packages/be/14/faf1b90d267cea68d7e70662e7f88cefdb1bc890bd596c74b959e0517a72/pyproj-3.7.2-cp313-cp313-macosx_13_0_x86_64.whl", hash = "sha256:19466e529b1b15eeefdf8ff26b06fa745856c044f2f77bf0edbae94078c1dfa1", size = 6214580, upload-time = "2025-08-14T12:04:28.804Z" },

+    { url = "https://files.pythonhosted.org/packages/35/48/da9a45b184d375f62667f62eba0ca68569b0bd980a0bb7ffcc1d50440520/pyproj-3.7.2-cp313-cp313-macosx_14_0_arm64.whl", hash = "sha256:c79b9b84c4a626c5dc324c0d666be0bfcebd99f7538d66e8898c2444221b3da7", size = 4615388, upload-time = "2025-08-14T12:04:30.553Z" },

+    { url = "https://files.pythonhosted.org/packages/5e/e7/d2b459a4a64bca328b712c1b544e109df88e5c800f7c143cfbc404d39bfb/pyproj-3.7.2-cp313-cp313-manylinux_2_28_aarch64.whl", hash = "sha256:ceecf374cacca317bc09e165db38ac548ee3cad07c3609442bd70311c59c21aa", size = 9628455, upload-time = "2025-08-14T12:04:32.435Z" },

+    { url = "https://files.pythonhosted.org/packages/f8/85/c2b1706e51942de19076eff082f8495e57d5151364e78b5bef4af4a1d94a/pyproj-3.7.2-cp313-cp313-manylinux_2_28_x86_64.whl", hash = "sha256:5141a538ffdbe4bfd157421828bb2e07123a90a7a2d6f30fa1462abcfb5ce681", size = 9514269, upload-time = "2025-08-14T12:04:34.599Z" },

+    { url = "https://files.pythonhosted.org/packages/34/38/07a9b89ae7467872f9a476883a5bad9e4f4d1219d31060f0f2b282276cbe/pyproj-3.7.2-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:f000841e98ea99acbb7b8ca168d67773b0191de95187228a16110245c5d954d5", size = 10808437, upload-time = "2025-08-14T12:04:36.485Z" },

+    { url = "https://files.pythonhosted.org/packages/12/56/fda1daeabbd39dec5b07f67233d09f31facb762587b498e6fc4572be9837/pyproj-3.7.2-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:8115faf2597f281a42ab608ceac346b4eb1383d3b45ab474fd37341c4bf82a67", size = 10745540, upload-time = "2025-08-14T12:04:38.568Z" },

+    { url = "https://files.pythonhosted.org/packages/0d/90/c793182cbba65a39a11db2ac6b479fe76c59e6509ae75e5744c344a0da9d/pyproj-3.7.2-cp313-cp313-win32.whl", hash = "sha256:f18c0579dd6be00b970cb1a6719197fceecc407515bab37da0066f0184aafdf3", size = 5896506, upload-time = "2025-08-14T12:04:41.059Z" },

+    { url = "https://files.pythonhosted.org/packages/be/0f/747974129cf0d800906f81cd25efd098c96509026e454d4b66868779ab04/pyproj-3.7.2-cp313-cp313-win_amd64.whl", hash = "sha256:bb41c29d5f60854b1075853fe80c58950b398d4ebb404eb532536ac8d2834ed7", size = 6310195, upload-time = "2025-08-14T12:04:42.974Z" },

+    { url = "https://files.pythonhosted.org/packages/82/64/fc7598a53172c4931ec6edf5228280663063150625d3f6423b4c20f9daff/pyproj-3.7.2-cp313-cp313-win_arm64.whl", hash = "sha256:2b617d573be4118c11cd96b8891a0b7f65778fa7733ed8ecdb297a447d439100", size = 6230748, upload-time = "2025-08-14T12:04:44.491Z" },

+    { url = "https://files.pythonhosted.org/packages/aa/f0/611dd5cddb0d277f94b7af12981f56e1441bf8d22695065d4f0df5218498/pyproj-3.7.2-cp313-cp313t-macosx_13_0_x86_64.whl", hash = "sha256:d27b48f0e81beeaa2b4d60c516c3a1cfbb0c7ff6ef71256d8e9c07792f735279", size = 6241729, upload-time = "2025-08-14T12:04:46.274Z" },

+    { url = "https://files.pythonhosted.org/packages/15/93/40bd4a6c523ff9965e480870611aed7eda5aa2c6128c6537345a2b77b542/pyproj-3.7.2-cp313-cp313t-macosx_14_0_arm64.whl", hash = "sha256:55a3610d75023c7b1c6e583e48ef8f62918e85a2ae81300569d9f104d6684bb6", size = 4652497, upload-time = "2025-08-14T12:04:48.203Z" },

+    { url = "https://files.pythonhosted.org/packages/1b/ae/7150ead53c117880b35e0d37960d3138fe640a235feb9605cb9386f50bb0/pyproj-3.7.2-cp313-cp313t-manylinux_2_28_aarch64.whl", hash = "sha256:8d7349182fa622696787cc9e195508d2a41a64765da9b8a6bee846702b9e6220", size = 9942610, upload-time = "2025-08-14T12:04:49.652Z" },

+    { url = "https://files.pythonhosted.org/packages/d8/17/7a4a7eafecf2b46ab64e5c08176c20ceb5844b503eaa551bf12ccac77322/pyproj-3.7.2-cp313-cp313t-manylinux_2_28_x86_64.whl", hash = "sha256:d230b186eb876ed4f29a7c5ee310144c3a0e44e89e55f65fb3607e13f6db337c", size = 9692390, upload-time = "2025-08-14T12:04:51.731Z" },

+    { url = "https://files.pythonhosted.org/packages/c3/55/ae18f040f6410f0ea547a21ada7ef3e26e6c82befa125b303b02759c0e9d/pyproj-3.7.2-cp313-cp313t-musllinux_1_2_aarch64.whl", hash = "sha256:237499c7862c578d0369e2b8ac56eec550e391a025ff70e2af8417139dabb41c", size = 11047596, upload-time = "2025-08-14T12:04:53.748Z" },

+    { url = "https://files.pythonhosted.org/packages/e6/2e/d3fff4d2909473f26ae799f9dda04caa322c417a51ff3b25763f7d03b233/pyproj-3.7.2-cp313-cp313t-musllinux_1_2_x86_64.whl", hash = "sha256:8c225f5978abd506fd9a78eaaf794435e823c9156091cabaab5374efb29d7f69", size = 10896975, upload-time = "2025-08-14T12:04:55.875Z" },

+    { url = "https://files.pythonhosted.org/packages/f2/bc/8fc7d3963d87057b7b51ebe68c1e7c51c23129eee5072ba6b86558544a46/pyproj-3.7.2-cp313-cp313t-win32.whl", hash = "sha256:2da731876d27639ff9d2d81c151f6ab90a1546455fabd93368e753047be344a2", size = 5953057, upload-time = "2025-08-14T12:04:58.466Z" },

+    { url = "https://files.pythonhosted.org/packages/cc/27/ea9809966cc47d2d51e6d5ae631ea895f7c7c7b9b3c29718f900a8f7d197/pyproj-3.7.2-cp313-cp313t-win_amd64.whl", hash = "sha256:f54d91ae18dd23b6c0ab48126d446820e725419da10617d86a1b69ada6d881d3", size = 6375414, upload-time = "2025-08-14T12:04:59.861Z" },

+    { url = "https://files.pythonhosted.org/packages/5b/f8/1ef0129fba9a555c658e22af68989f35e7ba7b9136f25758809efec0cd6e/pyproj-3.7.2-cp313-cp313t-win_arm64.whl", hash = "sha256:fc52ba896cfc3214dc9f9ca3c0677a623e8fdd096b257c14a31e719d21ff3fdd", size = 6262501, upload-time = "2025-08-14T12:05:01.39Z" },

+    { url = "https://files.pythonhosted.org/packages/42/17/c2b050d3f5b71b6edd0d96ae16c990fdc42a5f1366464a5c2772146de33a/pyproj-3.7.2-cp314-cp314-macosx_13_0_x86_64.whl", hash = "sha256:2aaa328605ace41db050d06bac1adc11f01b71fe95c18661497763116c3a0f02", size = 6214541, upload-time = "2025-08-14T12:05:03.166Z" },

+    { url = "https://files.pythonhosted.org/packages/03/68/68ada9c8aea96ded09a66cfd9bf87aa6db8c2edebe93f5bf9b66b0143fbc/pyproj-3.7.2-cp314-cp314-macosx_14_0_arm64.whl", hash = "sha256:35dccbce8201313c596a970fde90e33605248b66272595c061b511c8100ccc08", size = 4617456, upload-time = "2025-08-14T12:05:04.563Z" },

+    { url = "https://files.pythonhosted.org/packages/81/e4/4c50ceca7d0e937977866b02cb64e6ccf4df979a5871e521f9e255df6073/pyproj-3.7.2-cp314-cp314-manylinux_2_28_aarch64.whl", hash = "sha256:25b0b7cb0042444c29a164b993c45c1b8013d6c48baa61dc1160d834a277e83b", size = 9615590, upload-time = "2025-08-14T12:05:06.094Z" },

+    { url = "https://files.pythonhosted.org/packages/05/1e/ada6fb15a1d75b5bd9b554355a69a798c55a7dcc93b8d41596265c1772e3/pyproj-3.7.2-cp314-cp314-manylinux_2_28_x86_64.whl", hash = "sha256:85def3a6388e9ba51f964619aa002a9d2098e77c6454ff47773bb68871024281", size = 9474960, upload-time = "2025-08-14T12:05:07.973Z" },

+    { url = "https://files.pythonhosted.org/packages/51/07/9d48ad0a8db36e16f842f2c8a694c1d9d7dcf9137264846bef77585a71f3/pyproj-3.7.2-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:b1bccefec3875ab81eabf49059e2b2ea77362c178b66fd3528c3e4df242f1516", size = 10799478, upload-time = "2025-08-14T12:05:14.102Z" },

+    { url = "https://files.pythonhosted.org/packages/85/cf/2f812b529079f72f51ff2d6456b7fef06c01735e5cfd62d54ffb2b548028/pyproj-3.7.2-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:d5371ca114d6990b675247355a801925814eca53e6c4b2f1b5c0a956336ee36e", size = 10710030, upload-time = "2025-08-14T12:05:16.317Z" },

+    { url = "https://files.pythonhosted.org/packages/99/9b/4626a19e1f03eba4c0e77b91a6cf0f73aa9cb5d51a22ee385c22812bcc2c/pyproj-3.7.2-cp314-cp314-win32.whl", hash = "sha256:77f066626030f41be543274f5ac79f2a511fe89860ecd0914f22131b40a0ec25", size = 5991181, upload-time = "2025-08-14T12:05:19.492Z" },

+    { url = "https://files.pythonhosted.org/packages/04/b2/5a6610554306a83a563080c2cf2c57565563eadd280e15388efa00fb5b33/pyproj-3.7.2-cp314-cp314-win_amd64.whl", hash = "sha256:5a964da1696b8522806f4276ab04ccfff8f9eb95133a92a25900697609d40112", size = 6434721, upload-time = "2025-08-14T12:05:21.022Z" },

+    { url = "https://files.pythonhosted.org/packages/ae/ce/6c910ea2e1c74ef673c5d48c482564b8a7824a44c4e35cca2e765b68cfcc/pyproj-3.7.2-cp314-cp314-win_arm64.whl", hash = "sha256:e258ab4dbd3cf627809067c0ba8f9884ea76c8e5999d039fb37a1619c6c3e1f6", size = 6363821, upload-time = "2025-08-14T12:05:22.627Z" },

+    { url = "https://files.pythonhosted.org/packages/e4/e4/5532f6f7491812ba782a2177fe9de73fd8e2912b59f46a1d056b84b9b8f2/pyproj-3.7.2-cp314-cp314t-macosx_13_0_x86_64.whl", hash = "sha256:bbbac2f930c6d266f70ec75df35ef851d96fdb3701c674f42fd23a9314573b37", size = 6241773, upload-time = "2025-08-14T12:05:24.577Z" },

+    { url = "https://files.pythonhosted.org/packages/20/1f/0938c3f2bbbef1789132d1726d9b0e662f10cfc22522743937f421ad664e/pyproj-3.7.2-cp314-cp314t-macosx_14_0_arm64.whl", hash = "sha256:b7544e0a3d6339dc9151e9c8f3ea62a936ab7cc446a806ec448bbe86aebb979b", size = 4652537, upload-time = "2025-08-14T12:05:26.391Z" },

+    { url = "https://files.pythonhosted.org/packages/c7/a8/488b1ed47d25972f33874f91f09ca8f2227902f05f63a2b80dc73e7b1c97/pyproj-3.7.2-cp314-cp314t-manylinux_2_28_aarch64.whl", hash = "sha256:f7f5133dca4c703e8acadf6f30bc567d39a42c6af321e7f81975c2518f3ed357", size = 9940864, upload-time = "2025-08-14T12:05:27.985Z" },

+    { url = "https://files.pythonhosted.org/packages/c7/cc/7f4c895d0cb98e47b6a85a6d79eaca03eb266129eed2f845125c09cf31ff/pyproj-3.7.2-cp314-cp314t-manylinux_2_28_x86_64.whl", hash = "sha256:5aff3343038d7426aa5076f07feb88065f50e0502d1b0d7c22ddfdd2c75a3f81", size = 9688868, upload-time = "2025-08-14T12:05:30.425Z" },

+    { url = "https://files.pythonhosted.org/packages/b2/b7/c7e306b8bb0f071d9825b753ee4920f066c40fbfcce9372c4f3cfb2fc4ed/pyproj-3.7.2-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:b0552178c61f2ac1c820d087e8ba6e62b29442debddbb09d51c4bf8acc84d888", size = 11045910, upload-time = "2025-08-14T12:05:32.507Z" },

+    { url = "https://files.pythonhosted.org/packages/42/fb/538a4d2df695980e2dde5c04d965fbdd1fe8c20a3194dc4aaa3952a4d1be/pyproj-3.7.2-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:47d87db2d2c436c5fd0409b34d70bb6cdb875cca2ebe7a9d1c442367b0ab8d59", size = 10895724, upload-time = "2025-08-14T12:05:35.465Z" },

+    { url = "https://files.pythonhosted.org/packages/e8/8b/a3f0618b03957de9db5489a04558a8826f43906628bb0b766033aa3b5548/pyproj-3.7.2-cp314-cp314t-win32.whl", hash = "sha256:c9b6f1d8ad3e80a0ee0903a778b6ece7dca1d1d40f6d114ae01bc8ddbad971aa", size = 6056848, upload-time = "2025-08-14T12:05:37.553Z" },

+    { url = "https://files.pythonhosted.org/packages/bc/56/413240dd5149dd3291eda55aa55a659da4431244a2fd1319d0ae89407cfb/pyproj-3.7.2-cp314-cp314t-win_amd64.whl", hash = "sha256:1914e29e27933ba6f9822663ee0600f169014a2859f851c054c88cf5ea8a333c", size = 6517676, upload-time = "2025-08-14T12:05:39.126Z" },

+    { url = "https://files.pythonhosted.org/packages/15/73/a7141a1a0559bf1a7aa42a11c879ceb19f02f5c6c371c6d57fd86cefd4d1/pyproj-3.7.2-cp314-cp314t-win_arm64.whl", hash = "sha256:d9d25bae416a24397e0d85739f84d323b55f6511e45a522dd7d7eae70d10c7e4", size = 6391844, upload-time = "2025-08-14T12:05:40.745Z" },

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

+resolution-markers = [

+    "python_full_version < '3.12'",

+]

+dependencies = [

+    { name = "affine", marker = "python_full_version < '3.12'" },

+    { name = "attrs", marker = "python_full_version < '3.12'" },

+    { name = "certifi", marker = "python_full_version < '3.12'" },

+    { name = "click", marker = "python_full_version < '3.12'" },

+    { name = "click-plugins", marker = "python_full_version < '3.12'" },

+    { name = "cligj", marker = "python_full_version < '3.12'" },

+    { name = "numpy", marker = "python_full_version < '3.12'" },

+    { name = "pyparsing", marker = "python_full_version < '3.12'" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/ec/fa/fce8dc9f09e5bc6520b6fc1b4ecfa510af9ca06eb42ad7bdff9c9b8989d0/rasterio-1.4.4.tar.gz", hash = "sha256:c95424e2c7f009b8f7df1095d645c52895cd332c0c2e1b4c2e073ea28b930320", size = 445004, upload-time = "2025-12-12T18:01:08.971Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/c6/0d/d3859e49ab94464de2623fec82c6798d8d7c8bea2473cd2696fc5e09f717/rasterio-1.4.4-cp311-cp311-macosx_14_0_arm64.whl", hash = "sha256:b8eea428b5f0c78a963f6003a19b60777df83a0aba8c28231d65431e32ac160e", size = 21144125, upload-time = "2025-12-12T17:58:59.511Z" },

+    { url = "https://files.pythonhosted.org/packages/aa/3c/97ba4b146309cdc0e36f289b02ac69465b026a21afc828e4e4e1dc39466a/rasterio-1.4.4-cp311-cp311-macosx_15_0_x86_64.whl", hash = "sha256:1cc0ea5aa0d22f5f349aa221674481de689b7b3a99607ce6bb58a29e5be54d17", size = 25746406, upload-time = "2025-12-12T17:59:02.902Z" },

+    { url = "https://files.pythonhosted.org/packages/ce/33/75f81bd837ac2336b24456fdb249597a4b9af2a212b7151f64d09022be36/rasterio-1.4.4-cp311-cp311-manylinux_2_28_aarch64.whl", hash = "sha256:7eb25b23666b29dadfc49a59206cead62c99190584b61771bba0e95f7da06801", size = 34587242, upload-time = "2025-12-12T17:59:05.848Z" },

+    { url = "https://files.pythonhosted.org/packages/f9/77/3869a426f6e752dde13f3868cdf16253ca0214f92107db79c1583c9aa07b/rasterio-1.4.4-cp311-cp311-manylinux_2_28_x86_64.whl", hash = "sha256:e24b7b8c2df801dde2a1dffb44c58902bd76b5cab740dc11de4ff9963992a71a", size = 35881871, upload-time = "2025-12-12T17:59:09.779Z" },

+    { url = "https://files.pythonhosted.org/packages/66/d0/3818859ddbd3750d0ef5a6580a3272e81764286d943c689dd41e49b8b786/rasterio-1.4.4-cp311-cp311-win_amd64.whl", hash = "sha256:0718630f607be2f5742d8e4b34b434746fd788a192d77eefc9bb924399fea802", size = 25716477, upload-time = "2025-12-12T17:59:13.519Z" },

+    { url = "https://files.pythonhosted.org/packages/4b/02/039eb4970c93aaef4c9eb1ee159abad18e6e7f932c2eed575c95f78d94f6/rasterio-1.4.4-cp311-cp311-win_arm64.whl", hash = "sha256:0308ff4762ae9eb40a991f12d758626b59af4376b13675480391dd7295d17bbf", size = 24075993, upload-time = "2025-12-12T17:59:16.407Z" },

+    { url = "https://files.pythonhosted.org/packages/4c/fc/63d89ddfcb4643730553683ee322566b9b15fe56d026e4c21c4f4f5d9d26/rasterio-1.4.4-cp312-cp312-macosx_14_0_arm64.whl", hash = "sha256:f3c4f0cbd188f893011f2a0a6dc2852b3892799b3a0d79eddf92f2b115ec7ed7", size = 21120715, upload-time = "2025-12-12T17:59:19.35Z" },

+    { url = "https://files.pythonhosted.org/packages/43/70/2c003f76a23dbb078fdee35c8e2ec490d2ad8982f4dc956ba08b56027b87/rasterio-1.4.4-cp312-cp312-macosx_15_0_x86_64.whl", hash = "sha256:6fce26090b9f509eab337228420145947c491a13628965410f25bc3e6e05cf75", size = 25732944, upload-time = "2025-12-12T17:59:22.533Z" },

+    { url = "https://files.pythonhosted.org/packages/f6/cc/4a8e92362c0ff496dd1007c3dcba66e9ededf1a45eca8ad1db302b071c49/rasterio-1.4.4-cp312-cp312-manylinux_2_28_aarch64.whl", hash = "sha256:c1c722da390dc264aeccdc0dc200ca37923875d910ca4cd5bec0fec351bb818e", size = 34295209, upload-time = "2025-12-12T17:59:26.035Z" },

+    { url = "https://files.pythonhosted.org/packages/e6/6d/717d2dec47fbefad33ca0d27bd5f0d543b1d1bc9fcab5ef82a13adaaf38d/rasterio-1.4.4-cp312-cp312-manylinux_2_28_x86_64.whl", hash = "sha256:98b6dfb8282b2a54b9d75c3dc8d2520a69bbc66916c7d43de8e0bbf6e0240ca1", size = 35661866, upload-time = "2025-12-12T17:59:29.928Z" },

+    { url = "https://files.pythonhosted.org/packages/ed/60/ae3351fba2726ec0976974ce2eb030c159edd3363b8771e832b8db571c24/rasterio-1.4.4-cp312-cp312-win_amd64.whl", hash = "sha256:9513f4c7a6d93b45098f8dff2421fa9516604e3bfbf35aa144484a88d36a321f", size = 25682853, upload-time = "2025-12-12T17:59:35.869Z" },

+    { url = "https://files.pythonhosted.org/packages/38/ee/35387296bbacfc5cbbb4273228b1b959793d3ce38b0402a07f11a248420b/rasterio-1.4.4-cp312-cp312-win_arm64.whl", hash = "sha256:60b49a482e0f12f12ce9d2cc3090add02f89f3d422e85f2cffaa9207adb83c04", size = 24043249, upload-time = "2025-12-12T17:59:39.915Z" },

+    { url = "https://files.pythonhosted.org/packages/c1/fe/e3e37041c49956f4f4cbe473c3fe290aaba96ed20e9c07da304e0cad2015/rasterio-1.4.4-cp313-cp313-macosx_14_0_arm64.whl", hash = "sha256:df26c96aa81ffbd0b33189680859211eadf9950123c21579f84de73bb0f91d81", size = 21107336, upload-time = "2025-12-12T17:59:43.585Z" },

+    { url = "https://files.pythonhosted.org/packages/f3/02/c217fdcc8e80a4b7d1b1bc4529d78f98452816e9add53ff8742049a77ae7/rasterio-1.4.4-cp313-cp313-macosx_15_0_x86_64.whl", hash = "sha256:b3af0ecc922a80f3755516629f7948e37bade9077b5f5c12a3869a5e7f01619b", size = 25719929, upload-time = "2025-12-12T17:59:47.64Z" },

+    { url = "https://files.pythonhosted.org/packages/c0/d0/7f177f37bc9595d809dabb0073abd0c42358469f6b10875192b46331c652/rasterio-1.4.4-cp313-cp313-manylinux_2_28_aarch64.whl", hash = "sha256:7ce3b0f9a22e95a27790087908753973644d7c3877d495ec9bd6e04a25233ca4", size = 34198845, upload-time = "2025-12-12T17:59:52.405Z" },

+    { url = "https://files.pythonhosted.org/packages/7b/84/66c0d9cca2a09074ec2ce6fffa87709ca51b0d197ae742d835e841bac660/rasterio-1.4.4-cp313-cp313-manylinux_2_28_x86_64.whl", hash = "sha256:c072450caa96428b1218b030500bb908fd6f09bc013a88969ff81a124b6a112a", size = 35576074, upload-time = "2025-12-12T17:59:56.392Z" },

+    { url = "https://files.pythonhosted.org/packages/32/68/f7df5478458ace2fa50be43e9fab1a39957a0e71afaa3e6147ec289e0fc8/rasterio-1.4.4-cp313-cp313-win_amd64.whl", hash = "sha256:16ee92ef10c0ba89f45f9c2b40fca9f971f357385f04ee9b716fb09cbd9ce20c", size = 25680573, upload-time = "2025-12-12T18:00:00.45Z" },

+    { url = "https://files.pythonhosted.org/packages/34/e5/1bdaccb658430dfd391ad4a63d206546f36639d7e4130bf31f125c6525b4/rasterio-1.4.4-cp313-cp313-win_arm64.whl", hash = "sha256:65c10afe64b5e488185aaff0b659e08eda22c89285b54a3e433b80e6c6621770", size = 24040367, upload-time = "2025-12-12T18:00:04.443Z" },

+    { url = "https://files.pythonhosted.org/packages/32/76/54643a7d1d650fd7f1acea9093c298603e4c01bba6f90be2254310b48507/rasterio-1.4.4-cp313-cp313t-macosx_14_0_arm64.whl", hash = "sha256:18c2c1130e789dc2771d0aa5ec4b56d5b8a0097c648ccb94882d5ff3ab55c928", size = 21247203, upload-time = "2025-12-12T18:00:07.547Z" },

+    { url = "https://files.pythonhosted.org/packages/76/ef/434b4849ccd6a3e03a0b1ac37c963c1771564945745613d15c5d96ce768d/rasterio-1.4.4-cp313-cp313t-macosx_15_0_x86_64.whl", hash = "sha256:2d1654b7ffa6f3dde42c5fd27159ae45148c11e352de26f12fe7313a3236aeed", size = 25822050, upload-time = "2025-12-12T18:00:11.081Z" },

+    { url = "https://files.pythonhosted.org/packages/2d/fa/fe9a478aa0cde246da58baeb0df3248c7ca174e4d9c9b27e81b504e40a76/rasterio-1.4.4-cp313-cp313t-manylinux_2_28_aarch64.whl", hash = "sha256:c4022cbddb659856e120603b12233cec8913ae760fff220657ce888c3c6b9f9d", size = 34833783, upload-time = "2025-12-12T18:00:14.525Z" },

+    { url = "https://files.pythonhosted.org/packages/04/cd/ed4716590dbcd4b8ae633417d758564e510bee4d6aaac5050a0f6d5179c5/rasterio-1.4.4-cp313-cp313t-manylinux_2_28_x86_64.whl", hash = "sha256:96b88880551a07b7a3b50439483cefbd9af91a09e19ff2b736815994e5671314", size = 35738114, upload-time = "2025-12-12T18:00:17.96Z" },

+    { url = "https://files.pythonhosted.org/packages/7e/29/da7050d11ba1d041e0333ac14768e6e9ca1aa2b9fa8416f317d2650ed276/rasterio-1.4.4-cp313-cp313t-win_amd64.whl", hash = "sha256:def75d486d0ab8f306f918a913c425ed57159495518c54efe8e18d5164d37d90", size = 25896835, upload-time = "2025-12-12T18:00:21.411Z" },

+    { url = "https://files.pythonhosted.org/packages/88/80/304dbe5434c4aa8dfaf90480c16d770161796a6a61fa88e72e8a402153df/rasterio-1.4.4-cp313-cp313t-win_arm64.whl", hash = "sha256:770b7e86f6c565e6f9cf30f6fa4479a5a2bab4e10ff44fe7acfd518ca4a71d1b", size = 24128074, upload-time = "2025-12-12T18:00:24.653Z" },

+    { url = "https://files.pythonhosted.org/packages/03/01/d5a3dc51cd5fef62b76ecc77d33c1ca20de305fed7e16c71bcdf4858e466/rasterio-1.4.4-cp314-cp314-macosx_14_0_arm64.whl", hash = "sha256:019693f14a83ae9225cb57c16e466901d0e6284962dcf13a9f4bb1175b979011", size = 21120237, upload-time = "2025-12-12T18:00:27.723Z" },

+    { url = "https://files.pythonhosted.org/packages/50/da/db18362602b17327c0e00c9e9c0847c1c4ac657c1a289169ca06a26faccb/rasterio-1.4.4-cp314-cp314-macosx_15_0_x86_64.whl", hash = "sha256:87d7c3e97e3b40c9041d1602e2dcb4fc2d88abe6c645fccb4939dec297a91cf8", size = 25720506, upload-time = "2025-12-12T18:00:30.592Z" },

+    { url = "https://files.pythonhosted.org/packages/5a/8f/a15d66c9c05bffb176c9707ef1f2bfcf9c0b835272937c80ac7207a20b5c/rasterio-1.4.4-cp314-cp314-manylinux_2_28_aarch64.whl", hash = "sha256:a2401e4c43a31c7382154d4042b60a63b9bca5886802983c5c9362cdc5b09548", size = 34153931, upload-time = "2025-12-12T18:00:33.852Z" },

+    { url = "https://files.pythonhosted.org/packages/05/2d/cd778286b910db7a3f0bc1743ca362173f1fbb7365137e4982ca857b6d26/rasterio-1.4.4-cp314-cp314-manylinux_2_28_x86_64.whl", hash = "sha256:6c4287d8934d953f7870b8e2a1df1096fbf47eba39ad0f777a31ea500f4e5010", size = 35421139, upload-time = "2025-12-12T18:00:37.482Z" },

+    { url = "https://files.pythonhosted.org/packages/70/97/13a2e33aede8d7a42178c696a6a93868d1f9560f73de05033a1675f0806a/rasterio-1.4.4-cp314-cp314-win_amd64.whl", hash = "sha256:c3ba1871549221140661227dd4fa1f9a472ded4a6d2f2c2e367b0648bb15b99d", size = 26419132, upload-time = "2025-12-12T18:00:40.871Z" },

+    { url = "https://files.pythonhosted.org/packages/27/d8/2dcfcb362d6a2fd07c14cfb803a345a7926d4d9fb6243e196df105671e97/rasterio-1.4.4-cp314-cp314-win_arm64.whl", hash = "sha256:7c9d7dc824cb8d222808be153643cd4e65ea3e1f66019ada1ccd630221edfe30", size = 24800998, upload-time = "2025-12-12T18:00:45.332Z" },

+    { url = "https://files.pythonhosted.org/packages/13/f8/16e9b648e7f16cadb41df7c0116dbab26b4a2ba02c85cbe3f744065bdf56/rasterio-1.4.4-cp314-cp314t-macosx_14_0_arm64.whl", hash = "sha256:98e17bded830a59992d9f8f8d9f227ce1c4be0694930afcc4360358f5cb1a5db", size = 21247046, upload-time = "2025-12-12T18:00:49.429Z" },

+    { url = "https://files.pythonhosted.org/packages/a8/ea/f3dc3a25d7591821d488f5c5eb89f6abcd1f5c8e2ef4bd2792f965cbc9c8/rasterio-1.4.4-cp314-cp314t-macosx_15_0_x86_64.whl", hash = "sha256:56134ca203f952855e60774b06672033cf65057eb9810fcc5c1a75f1921053a3", size = 25821677, upload-time = "2025-12-12T18:00:52.458Z" },

+    { url = "https://files.pythonhosted.org/packages/2e/d3/1e038350218e852f904c8dc4ab751aa023a2e82e68998767b7b42e33832c/rasterio-1.4.4-cp314-cp314t-manylinux_2_28_aarch64.whl", hash = "sha256:52edde65515b33fe4314c8a44a9ee2fc00b550deed6d56e1a8d085d42bbca3e6", size = 34829572, upload-time = "2025-12-12T18:00:56.294Z" },

+    { url = "https://files.pythonhosted.org/packages/0b/ce/28abf7a5f5d9cb014c2e14cc396bebe953b3deefbf604d49f4322e73fa35/rasterio-1.4.4-cp314-cp314t-manylinux_2_28_x86_64.whl", hash = "sha256:d61d3f2c171c64050bd75e54a5d964ff7f165b3f5d2b92c9ee09b9716aa1b8bf", size = 35735171, upload-time = "2025-12-12T18:00:59.531Z" },

+    { url = "https://files.pythonhosted.org/packages/54/91/1ce35cfda2d56dacd6395faf20a5290268bd9009c53393ac42b5f9bb2c4c/rasterio-1.4.4-cp314-cp314t-win_amd64.whl", hash = "sha256:40137fe512c0d6e96c0167a0ae4e56d82c488f244163c45494b7392e51c844de", size = 26700712, upload-time = "2025-12-12T18:01:03.023Z" },

+    { url = "https://files.pythonhosted.org/packages/3b/33/4d13f48a8f01d782ffc1eece20821586518f3f515dca7cf152bca9fd22d4/rasterio-1.4.4-cp314-cp314t-win_arm64.whl", hash = "sha256:29ec3a794454b5bb255c9c0374cc380030a8a1e295c81eee7feb036802d2a9e3", size = 24875933, upload-time = "2025-12-12T18:01:06.134Z" },

+]

+

+[[package]]

+name = "rasterio"

+version = "1.5.0"

+source = { registry = "https://pypi.org/simple" }

+resolution-markers = [

+    "python_full_version >= '3.12'",

+]

+dependencies = [

+    { name = "affine", marker = "python_full_version >= '3.12'" },

+    { name = "attrs", marker = "python_full_version >= '3.12'" },

+    { name = "certifi", marker = "python_full_version >= '3.12'" },

+    { name = "click", marker = "python_full_version >= '3.12'" },

+    { name = "cligj", marker = "python_full_version >= '3.12'" },

+    { name = "numpy", marker = "python_full_version >= '3.12'" },

+    { name = "pyparsing", marker = "python_full_version >= '3.12'" },

+]

+sdist = { url = "https://files.pythonhosted.org/packages/f6/88/edb4b66b6cb2c13f123af5a3896bf70c0cbe73ab3cd4243cb4eb0212a0f6/rasterio-1.5.0.tar.gz", hash = "sha256:1e0ea56b02eea4989b36edf8e58a5a3ef40e1b7edcb04def2603accd5ab3ee7b", size = 452184, upload-time = "2026-01-05T16:06:47.169Z" }

+wheels = [

+    { url = "https://files.pythonhosted.org/packages/ac/de/ba1cd11d7d1182bfb26e758bf07016d04e5442f4f5fea35b0d7279b72399/rasterio-1.5.0-cp312-cp312-macosx_14_0_arm64.whl", hash = "sha256:420656074897a460f5ef46f657b3061d2e004f9d99e613914b0671643e69d92c", size = 22787192, upload-time = "2026-01-05T16:05:19.779Z" },

+    { url = "https://files.pythonhosted.org/packages/e6/42/efaeb6dc531dbcd02fec01c791a853bb5a139a5126ecec579ac0f735eeb9/rasterio-1.5.0-cp312-cp312-macosx_15_0_x86_64.whl", hash = "sha256:c5c3597a783857e760550e8f26365d928b0377ac5ffc3e12ba447ac65ca5406d", size = 24412221, upload-time = "2026-01-05T16:05:22.526Z" },

+    { url = "https://files.pythonhosted.org/packages/a2/14/89645988424c40cbcb8334f94305ffe094dd28d85c643341d9690704c9f0/rasterio-1.5.0-cp312-cp312-manylinux_2_28_aarch64.whl", hash = "sha256:e14d07a09833b6df6024ce7a57aee1e1977b3aec682e30b1e58ce773462f2382", size = 36128020, upload-time = "2026-01-05T16:05:25.556Z" },

+    { url = "https://files.pythonhosted.org/packages/85/23/5a52319a98451ff910f42e5f7f4804bfb39f9327933a89daab685d1ce2dd/rasterio-1.5.0-cp312-cp312-manylinux_2_28_x86_64.whl", hash = "sha256:26dbcffcf0d01fc121cbb92186bc1cb78e16efe62b17be45ad7494446b325cf8", size = 37634010, upload-time = "2026-01-05T16:05:28.673Z" },

+    { url = "https://files.pythonhosted.org/packages/57/d6/fe8826f813c98b046d8d4c3bc83053c89c71f367f89257d211fe5dd0b0ba/rasterio-1.5.0-cp312-cp312-win_amd64.whl", hash = "sha256:ac8d04eee66ca8060763ead607800e5611d857dd005905d920365e24a16ba20a", size = 30142328, upload-time = "2026-01-05T16:05:31.357Z" },

+    { url = "https://files.pythonhosted.org/packages/af/62/6397379271d5628ed65ef781bf2d3a8f56094a86e6d8479c6ca506a1b960/rasterio-1.5.0-cp312-cp312-win_arm64.whl", hash = "sha256:31f1edc45c781ebd087e60cc00a4fc37028dd3fe25cff4098e4139fc9d0565be", size = 28500710, upload-time = "2026-01-05T16:05:33.906Z" },

+    { url = "https://files.pythonhosted.org/packages/42/87/42865a77cebf2e524d27b6afc71db48984799ecd1dbe6a213d4713f42f5f/rasterio-1.5.0-cp313-cp313-macosx_14_0_arm64.whl", hash = "sha256:e7b25b0a19975ccd511e507e6de45b0a2d8fb6802abe49bb726cf48588e34833", size = 22776107, upload-time = "2026-01-05T16:05:36.967Z" },

+    { url = "https://files.pythonhosted.org/packages/6a/53/e81683fbbfdf04e019e68b042d9cff8524b0571aa80e4f4d81c373c31a49/rasterio-1.5.0-cp313-cp313-macosx_15_0_x86_64.whl", hash = "sha256:1162c18eaece9f6d2aa1c2ff6b373b99651d93f113f24120a991eaebf28aa4f4", size = 24401477, upload-time = "2026-01-05T16:05:39.702Z" },

+    { url = "https://files.pythonhosted.org/packages/bc/3c/6aa6e0690b18eea02a61739cb362a47c5df66138f0a02cc69e1181b964e5/rasterio-1.5.0-cp313-cp313-manylinux_2_28_aarch64.whl", hash = "sha256:8eb87fd6f843eea109f3df9bef83f741b053b716b0465932276e2c0577dfb929", size = 36018214, upload-time = "2026-01-05T16:05:42.741Z" },

+    { url = "https://files.pythonhosted.org/packages/48/4a/1af9aa9810fb30668568f2c4dd3eec2412c8e9762b69201d971c509b295e/rasterio-1.5.0-cp313-cp313-manylinux_2_28_x86_64.whl", hash = "sha256:08a7580cbb9b3bd320bdf827e10c9b2424d0df066d8eef6f2feb37e154ce0c17", size = 37544972, upload-time = "2026-01-05T16:05:45.815Z" },

+    { url = "https://files.pythonhosted.org/packages/01/62/bfe3408743c9837919ff232474a09ece9eaa88d4ee8c040711fa3dff6dad/rasterio-1.5.0-cp313-cp313-win_amd64.whl", hash = "sha256:d7d6729c0739b5ec48c33686668a30e27f5bdb361093f180ee7818ff19665547", size = 30140141, upload-time = "2026-01-05T16:05:48.751Z" },

+    { url = "https://files.pythonhosted.org/packages/63/ca/e90e19a6d065a718cc3d468a12b9f015289ad17017656dea8c76f7318d1f/rasterio-1.5.0-cp313-cp313-win_arm64.whl", hash = "sha256:8af7c368c22f0a99d1259ccc5a5cd96c432c2bde6f132c1ac78508cd7445a745", size = 28498556, upload-time = "2026-01-05T16:05:51.334Z" },

+    { url = "https://files.pythonhosted.org/packages/a0/ba/e37462d8c33bbbd6c152a0390ec6911a3d9614ded3d2bc6f6a48e147e833/rasterio-1.5.0-cp313-cp313t-macosx_14_0_arm64.whl", hash = "sha256:b4ccfcc8ed9400e4f14efdf2005533fcf72048748b727f85ff89b9291ecdf98a", size = 22920107, upload-time = "2026-01-05T16:05:53.773Z" },

+    { url = "https://files.pythonhosted.org/packages/66/dc/7bfa9cf96ac39b451b2f94dfc584c223ec584c52c148df2e4bab60c3341b/rasterio-1.5.0-cp313-cp313t-macosx_15_0_x86_64.whl", hash = "sha256:2f57c36ca4d3c896f7024226bd71eeb5cd10c8183c2a94508534d78cc05ff9e7", size = 24508993, upload-time = "2026-01-05T16:05:57.062Z" },

+    { url = "https://files.pythonhosted.org/packages/e5/55/7293743f3b69de4b726c67b8dc9da01fc194070b6becc51add4ca8a20a27/rasterio-1.5.0-cp313-cp313t-manylinux_2_28_aarch64.whl", hash = "sha256:cc1395475e4bb7032cd81dda4d5558061c4c7d5a50b1b5e146bdf9716d0b9353", size = 36565784, upload-time = "2026-01-05T16:06:00.019Z" },

+    { url = "https://files.pythonhosted.org/packages/cf/ef/5354c47de16c6e289728c3a3d6961ffcf7a9ad6313aef7e8db5d6a40c46e/rasterio-1.5.0-cp313-cp313t-manylinux_2_28_x86_64.whl", hash = "sha256:592a485e2057b1aaeab4f843c9897628e60e3ff45e2509325c3e1479116599cb", size = 37686456, upload-time = "2026-01-05T16:06:02.772Z" },

+    { url = "https://files.pythonhosted.org/packages/b7/fc/fe1f034b1acd1900d9fbd616826d001a3d5811f1d0c97c785f88f525853e/rasterio-1.5.0-cp313-cp313t-win_amd64.whl", hash = "sha256:0c739e70a72fb080f039ee1570c5d02b974dde32ded1a3216e1f13fe38ac4844", size = 30355842, upload-time = "2026-01-05T16:06:06.359Z" },

+    { url = "https://files.pythonhosted.org/packages/e0/cb/4dee9697891c9c6474b240d00e27688e03ecd882d3c83cc97eb25c2266ff/rasterio-1.5.0-cp313-cp313t-win_arm64.whl", hash = "sha256:a3539a2f401a7b4b2e94ff2db334878c0e15a2d1c9fe90bb0879c52f89367ae5", size = 28589538, upload-time = "2026-01-05T16:06:09.662Z" },

+    { url = "https://files.pythonhosted.org/packages/77/9f/f84dfa54110c1c82f9f4fd929465d12519569b6f5d015273aa0957013b2e/rasterio-1.5.0-cp314-cp314-macosx_14_0_arm64.whl", hash = "sha256:597be8df418d5ba7b6a927b6b9febfcb42b192882448a8d5b2e2e75a1296631f", size = 22788832, upload-time = "2026-01-05T16:06:12.247Z" },

+    { url = "https://files.pythonhosted.org/packages/20/f1/de55255c918b17afd7292f793a3500c4aea7e9530b2b3f5b3a57836c7d49/rasterio-1.5.0-cp314-cp314-macosx_15_0_x86_64.whl", hash = "sha256:dd292030d39d685c0b35eddef233e7f1cb8b43052578a3ec97a2da57799693be", size = 24405917, upload-time = "2026-01-05T16:06:14.603Z" },

+    { url = "https://files.pythonhosted.org/packages/a9/57/054087a9d5011ad5dfa799277ba8814e41775e1967d37a59ab7b8e2f1876/rasterio-1.5.0-cp314-cp314-manylinux_2_28_aarch64.whl", hash = "sha256:62c3f97a3c72643c74f2d0f310621a09c35c0c412229c327ae6bcc1ee4b9c3bc", size = 35987536, upload-time = "2026-01-05T16:06:17.707Z" },

+    { url = "https://files.pythonhosted.org/packages/c9/72/5fbe5f67ae75d7e89ffb718c500d5fecbaa84f6ba354db306de689faf961/rasterio-1.5.0-cp314-cp314-manylinux_2_28_x86_64.whl", hash = "sha256:19577f0f0c5f1158af47b57f73356961cbd1782a5f6ae6f3adf6f2650f4eb369", size = 37408048, upload-time = "2026-01-05T16:06:20.82Z" },

+    { url = "https://files.pythonhosted.org/packages/c4/3e/0c4ef19980204bdcbc8f9e084056adebc97916ff4edcc718750ef34e5bf9/rasterio-1.5.0-cp314-cp314-win_amd64.whl", hash = "sha256:015c1ab6e5453312c5e29692752e7ad73568fe4d13567cbd448d7893128cbd2d", size = 30949590, upload-time = "2026-01-05T16:06:23.425Z" },

+    { url = "https://files.pythonhosted.org/packages/c2/d8/2e6b81505408926c00e629d7d3d73fd0454213201bd9907450e0fe82f3dd/rasterio-1.5.0-cp314-cp314-win_arm64.whl", hash = "sha256:ff677c0a9d3ba667c067227ef2b76872488b37ff29b061bc3e576fad9baa3286", size = 29337287, upload-time = "2026-01-05T16:06:26.599Z" },

+    { url = "https://files.pythonhosted.org/packages/19/49/7b6e6afb28d4e3f69f2229f990ed87dfdc21a3e15ca63b96b2fd9ba17d89/rasterio-1.5.0-cp314-cp314t-macosx_14_0_arm64.whl", hash = "sha256:508251b9c746d8d008771a30c2160ff321bfc3b41f6a1aa8e8ef1dd4a00d97ba", size = 22926149, upload-time = "2026-01-05T16:06:29.617Z" },

+    { url = "https://files.pythonhosted.org/packages/24/30/19345d8bc7d2b96c1172594026b9009702e9ab9f0baf07079d3612aaadae/rasterio-1.5.0-cp314-cp314t-macosx_15_0_x86_64.whl", hash = "sha256:742841ed48bc70f6ef517b8fa3521f231780bf408fde0aa6d73770337a36374e", size = 24516040, upload-time = "2026-01-05T16:06:32.964Z" },

+    { url = "https://files.pythonhosted.org/packages/9e/43/dc7a4518fa78904bc41952cbf346c3c2a88a20e61b479154058392914c0b/rasterio-1.5.0-cp314-cp314t-manylinux_2_28_aarch64.whl", hash = "sha256:c9a9eee49ce9410c2f352b34c370bb3a96bb518b6a7f97b3a72ee4c835fd4b5c", size = 36589519, upload-time = "2026-01-05T16:06:35.922Z" },

+    { url = "https://files.pythonhosted.org/packages/8f/f2/8f706083c6c163054d12c7ed6d5ac4e4ed02252b761288d74e6158871b34/rasterio-1.5.0-cp314-cp314t-manylinux_2_28_x86_64.whl", hash = "sha256:b9fd87a0b63ab5c6267dfb0bc96f54fdf49d000651b9ee85ed37798141cff046", size = 37714599, upload-time = "2026-01-05T16:06:38.818Z" },

+    { url = "https://files.pythonhosted.org/packages/a6/d5/bbca726d5fea5864f7e4bcf3ee893095369e93ad51120495e8c40e2aa1a0/rasterio-1.5.0-cp314-cp314t-win_amd64.whl", hash = "sha256:f459db8953ba30ca04fcef2b5e1260eeeff0eae8158bd9c3d6adbe56289765cc", size = 31233931, upload-time = "2026-01-05T16:06:42.208Z" },

+    { url = "https://files.pythonhosted.org/packages/6e/d1/8b017856e63ccaff3cbd0e82490dbb01363a42f3a462a41b1d8a391e1443/rasterio-1.5.0-cp314-cp314t-win_arm64.whl", hash = "sha256:f4b9c2c3b5f10469eb9588f105086e68f0279e62cc9095c4edd245e3f9b88c8a", size = 29418321, upload-time = "2026-01-05T16:06:44.758Z" },

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

+    { url = "https://files.pythonhosted.org/packages/24/c0/f3b6453cf2dfa99adc0ba6675f9aaff9e526d2224cbd7ff9c1a879238693/shapely-2.1.2-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:fe2533caae6a91a543dec62e8360fe86ffcdc42a7c55f9dfd0128a977a896b94", size = 1833550, upload-time = "2025-09-24T13:50:30.019Z" },

+    { url = "https://files.pythonhosted.org/packages/86/07/59dee0bc4b913b7ab59ab1086225baca5b8f19865e6101db9ebb7243e132/shapely-2.1.2-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:ba4d1333cc0bc94381d6d4308d2e4e008e0bd128bdcff5573199742ee3634359", size = 1643556, upload-time = "2025-09-24T13:50:32.291Z" },

+    { url = "https://files.pythonhosted.org/packages/26/29/a5397e75b435b9895cd53e165083faed5d12fd9626eadec15a83a2411f0f/shapely-2.1.2-cp312-cp312-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:0bd308103340030feef6c111d3eb98d50dc13feea33affc8a6f9fa549e9458a3", size = 2988308, upload-time = "2025-09-24T13:50:33.862Z" },

+    { url = "https://files.pythonhosted.org/packages/b9/37/e781683abac55dde9771e086b790e554811a71ed0b2b8a1e789b7430dd44/shapely-2.1.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:1e7d4d7ad262a48bb44277ca12c7c78cb1b0f56b32c10734ec9a1d30c0b0c54b", size = 3099844, upload-time = "2025-09-24T13:50:35.459Z" },

+    { url = "https://files.pythonhosted.org/packages/d8/f3/9876b64d4a5a321b9dc482c92bb6f061f2fa42131cba643c699f39317cb9/shapely-2.1.2-cp312-cp312-musllinux_1_2_aarch64.whl", hash = "sha256:e9eddfe513096a71896441a7c37db72da0687b34752c4e193577a145c71736fc", size = 3988842, upload-time = "2025-09-24T13:50:37.478Z" },

+    { url = "https://files.pythonhosted.org/packages/d1/a0/704c7292f7014c7e74ec84eddb7b109e1fbae74a16deae9c1504b1d15565/shapely-2.1.2-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:980c777c612514c0cf99bc8a9de6d286f5e186dcaf9091252fcd444e5638193d", size = 4152714, upload-time = "2025-09-24T13:50:39.9Z" },

+    { url = "https://files.pythonhosted.org/packages/53/46/319c9dc788884ad0785242543cdffac0e6530e4d0deb6c4862bc4143dcf3/shapely-2.1.2-cp312-cp312-win32.whl", hash = "sha256:9111274b88e4d7b54a95218e243282709b330ef52b7b86bc6aaf4f805306f454", size = 1542745, upload-time = "2025-09-24T13:50:41.414Z" },

+    { url = "https://files.pythonhosted.org/packages/ec/bf/cb6c1c505cb31e818e900b9312d514f381fbfa5c4363edfce0fcc4f8c1a4/shapely-2.1.2-cp312-cp312-win_amd64.whl", hash = "sha256:743044b4cfb34f9a67205cee9279feaf60ba7d02e69febc2afc609047cb49179", size = 1722861, upload-time = "2025-09-24T13:50:43.35Z" },

+    { url = "https://files.pythonhosted.org/packages/c3/90/98ef257c23c46425dc4d1d31005ad7c8d649fe423a38b917db02c30f1f5a/shapely-2.1.2-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:b510dda1a3672d6879beb319bc7c5fd302c6c354584690973c838f46ec3e0fa8", size = 1832644, upload-time = "2025-09-24T13:50:44.886Z" },

+    { url = "https://files.pythonhosted.org/packages/6d/ab/0bee5a830d209adcd3a01f2d4b70e587cdd9fd7380d5198c064091005af8/shapely-2.1.2-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:8cff473e81017594d20ec55d86b54bc635544897e13a7cfc12e36909c5309a2a", size = 1642887, upload-time = "2025-09-24T13:50:46.735Z" },

+    { url = "https://files.pythonhosted.org/packages/2d/5e/7d7f54ba960c13302584c73704d8c4d15404a51024631adb60b126a4ae88/shapely-2.1.2-cp313-cp313-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:fe7b77dc63d707c09726b7908f575fc04ff1d1ad0f3fb92aec212396bc6cfe5e", size = 2970931, upload-time = "2025-09-24T13:50:48.374Z" },

+    { url = "https://files.pythonhosted.org/packages/f2/a2/83fc37e2a58090e3d2ff79175a95493c664bcd0b653dd75cb9134645a4e5/shapely-2.1.2-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:7ed1a5bbfb386ee8332713bf7508bc24e32d24b74fc9a7b9f8529a55db9f4ee6", size = 3082855, upload-time = "2025-09-24T13:50:50.037Z" },

+    { url = "https://files.pythonhosted.org/packages/44/2b/578faf235a5b09f16b5f02833c53822294d7f21b242f8e2d0cf03fb64321/shapely-2.1.2-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:a84e0582858d841d54355246ddfcbd1fce3179f185da7470f41ce39d001ee1af", size = 3979960, upload-time = "2025-09-24T13:50:51.74Z" },

+    { url = "https://files.pythonhosted.org/packages/4d/04/167f096386120f692cc4ca02f75a17b961858997a95e67a3cb6a7bbd6b53/shapely-2.1.2-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:dc3487447a43d42adcdf52d7ac73804f2312cbfa5d433a7d2c506dcab0033dfd", size = 4142851, upload-time = "2025-09-24T13:50:53.49Z" },

+    { url = "https://files.pythonhosted.org/packages/48/74/fb402c5a6235d1c65a97348b48cdedb75fb19eca2b1d66d04969fc1c6091/shapely-2.1.2-cp313-cp313-win32.whl", hash = "sha256:9c3a3c648aedc9f99c09263b39f2d8252f199cb3ac154fadc173283d7d111350", size = 1541890, upload-time = "2025-09-24T13:50:55.337Z" },

+    { url = "https://files.pythonhosted.org/packages/41/47/3647fe7ad990af60ad98b889657a976042c9988c2807cf322a9d6685f462/shapely-2.1.2-cp313-cp313-win_amd64.whl", hash = "sha256:ca2591bff6645c216695bdf1614fca9c82ea1144d4a7591a466fef64f28f0715", size = 1722151, upload-time = "2025-09-24T13:50:57.153Z" },

+    { url = "https://files.pythonhosted.org/packages/3c/49/63953754faa51ffe7d8189bfbe9ca34def29f8c0e34c67cbe2a2795f269d/shapely-2.1.2-cp313-cp313t-macosx_10_13_x86_64.whl", hash = "sha256:2d93d23bdd2ed9dc157b46bc2f19b7da143ca8714464249bef6771c679d5ff40", size = 1834130, upload-time = "2025-09-24T13:50:58.49Z" },

+    { url = "https://files.pythonhosted.org/packages/7f/ee/dce001c1984052970ff60eb4727164892fb2d08052c575042a47f5a9e88f/shapely-2.1.2-cp313-cp313t-macosx_11_0_arm64.whl", hash = "sha256:01d0d304b25634d60bd7cf291828119ab55a3bab87dc4af1e44b07fb225f188b", size = 1642802, upload-time = "2025-09-24T13:50:59.871Z" },

+    { url = "https://files.pythonhosted.org/packages/da/e7/fc4e9a19929522877fa602f705706b96e78376afb7fad09cad5b9af1553c/shapely-2.1.2-cp313-cp313t-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:8d8382dd120d64b03698b7298b89611a6ea6f55ada9d39942838b79c9bc89801", size = 3018460, upload-time = "2025-09-24T13:51:02.08Z" },

+    { url = "https://files.pythonhosted.org/packages/a1/18/7519a25db21847b525696883ddc8e6a0ecaa36159ea88e0fef11466384d0/shapely-2.1.2-cp313-cp313t-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:19efa3611eef966e776183e338b2d7ea43569ae99ab34f8d17c2c054d3205cc0", size = 3095223, upload-time = "2025-09-24T13:51:04.472Z" },

+    { url = "https://files.pythonhosted.org/packages/48/de/b59a620b1f3a129c3fecc2737104a0a7e04e79335bd3b0a1f1609744cf17/shapely-2.1.2-cp313-cp313t-musllinux_1_2_aarch64.whl", hash = "sha256:346ec0c1a0fcd32f57f00e4134d1200e14bf3f5ae12af87ba83ca275c502498c", size = 4030760, upload-time = "2025-09-24T13:51:06.455Z" },

+    { url = "https://files.pythonhosted.org/packages/96/b3/c6655ee7232b417562bae192ae0d3ceaadb1cc0ffc2088a2ddf415456cc2/shapely-2.1.2-cp313-cp313t-musllinux_1_2_x86_64.whl", hash = "sha256:6305993a35989391bd3476ee538a5c9a845861462327efe00dd11a5c8c709a99", size = 4170078, upload-time = "2025-09-24T13:51:08.584Z" },

+    { url = "https://files.pythonhosted.org/packages/a0/8e/605c76808d73503c9333af8f6cbe7e1354d2d238bda5f88eea36bfe0f42a/shapely-2.1.2-cp313-cp313t-win32.whl", hash = "sha256:c8876673449f3401f278c86eb33224c5764582f72b653a415d0e6672fde887bf", size = 1559178, upload-time = "2025-09-24T13:51:10.73Z" },

+    { url = "https://files.pythonhosted.org/packages/36/f7/d317eb232352a1f1444d11002d477e54514a4a6045536d49d0c59783c0da/shapely-2.1.2-cp313-cp313t-win_amd64.whl", hash = "sha256:4a44bc62a10d84c11a7a3d7c1c4fe857f7477c3506e24c9062da0db0ae0c449c", size = 1739756, upload-time = "2025-09-24T13:51:12.105Z" },

+    { url = "https://files.pythonhosted.org/packages/fc/c4/3ce4c2d9b6aabd27d26ec988f08cb877ba9e6e96086eff81bfea93e688c7/shapely-2.1.2-cp314-cp314-macosx_10_13_x86_64.whl", hash = "sha256:9a522f460d28e2bf4e12396240a5fc1518788b2fcd73535166d748399ef0c223", size = 1831290, upload-time = "2025-09-24T13:51:13.56Z" },

+    { url = "https://files.pythonhosted.org/packages/17/b9/f6ab8918fc15429f79cb04afa9f9913546212d7fb5e5196132a2af46676b/shapely-2.1.2-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:1ff629e00818033b8d71139565527ced7d776c269a49bd78c9df84e8f852190c", size = 1641463, upload-time = "2025-09-24T13:51:14.972Z" },

+    { url = "https://files.pythonhosted.org/packages/a5/57/91d59ae525ca641e7ac5551c04c9503aee6f29b92b392f31790fcb1a4358/shapely-2.1.2-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:f67b34271dedc3c653eba4e3d7111aa421d5be9b4c4c7d38d30907f796cb30df", size = 2970145, upload-time = "2025-09-24T13:51:16.961Z" },

+    { url = "https://files.pythonhosted.org/packages/8a/cb/4948be52ee1da6927831ab59e10d4c29baa2a714f599f1f0d1bc747f5777/shapely-2.1.2-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:21952dc00df38a2c28375659b07a3979d22641aeb104751e769c3ee825aadecf", size = 3073806, upload-time = "2025-09-24T13:51:18.712Z" },

+    { url = "https://files.pythonhosted.org/packages/03/83/f768a54af775eb41ef2e7bec8a0a0dbe7d2431c3e78c0a8bdba7ab17e446/shapely-2.1.2-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:1f2f33f486777456586948e333a56ae21f35ae273be99255a191f5c1fa302eb4", size = 3980803, upload-time = "2025-09-24T13:51:20.37Z" },

+    { url = "https://files.pythonhosted.org/packages/9f/cb/559c7c195807c91c79d38a1f6901384a2878a76fbdf3f1048893a9b7534d/shapely-2.1.2-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:cf831a13e0d5a7eb519e96f58ec26e049b1fad411fc6fc23b162a7ce04d9cffc", size = 4133301, upload-time = "2025-09-24T13:51:21.887Z" },

+    { url = "https://files.pythonhosted.org/packages/80/cd/60d5ae203241c53ef3abd2ef27c6800e21afd6c94e39db5315ea0cbafb4a/shapely-2.1.2-cp314-cp314-win32.whl", hash = "sha256:61edcd8d0d17dd99075d320a1dd39c0cb9616f7572f10ef91b4b5b00c4aeb566", size = 1583247, upload-time = "2025-09-24T13:51:23.401Z" },

+    { url = "https://files.pythonhosted.org/packages/74/d4/135684f342e909330e50d31d441ace06bf83c7dc0777e11043f99167b123/shapely-2.1.2-cp314-cp314-win_amd64.whl", hash = "sha256:a444e7afccdb0999e203b976adb37ea633725333e5b119ad40b1ca291ecf311c", size = 1773019, upload-time = "2025-09-24T13:51:24.873Z" },

+    { url = "https://files.pythonhosted.org/packages/a3/05/a44f3f9f695fa3ada22786dc9da33c933da1cbc4bfe876fe3a100bafe263/shapely-2.1.2-cp314-cp314t-macosx_10_13_x86_64.whl", hash = "sha256:5ebe3f84c6112ad3d4632b1fd2290665aa75d4cef5f6c5d77c4c95b324527c6a", size = 1834137, upload-time = "2025-09-24T13:51:26.665Z" },

+    { url = "https://files.pythonhosted.org/packages/52/7e/4d57db45bf314573427b0a70dfca15d912d108e6023f623947fa69f39b72/shapely-2.1.2-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:5860eb9f00a1d49ebb14e881f5caf6c2cf472c7fd38bd7f253bbd34f934eb076", size = 1642884, upload-time = "2025-09-24T13:51:28.029Z" },

+    { url = "https://files.pythonhosted.org/packages/5a/27/4e29c0a55d6d14ad7422bf86995d7ff3f54af0eba59617eb95caf84b9680/shapely-2.1.2-cp314-cp314t-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:b705c99c76695702656327b819c9660768ec33f5ce01fa32b2af62b56ba400a1", size = 3018320, upload-time = "2025-09-24T13:51:29.903Z" },

+    { url = "https://files.pythonhosted.org/packages/9f/bb/992e6a3c463f4d29d4cd6ab8963b75b1b1040199edbd72beada4af46bde5/shapely-2.1.2-cp314-cp314t-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:a1fd0ea855b2cf7c9cddaf25543e914dd75af9de08785f20ca3085f2c9ca60b0", size = 3094931, upload-time = "2025-09-24T13:51:32.699Z" },

+    { url = "https://files.pythonhosted.org/packages/9c/16/82e65e21070e473f0ed6451224ed9fa0be85033d17e0c6e7213a12f59d12/shapely-2.1.2-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:df90e2db118c3671a0754f38e36802db75fe0920d211a27481daf50a711fdf26", size = 4030406, upload-time = "2025-09-24T13:51:34.189Z" },

+    { url = "https://files.pythonhosted.org/packages/7c/75/c24ed871c576d7e2b64b04b1fe3d075157f6eb54e59670d3f5ffb36e25c7/shapely-2.1.2-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:361b6d45030b4ac64ddd0a26046906c8202eb60d0f9f53085f5179f1d23021a0", size = 4169511, upload-time = "2025-09-24T13:51:36.297Z" },

+    { url = "https://files.pythonhosted.org/packages/b1/f7/b3d1d6d18ebf55236eec1c681ce5e665742aab3c0b7b232720a7d43df7b6/shapely-2.1.2-cp314-cp314t-win32.whl", hash = "sha256:b54df60f1fbdecc8ebc2c5b11870461a6417b3d617f555e5033f1505d36e5735", size = 1602607, upload-time = "2025-09-24T13:51:37.757Z" },

+    { url = "https://files.pythonhosted.org/packages/9a/f6/f09272a71976dfc138129b8faf435d064a811ae2f708cb147dccdf7aacdb/shapely-2.1.2-cp314-cp314t-win_amd64.whl", hash = "sha256:0036ac886e0923417932c2e6369b6c52e38e0ff5d9120b90eef5cd9a5fc5cae9", size = 1796682, upload-time = "2025-09-24T13:51:39.233Z" },

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

+    { name = "rasterio", version = "1.4.4", source = { registry = "https://pypi.org/simple" }, marker = "python_full_version < '3.12'" },

+    { name = "rasterio", version = "1.5.0", source = { registry = "https://pypi.org/simple" }, marker = "python_full_version >= '3.12'" },

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
@@ -0,0 +1,47 @@
+from __future__ import annotations

+

+import ast

+from pathlib import Path

+

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

+def imported_modules(source: Path) -> set[str]:

+    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))

+    imports: set[str] = set()

+

+    for node in ast.walk(tree):

+        if isinstance(node, ast.Import):

+            imports.update(alias.name for alias in node.names)

+        elif isinstance(node, ast.ImportFrom) and node.module:

+            imports.add(node.module)

+

+    return imports

+

+

+def test_core_packages_do_not_import_qt_or_editor_modules() -> None:

+    package_root = Path(__file__).parents[2] / "src" / "thucthengay"

+    violations: list[str] = []

+

+    for package_name in sorted(CORE_PACKAGES):

+        for source in (package_root / package_name).rglob("*.py"):

+            for module_name in imported_modules(source):

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
