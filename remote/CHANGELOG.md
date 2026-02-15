# Changelog

## 0.1.0 (2026-02-15)


### Features

* add basic rate limiting using fastapi-limiter ([5347d5d](https://github.com/GlitchDevX/pull-deployment/commit/5347d5d38706df2bc7d09fb9fa702e1cd126e38f))
* add commitSha parameter to only use the exact commit that was created and ignore malicious commits. Also improved client action part ([5e1d0ad](https://github.com/GlitchDevX/pull-deployment/commit/5e1d0ad68c6c858f04a7f8077560547819df7b25))
* add config loading cache ([44330c9](https://github.com/GlitchDevX/pull-deployment/commit/44330c98f2b54982d48021bf5fcf7cae55eb4759))
* add dockerfile ([0eb57b6](https://github.com/GlitchDevX/pull-deployment/commit/0eb57b67563b752038e0a2c524c8bf8b0ad581dd))
* add first unit test case ([b06ab54](https://github.com/GlitchDevX/pull-deployment/commit/b06ab54dc7c045962a8b7134a6e3deb65e01d7e1))
* add more test cases for git and config ([fc53805](https://github.com/GlitchDevX/pull-deployment/commit/fc5380599cf54b615502649410255cde08709012))
* add rate limiter configuration to website deployment config ([270f9ff](https://github.com/GlitchDevX/pull-deployment/commit/270f9ff1d83d99ab32c7cdea6be0223c9cb4a9fe))
* add some test cases for service ([055a159](https://github.com/GlitchDevX/pull-deployment/commit/055a1598600708d71ea9b151ada8c2e9d031b09b))
* add test case for pull with access token & replace deployment_stub fixture with build_stub method ([f396aaa](https://github.com/GlitchDevX/pull-deployment/commit/f396aaafe555d5ae54ce763b7554f5d6a3768ac0))
* implemented git branch pull and config loading ([f9608da](https://github.com/GlitchDevX/pull-deployment/commit/f9608da666247c7a148f6e231de0dea8097c16cd))
* make application more robust ([f3212dd](https://github.com/GlitchDevX/pull-deployment/commit/f3212dd814139f21d5b8c208b8122a20cf5401af))
* remove access token from website deployment body as the token from ci is overprivileged ([e837480](https://github.com/GlitchDevX/pull-deployment/commit/e837480840a0a471ac2621d38d4fa7232ce1becf))


### Bug Fixes

* add and fix test_git commented out assertions ([a5363b2](https://github.com/GlitchDevX/pull-deployment/commit/a5363b2804882ef7d2708a35407cc5ccf9f145ff))
* add missing override option to copytree function ([6b4407e](https://github.com/GlitchDevX/pull-deployment/commit/6b4407e4c644101f59f9cb158bce1d3595c91c05))
* test by providing different path to load_config to not match lru_cache ([ad9ab78](https://github.com/GlitchDevX/pull-deployment/commit/ad9ab78eb348b8eaf1aad07c35d740dbc75f8b07))
