# Changelog

## [v5.0.0](https://github.com/geertmeersman/robonect/tree/v5.0.0) (2025-10-17)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v4.1.0...v5.0.0)

**Closed issues:**

- Error when configuring failed \(but previously working\) Robonect integration: 'RobonectOptionsFlow' object has no attribute 'config\_entry' [\#338](https://github.com/geertmeersman/robonect/issues/338)
- No sum of mowing times [\#317](https://github.com/geertmeersman/robonect/issues/317)

**Merged pull requests:**

- refactor: Refactor RobonectClient to fully async HTTPX with limited concurrency [\#344](https://github.com/geertmeersman/robonect/pull/344) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.13.3 to 0.14.0 [\#343](https://github.com/geertmeersman/robonect/pull/343) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump github/codeql-action from 3 to 4 [\#342](https://github.com/geertmeersman/robonect/pull/342) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.13.2 to 0.13.3 [\#340](https://github.com/geertmeersman/robonect/pull/340) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.13.1 to 0.13.2 [\#339](https://github.com/geertmeersman/robonect/pull/339) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.13.0 to 0.13.1 [\#337](https://github.com/geertmeersman/robonect/pull/337) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v4.1.0](https://github.com/geertmeersman/robonect/tree/v4.1.0) (2025-09-16)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v4.0.0...v4.1.0)

**Closed issues:**

- Robonect integration leaks connections, causing Home Assistant to crash after 2–3 hours [\#334](https://github.com/geertmeersman/robonect/issues/334)

**Merged pull requests:**

- fix: Avoid closing the shared Home Assistant HTTP client to improve stability during reloads/unloads; enhanced error logging and more robust state handling, fixes \#334 [\#335](https://github.com/geertmeersman/robonect/pull/335) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.12.12 to 0.13.0 [\#333](https://github.com/geertmeersman/robonect/pull/333) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v4.0.0](https://github.com/geertmeersman/robonect/tree/v4.0.0) (2025-09-10)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v3.1.0...v4.0.0)

**Closed issues:**

- make wintermode an editable entity [\#331](https://github.com/geertmeersman/robonect/issues/331)
- Home Assistant 2025.8.0b3 issue [\#318](https://github.com/geertmeersman/robonect/issues/318)

**Merged pull requests:**

- feat: add wintermode switch entity \(fixes \#331\) [\#332](https://github.com/geertmeersman/robonect/pull/332) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump actions/setup-python from 5 to 6 [\#330](https://github.com/geertmeersman/robonect/pull/330) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/github-script from 7 to 8 [\#329](https://github.com/geertmeersman/robonect/pull/329) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/stale from 9 to 10 [\#328](https://github.com/geertmeersman/robonect/pull/328) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.11 to 0.12.12 [\#327](https://github.com/geertmeersman/robonect/pull/327) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.10 to 0.12.11 [\#326](https://github.com/geertmeersman/robonect/pull/326) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.9 to 0.12.10 [\#325](https://github.com/geertmeersman/robonect/pull/325) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.8 to 0.12.9 [\#324](https://github.com/geertmeersman/robonect/pull/324) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/checkout from 4 to 5 [\#323](https://github.com/geertmeersman/robonect/pull/323) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.7 to 0.12.8 [\#322](https://github.com/geertmeersman/robonect/pull/322) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v3.1.0](https://github.com/geertmeersman/robonect/tree/v3.1.0) (2025-08-10)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v3.0.0...v3.1.0)

**Merged pull requests:**

- feat: new sensor displaying wire quality and related sensor details, available in diagnostics [\#321](https://github.com/geertmeersman/robonect/pull/321) ([geertmeersman](https://github.com/geertmeersman))

## [v3.0.0](https://github.com/geertmeersman/robonect/tree/v3.0.0) (2025-08-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.4.6...v3.0.0)

**Closed issues:**

- Sensor automower\_mower\_blades\_quality is missing [\#307](https://github.com/geertmeersman/robonect/issues/307)
- Reconnection issue after WiFi loss [\#305](https://github.com/geertmeersman/robonect/issues/305)
- Show battery percentag on Dashboard [\#296](https://github.com/geertmeersman/robonect/issues/296)
- lawn mower entity card with 'mode' state [\#291](https://github.com/geertmeersman/robonect/issues/291)

**Merged pull requests:**

- chore: improved error/debug logging [\#320](https://github.com/geertmeersman/robonect/pull/320) ([geertmeersman](https://github.com/geertmeersman))
- fix: Pass config\_entry explicitly to DataUpdateCoordinator to avoid C… [\#319](https://github.com/geertmeersman/robonect/pull/319) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.12.5 to 0.12.7 [\#316](https://github.com/geertmeersman/robonect/pull/316) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): update pip requirement from \<25.2,\>=8.0.3 to \>=8.0.3,\<25.3 [\#315](https://github.com/geertmeersman/robonect/pull/315) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump hugo19941994/delete-draft-releases from 1.0.1 to 2.0.0 [\#314](https://github.com/geertmeersman/robonect/pull/314) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.4 to 0.12.5 [\#313](https://github.com/geertmeersman/robonect/pull/313) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.3 to 0.12.4 [\#312](https://github.com/geertmeersman/robonect/pull/312) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.2 to 0.12.3 [\#311](https://github.com/geertmeersman/robonect/pull/311) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.1 to 0.12.2 [\#310](https://github.com/geertmeersman/robonect/pull/310) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.12.0 to 0.12.1 [\#309](https://github.com/geertmeersman/robonect/pull/309) ([dependabot[bot]](https://github.com/apps/dependabot))
- docs: note on firmware update refs \#307 [\#308](https://github.com/geertmeersman/robonect/pull/308) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.11.13 to 0.12.0 [\#304](https://github.com/geertmeersman/robonect/pull/304) ([dependabot[bot]](https://github.com/apps/dependabot))
- fix: reduce to 1 commit when releasing [\#303](https://github.com/geertmeersman/robonect/pull/303) ([geertmeersman](https://github.com/geertmeersman))

## [v2.4.6](https://github.com/geertmeersman/robonect/tree/v2.4.6) (2025-06-13)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.4.5...v2.4.6)

**Closed issues:**

- Exception in topic\_received when handling msg [\#299](https://github.com/geertmeersman/robonect/issues/299)

**Merged pull requests:**

- chore: simplify commit in build workflow [\#302](https://github.com/geertmeersman/robonect/pull/302) ([geertmeersman](https://github.com/geertmeersman))
- fix: parse\_duration\_seconds\_to\_minutes takes both string as int as payload now [\#301](https://github.com/geertmeersman/robonect/pull/301) ([geertmeersman](https://github.com/geertmeersman))

## [v2.4.5](https://github.com/geertmeersman/robonect/tree/v2.4.5) (2025-06-13)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.4.4...v2.4.5)

**Merged pull requests:**

- fix: parse\_duration\_seconds\_to\_minutes retaining only the digits refs \#299 [\#300](https://github.com/geertmeersman/robonect/pull/300) ([geertmeersman](https://github.com/geertmeersman))

## [v2.4.4](https://github.com/geertmeersman/robonect/tree/v2.4.4) (2025-06-12)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.4.3...v2.4.4)

**Merged pull requests:**

- fix: translation for lawn mower mode was changed to status\_mode [\#298](https://github.com/geertmeersman/robonect/pull/298) ([geertmeersman](https://github.com/geertmeersman))

## [v2.4.3](https://github.com/geertmeersman/robonect/tree/v2.4.3) (2025-06-12)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.4.2...v2.4.3)

**Closed issues:**

- cannot initialize [\#294](https://github.com/geertmeersman/robonect/issues/294)
- Cannot add Robonect integration via HACS \(dead link\) [\#293](https://github.com/geertmeersman/robonect/issues/293)
- lawn mower entity card - add more commands [\#292](https://github.com/geertmeersman/robonect/issues/292)
- ERROR: numeric value; however, it has the non-numeric value: 'unknown' [\#287](https://github.com/geertmeersman/robonect/issues/287)
- ERROR: Object has no attribute "tzinfo" [\#286](https://github.com/geertmeersman/robonect/issues/286)
- Position as a sensor [\#284](https://github.com/geertmeersman/robonect/issues/284)
- battery extension automover 315X [\#263](https://github.com/geertmeersman/robonect/issues/263)

**Merged pull requests:**

- fix: lawn\_mower entity attributes improvements, refs \#291 [\#297](https://github.com/geertmeersman/robonect/pull/297) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.11.12 to 0.11.13 [\#295](https://github.com/geertmeersman/robonect/pull/295) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.11.11 to 0.11.12 [\#290](https://github.com/geertmeersman/robonect/pull/290) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.11.9 to 0.11.11 [\#285](https://github.com/geertmeersman/robonect/pull/285) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v2.4.2](https://github.com/geertmeersman/robonect/tree/v2.4.2) (2025-05-28)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.4.1...v2.4.2)

**Merged pull requests:**

- fix: Improved the method for extracting numeric values from strings, enhancing accuracy while maintaining the same user-facing behavior [\#289](https://github.com/geertmeersman/robonect/pull/289) ([geertmeersman](https://github.com/geertmeersman))

## [v2.4.1](https://github.com/geertmeersman/robonect/tree/v2.4.1) (2025-05-28)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.4.0...v2.4.1)

**Closed issues:**

- Error "Actie lawn\_mower/dock kan niet worden uitgevoerd. coroutines could not be used with run\_in\_executor\(\)" [\#279](https://github.com/geertmeersman/robonect/issues/279)
- charginbg current gets negative as soon as robonect integration is active [\#265](https://github.com/geertmeersman/robonect/issues/265)

**Merged pull requests:**

- fix: Improved handling of unknown sensor states, ensuring unavailable sensor values are now shown as empty or unavailable [\#288](https://github.com/geertmeersman/robonect/pull/288) ([geertmeersman](https://github.com/geertmeersman))

## [v2.4.0](https://github.com/geertmeersman/robonect/tree/v2.4.0) (2025-05-12)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.3.3...v2.4.0)

**Merged pull requests:**

- feat: binary\_sensor for error status [\#282](https://github.com/geertmeersman/robonect/pull/282) ([geertmeersman](https://github.com/geertmeersman))

## [v2.3.3](https://github.com/geertmeersman/robonect/tree/v2.3.3) (2025-05-12)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.3.2...v2.3.3)

**Closed issues:**

- Closing of HA HTTPx client [\#274](https://github.com/geertmeersman/robonect/issues/274)

**Merged pull requests:**

- fix: async lawn\_mower commands, fixes \#279 [\#281](https://github.com/geertmeersman/robonect/pull/281) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.11.8 to 0.11.9 [\#280](https://github.com/geertmeersman/robonect/pull/280) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.11.7 to 0.11.8 [\#277](https://github.com/geertmeersman/robonect/pull/277) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v2.3.2](https://github.com/geertmeersman/robonect/tree/v2.3.2) (2025-05-02)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.3.1...v2.3.2)

**Closed issues:**

- Two Robonect Mowers: Service Call "Direct the Mower" controls only one correctly [\#268](https://github.com/geertmeersman/robonect/issues/268)
- Add action for "blades replaced" [\#266](https://github.com/geertmeersman/robonect/issues/266)

**Merged pull requests:**

- fix: don't close the Home Assistant httpx client, refs \#274 [\#275](https://github.com/geertmeersman/robonect/pull/275) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.11.5 to 0.11.7 [\#273](https://github.com/geertmeersman/robonect/pull/273) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): update pip requirement from \<25.1,\>=8.0.3 to \>=8.0.3,\<25.2 [\#272](https://github.com/geertmeersman/robonect/pull/272) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v2.3.1](https://github.com/geertmeersman/robonect/tree/v2.3.1) (2025-04-18)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.3.0...v2.3.1)

**Merged pull requests:**

- fix: retrieve config entry based on entity\_id so service calls go to the right hub client, refs \#268 [\#270](https://github.com/geertmeersman/robonect/pull/270) ([geertmeersman](https://github.com/geertmeersman))

## [v2.3.0](https://github.com/geertmeersman/robonect/tree/v2.3.0) (2025-04-17)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.2.0...v2.3.0)

**Merged pull requests:**

- fix: client connection handling to improve reliability by managing HTTP client instances individually for each mower, refs \#268 [\#269](https://github.com/geertmeersman/robonect/pull/269) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.11.2 to 0.11.5 [\#267](https://github.com/geertmeersman/robonect/pull/267) ([dependabot[bot]](https://github.com/apps/dependabot))
- fix: remove general\_settings [\#262](https://github.com/geertmeersman/robonect/pull/262) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.9.9 to 0.11.2 [\#261](https://github.com/geertmeersman/robonect/pull/261) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v2.2.0](https://github.com/geertmeersman/robonect/tree/v2.2.0) (2025-03-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.1.1...v2.2.0)

**Closed issues:**

- Time shift of one hours [\#256](https://github.com/geertmeersman/robonect/issues/256)
- Question about the MQTT topic [\#253](https://github.com/geertmeersman/robonect/issues/253)
- Log error "object has no attribute '\_\_attr\_extra\_state\_attributes'." [\#240](https://github.com/geertmeersman/robonect/issues/240)

**Merged pull requests:**

- fix: ensure accurate local time displays [\#258](https://github.com/geertmeersman/robonect/pull/258) ([geertmeersman](https://github.com/geertmeersman))
- fix: unix\_to\_datetime shift [\#257](https://github.com/geertmeersman/robonect/pull/257) ([poggenpower](https://github.com/poggenpower))
- build\(deps\): bump ruff from 0.9.7 to 0.9.9 [\#255](https://github.com/geertmeersman/robonect/pull/255) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.9.3 to 0.9.7 [\#254](https://github.com/geertmeersman/robonect/pull/254) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): update pip requirement from \<24.4,\>=8.0.3 to \>=8.0.3,\<25.1 [\#249](https://github.com/geertmeersman/robonect/pull/249) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.8.6 to 0.9.3 [\#248](https://github.com/geertmeersman/robonect/pull/248) ([dependabot[bot]](https://github.com/apps/dependabot))
- chore: github sync dev-current workflow [\#245](https://github.com/geertmeersman/robonect/pull/245) ([geertmeersman](https://github.com/geertmeersman))
- chore: spellcheck [\#244](https://github.com/geertmeersman/robonect/pull/244) ([geertmeersman](https://github.com/geertmeersman))

## [v2.1.1](https://github.com/geertmeersman/robonect/tree/v2.1.1) (2025-01-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.1.0...v2.1.1)

**Merged pull requests:**

- fix: New options flow properties [\#243](https://github.com/geertmeersman/robonect/pull/243) ([geertmeersman](https://github.com/geertmeersman))

## [v2.1.0](https://github.com/geertmeersman/robonect/tree/v2.1.0) (2025-01-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.0.5...v2.1.0)

**Closed issues:**

- mower\_mode? [\#230](https://github.com/geertmeersman/robonect/issues/230)
- Winter mode [\#224](https://github.com/geertmeersman/robonect/issues/224)

**Merged pull requests:**

- fix: RobonectRestSwitch AttributeError when mower was disconnected [\#242](https://github.com/geertmeersman/robonect/pull/242) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.8.4 to 0.8.6 [\#241](https://github.com/geertmeersman/robonect/pull/241) ([dependabot[bot]](https://github.com/apps/dependabot))
- fix: pretty-format-json [\#239](https://github.com/geertmeersman/robonect/pull/239) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.8.3 to 0.8.4 [\#238](https://github.com/geertmeersman/robonect/pull/238) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.8.2 to 0.8.3 [\#237](https://github.com/geertmeersman/robonect/pull/237) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.8.0 to 0.8.2 [\#236](https://github.com/geertmeersman/robonect/pull/236) ([dependabot[bot]](https://github.com/apps/dependabot))
- fix: github workflow delete pre-releases on release [\#234](https://github.com/geertmeersman/robonect/pull/234) ([geertmeersman](https://github.com/geertmeersman))
- fix: beta release zip file [\#233](https://github.com/geertmeersman/robonect/pull/233) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.7.4 to 0.8.0 [\#232](https://github.com/geertmeersman/robonect/pull/232) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.7.3 to 0.7.4 [\#231](https://github.com/geertmeersman/robonect/pull/231) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.7.2 to 0.7.3 [\#229](https://github.com/geertmeersman/robonect/pull/229) ([dependabot[bot]](https://github.com/apps/dependabot))
- chore: zip\_release for hacs [\#228](https://github.com/geertmeersman/robonect/pull/228) ([geertmeersman](https://github.com/geertmeersman))
- docs: release template [\#227](https://github.com/geertmeersman/robonect/pull/227) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.7.1 to 0.7.2 [\#226](https://github.com/geertmeersman/robonect/pull/226) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump colorlog from 6.8.2 to 6.9.0 [\#225](https://github.com/geertmeersman/robonect/pull/225) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): update pip requirement from \<24.3,\>=8.0.3 to \>=8.0.3,\<24.4 [\#223](https://github.com/geertmeersman/robonect/pull/223) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.7.0 to 0.7.1 [\#222](https://github.com/geertmeersman/robonect/pull/222) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.6.9 to 0.7.0 [\#221](https://github.com/geertmeersman/robonect/pull/221) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v2.0.5](https://github.com/geertmeersman/robonect/tree/v2.0.5) (2024-10-18)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.0.4...v2.0.5)

**Closed issues:**

- Mower keeps waking up and getting back to sleep [\#218](https://github.com/geertmeersman/robonect/issues/218)

**Merged pull requests:**

- fix: read timeout errors in the logs moved to debug [\#220](https://github.com/geertmeersman/robonect/pull/220) ([geertmeersman](https://github.com/geertmeersman))

## [v2.0.4](https://github.com/geertmeersman/robonect/tree/v2.0.4) (2024-10-16)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.0.3...v2.0.4)

**Merged pull requests:**

- fix: don't call gps command when sleeping [\#219](https://github.com/geertmeersman/robonect/pull/219) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace template corrections for binary\_sensors [\#217](https://github.com/geertmeersman/robonect/pull/217) ([geertmeersman](https://github.com/geertmeersman))

## [v2.0.3](https://github.com/geertmeersman/robonect/tree/v2.0.3) (2024-10-10)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.0.2...v2.0.3)

**Closed issues:**

- error: exception [\#214](https://github.com/geertmeersman/robonect/issues/214)
- ON/OFF switches for OUT 1 & OUT 2 [\#195](https://github.com/geertmeersman/robonect/issues/195)

**Merged pull requests:**

- fix: read safe json commands while mower is sleeping [\#216](https://github.com/geertmeersman/robonect/pull/216) ([geertmeersman](https://github.com/geertmeersman))

## [v2.0.2](https://github.com/geertmeersman/robonect/tree/v2.0.2) (2024-10-09)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.0.1...v2.0.2)

**Closed issues:**

- Entity State in Condition not working [\#207](https://github.com/geertmeersman/robonect/issues/207)

**Merged pull requests:**

- fix: add timeout of 20 seconds to httpx client, refers to \#214 [\#215](https://github.com/geertmeersman/robonect/pull/215) ([geertmeersman](https://github.com/geertmeersman))

## [v2.0.1](https://github.com/geertmeersman/robonect/tree/v2.0.1) (2024-10-08)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v2.0.0...v2.0.1)

**Closed issues:**

- The Lovelace example uses vacuum entity, which does not exist after 2.0.0 [\#211](https://github.com/geertmeersman/robonect/issues/211)
- Detected blocking call to load\_verify\_locations [\#208](https://github.com/geertmeersman/robonect/issues/208)

**Merged pull requests:**

- fix: async for blocking file system operations [\#213](https://github.com/geertmeersman/robonect/pull/213) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace card change vacuum to lawn\_mower [\#212](https://github.com/geertmeersman/robonect/pull/212) ([geertmeersman](https://github.com/geertmeersman))

## [v2.0.0](https://github.com/geertmeersman/robonect/tree/v2.0.0) (2024-10-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.9.1...v2.0.0)

**Closed issues:**

- Feature request [\#194](https://github.com/geertmeersman/robonect/issues/194)
- Home Assistant Color for status \(sleepling - mowing\) [\#190](https://github.com/geertmeersman/robonect/issues/190)

**Merged pull requests:**

- feat: switches for equipment, vacuum removed, states changed for lawn… [\#210](https://github.com/geertmeersman/robonect/pull/210) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.6.8 to 0.6.9 [\#209](https://github.com/geertmeersman/robonect/pull/209) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.9.1](https://github.com/geertmeersman/robonect/tree/v1.9.1) (2024-09-30)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.9.0...v1.9.1)

**Closed issues:**

- Timeout check on 'Direct the mower' -service. [\#205](https://github.com/geertmeersman/robonect/issues/205)
- Send 'Joystick'-commands to robonnect [\#197](https://github.com/geertmeersman/robonect/issues/197)

**Merged pull requests:**

- fix: limit direct service timeout to 5000ms, fixes \#205 [\#206](https://github.com/geertmeersman/robonect/pull/206) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.6.7 to 0.6.8 [\#204](https://github.com/geertmeersman/robonect/pull/204) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.9.0](https://github.com/geertmeersman/robonect/tree/v1.9.0) (2024-09-27)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.8.0...v1.9.0)

**Merged pull requests:**

- fix: removed new lines from translations [\#203](https://github.com/geertmeersman/robonect/pull/203) ([geertmeersman](https://github.com/geertmeersman))
- feat: direct command service, refers to \#197 and \#194 [\#202](https://github.com/geertmeersman/robonect/pull/202) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.6.5 to 0.6.7 [\#201](https://github.com/geertmeersman/robonect/pull/201) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.6.4 to 0.6.5 [\#200](https://github.com/geertmeersman/robonect/pull/200) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.6.2 to 0.6.4 [\#199](https://github.com/geertmeersman/robonect/pull/199) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.5.4 to 0.6.2 [\#196](https://github.com/geertmeersman/robonect/pull/196) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): update pip requirement from \<24.2,\>=8.0.3 to \>=8.0.3,\<24.3 [\#189](https://github.com/geertmeersman/robonect/pull/189) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.8.0](https://github.com/geertmeersman/robonect/tree/v1.8.0) (2024-07-26)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.7.3...v1.8.0)

**Closed issues:**

-  Error message during integration, Error doing job: Future exception was never retrieved \(None\) [\#184](https://github.com/geertmeersman/robonect/issues/184)

**Merged pull requests:**

- feat: add reset mower blades button [\#187](https://github.com/geertmeersman/robonect/pull/187) ([geertmeersman](https://github.com/geertmeersman))

## [v1.7.3](https://github.com/geertmeersman/robonect/tree/v1.7.3) (2024-07-26)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.7.2...v1.7.3)

**Closed issues:**

- Unable to place mowing job [\#180](https://github.com/geertmeersman/robonect/issues/180)

**Merged pull requests:**

- fix: threadsafe update\_ha\_state, references \#184 [\#186](https://github.com/geertmeersman/robonect/pull/186) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.5.1 to 0.5.4 [\#185](https://github.com/geertmeersman/robonect/pull/185) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.7.2](https://github.com/geertmeersman/robonect/tree/v1.7.2) (2024-07-09)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.7.1...v1.7.2)

**Closed issues:**

- Blocking call [\#171](https://github.com/geertmeersman/robonect/issues/171)

**Merged pull requests:**

- fix: httpx error message, references \#180 [\#182](https://github.com/geertmeersman/robonect/pull/182) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.5.0 to 0.5.1 [\#181](https://github.com/geertmeersman/robonect/pull/181) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.4.10 to 0.5.0 [\#179](https://github.com/geertmeersman/robonect/pull/179) ([dependabot[bot]](https://github.com/apps/dependabot))
- docs: Sensor templates for lovelace [\#178](https://github.com/geertmeersman/robonect/pull/178) ([geertmeersman](https://github.com/geertmeersman))
- docs: Lovelace card yaml  updated + screenshot [\#177](https://github.com/geertmeersman/robonect/pull/177) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.4.9 to 0.4.10 [\#176](https://github.com/geertmeersman/robonect/pull/176) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): update pip requirement from \<24.1,\>=8.0.3 to \>=8.0.3,\<24.2 [\#175](https://github.com/geertmeersman/robonect/pull/175) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.7.1](https://github.com/geertmeersman/robonect/tree/v1.7.1) (2024-06-21)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.7.0...v1.7.1)

**Merged pull requests:**

- fix: concurrency for validat workflow [\#174](https://github.com/geertmeersman/robonect/pull/174) ([geertmeersman](https://github.com/geertmeersman))
- fix: blocking call for timezone fetching, references \#171 [\#173](https://github.com/geertmeersman/robonect/pull/173) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.4.8 to 0.4.9 [\#172](https://github.com/geertmeersman/robonect/pull/172) ([dependabot[bot]](https://github.com/apps/dependabot))
- docs: yaml markdown [\#170](https://github.com/geertmeersman/robonect/pull/170) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.4.7 to 0.4.8 [\#169](https://github.com/geertmeersman/robonect/pull/169) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.7.0](https://github.com/geertmeersman/robonect/tree/v1.7.0) (2024-06-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.10...v1.7.0)

**Merged pull requests:**

- feat: sensor application version [\#168](https://github.com/geertmeersman/robonect/pull/168) ([geertmeersman](https://github.com/geertmeersman))

## [v1.6.10](https://github.com/geertmeersman/robonect/tree/v1.6.10) (2024-06-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.9...v1.6.10)

**Closed issues:**

- Exception 'NoneType' object has no attribute 'items' [\#162](https://github.com/geertmeersman/robonect/issues/162)

**Merged pull requests:**

- fix: bump aiorobonect to catch incorrect robonect json [\#167](https://github.com/geertmeersman/robonect/pull/167) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.4.5 to 0.4.7 [\#166](https://github.com/geertmeersman/robonect/pull/166) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.6.9](https://github.com/geertmeersman/robonect/tree/v1.6.9) (2024-05-29)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.8...v1.6.9)

**Merged pull requests:**

- fix: move warnings on requesterrors to debug, bump aiorobonect [\#165](https://github.com/geertmeersman/robonect/pull/165) ([geertmeersman](https://github.com/geertmeersman))

## [v1.6.8](https://github.com/geertmeersman/robonect/tree/v1.6.8) (2024-05-28)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.7...v1.6.8)

**Merged pull requests:**

- fix: throw requesterror when response is none, bump aiorobonect [\#164](https://github.com/geertmeersman/robonect/pull/164) ([geertmeersman](https://github.com/geertmeersman))

## [v1.6.7](https://github.com/geertmeersman/robonect/tree/v1.6.7) (2024-05-28)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.6...v1.6.7)

**Closed issues:**

- Status entity general error [\#157](https://github.com/geertmeersman/robonect/issues/157)

**Merged pull requests:**

- Refactor: Rename translation of health\_voltage\_batt to Robonect supply voltage [\#163](https://github.com/geertmeersman/robonect/pull/163) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.4.4 to 0.4.5 [\#161](https://github.com/geertmeersman/robonect/pull/161) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.6.6](https://github.com/geertmeersman/robonect/tree/v1.6.6) (2024-05-24)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.5...v1.6.6)

**Closed issues:**

- Unable to connect to mower/cloud [\#158](https://github.com/geertmeersman/robonect/issues/158)

**Merged pull requests:**

- fix: only switch to https scheme on a redirect \(3xx\) or connection error [\#160](https://github.com/geertmeersman/robonect/pull/160) ([geertmeersman](https://github.com/geertmeersman))

## [v1.6.5](https://github.com/geertmeersman/robonect/tree/v1.6.5) (2024-05-23)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.4...v1.6.5)

**Merged pull requests:**

- fix: take https scheme into account [\#159](https://github.com/geertmeersman/robonect/pull/159) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.4.3 to 0.4.4 [\#156](https://github.com/geertmeersman/robonect/pull/156) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.6.4](https://github.com/geertmeersman/robonect/tree/v1.6.4) (2024-05-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.3...v1.6.4)

**Merged pull requests:**

- fix: bump aiorobonect version [\#155](https://github.com/geertmeersman/robonect/pull/155) ([geertmeersman](https://github.com/geertmeersman))

## [v1.6.3](https://github.com/geertmeersman/robonect/tree/v1.6.3) (2024-05-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.2...v1.6.3)

**Closed issues:**

- Exception 0 warnings [\#152](https://github.com/geertmeersman/robonect/issues/152)
- No "Reset error" button  [\#151](https://github.com/geertmeersman/robonect/issues/151)
- Error adding entity binary\_sensor.robonect\_health\_alarm for domain binary\_sensor with platform robonect [\#145](https://github.com/geertmeersman/robonect/issues/145)

**Merged pull requests:**

- fix: replace aiohttp by httpx, fixes \#152 [\#154](https://github.com/geertmeersman/robonect/pull/154) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.4.2 to 0.4.3 [\#153](https://github.com/geertmeersman/robonect/pull/153) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.4.1 to 0.4.2 [\#150](https://github.com/geertmeersman/robonect/pull/150) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.3.7 to 0.4.1 [\#149](https://github.com/geertmeersman/robonect/pull/149) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.6.2](https://github.com/geertmeersman/robonect/tree/v1.6.2) (2024-04-15)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.1...v1.6.2)

**Merged pull requests:**

- fix: improvement for wifi % calculation [\#148](https://github.com/geertmeersman/robonect/pull/148) ([geertmeersman](https://github.com/geertmeersman))

## [v1.6.1](https://github.com/geertmeersman/robonect/tree/v1.6.1) (2024-04-15)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.6.0...v1.6.1)

**Closed issues:**

- Wrong "status\_plain" after Winter [\#144](https://github.com/geertmeersman/robonect/issues/144)

**Merged pull requests:**

- fix: state check for binary sensor, references \#145 [\#147](https://github.com/geertmeersman/robonect/pull/147) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.3.4 to 0.3.7 [\#146](https://github.com/geertmeersman/robonect/pull/146) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.6.0](https://github.com/geertmeersman/robonect/tree/v1.6.0) (2024-03-28)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.5.4...v1.6.0)

**Closed issues:**

- Sensors OK, Mower does not respond to commands from HASS [\#138](https://github.com/geertmeersman/robonect/issues/138)
- Duplicate battery sensor [\#127](https://github.com/geertmeersman/robonect/issues/127)
- TEMP\_CELSIUS used by robonect is a deprecated constant [\#121](https://github.com/geertmeersman/robonect/issues/121)

**Merged pull requests:**

- fix: icons.json for services/hassfest [\#142](https://github.com/geertmeersman/robonect/pull/142) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.3.3 to 0.3.4 [\#141](https://github.com/geertmeersman/robonect/pull/141) ([dependabot[bot]](https://github.com/apps/dependabot))
- refactor: improve github workflows [\#140](https://github.com/geertmeersman/robonect/pull/140) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.3.2 to 0.3.3 [\#139](https://github.com/geertmeersman/robonect/pull/139) ([dependabot[bot]](https://github.com/apps/dependabot))
- docs: bug\_report markdown [\#137](https://github.com/geertmeersman/robonect/pull/137) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.3.0 to 0.3.2 [\#136](https://github.com/geertmeersman/robonect/pull/136) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.2.2 to 0.3.0 [\#135](https://github.com/geertmeersman/robonect/pull/135) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.2.1 to 0.2.2 [\#134](https://github.com/geertmeersman/robonect/pull/134) ([dependabot[bot]](https://github.com/apps/dependabot))
- refactor: lint [\#133](https://github.com/geertmeersman/robonect/pull/133) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.2.0 to 0.2.1 [\#132](https://github.com/geertmeersman/robonect/pull/132) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): update pip requirement from \<23.4,\>=8.0.3 to \>=8.0.3,\<24.1 [\#131](https://github.com/geertmeersman/robonect/pull/131) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.1.14 to 0.2.0 [\#130](https://github.com/geertmeersman/robonect/pull/130) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump release-drafter/release-drafter from 5 to 6 [\#129](https://github.com/geertmeersman/robonect/pull/129) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump colorlog from 6.8.0 to 6.8.2 [\#128](https://github.com/geertmeersman/robonect/pull/128) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.1.13 to 0.1.14 [\#126](https://github.com/geertmeersman/robonect/pull/126) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/dependency-review-action from 3 to 4 [\#125](https://github.com/geertmeersman/robonect/pull/125) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.1.11 to 0.1.13 [\#124](https://github.com/geertmeersman/robonect/pull/124) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.1.9 to 0.1.11 [\#123](https://github.com/geertmeersman/robonect/pull/123) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.5.4](https://github.com/geertmeersman/robonect/tree/v1.5.4) (2024-01-04)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.5.3...v1.5.4)

**Closed issues:**

- Disabling while offline in winter mode [\#109](https://github.com/geertmeersman/robonect/issues/109)
- Restore entities at restart when mower is unavailable? [\#88](https://github.com/geertmeersman/robonect/issues/88)

**Merged pull requests:**

- fix: Deprecated units, references \#121 [\#122](https://github.com/geertmeersman/robonect/pull/122) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.1.8 to 0.1.9 [\#120](https://github.com/geertmeersman/robonect/pull/120) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.5.3](https://github.com/geertmeersman/robonect/tree/v1.5.3) (2023-12-19)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.5.2...v1.5.3)

**Merged pull requests:**

- fix: ignore connection issues [\#119](https://github.com/geertmeersman/robonect/pull/119) ([geertmeersman](https://github.com/geertmeersman))

## [v1.5.2](https://github.com/geertmeersman/robonect/tree/v1.5.2) (2023-12-19)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.5.1...v1.5.2)

**Merged pull requests:**

- build\(deps\): bump ruff from 0.1.7 to 0.1.8 [\#118](https://github.com/geertmeersman/robonect/pull/118) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/upload-artifact from 3 to 4 [\#117](https://github.com/geertmeersman/robonect/pull/117) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump github/codeql-action from 2 to 3 [\#116](https://github.com/geertmeersman/robonect/pull/116) ([dependabot[bot]](https://github.com/apps/dependabot))
- feat: Winter mode and data store, references \#88, \#109 [\#115](https://github.com/geertmeersman/robonect/pull/115) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.1.6 to 0.1.7 [\#114](https://github.com/geertmeersman/robonect/pull/114) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump heinrichreimer/github-changelog-generator-action from 2.3 to 2.4 [\#113](https://github.com/geertmeersman/robonect/pull/113) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/setup-python from 4.7.1 to 5.0.0 [\#112](https://github.com/geertmeersman/robonect/pull/112) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/stale from 8 to 9 [\#111](https://github.com/geertmeersman/robonect/pull/111) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.5.1](https://github.com/geertmeersman/robonect/tree/v1.5.1) (2023-12-10)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.5.0...v1.5.1)

**Merged pull requests:**

- fix: remove exceptions when mower not available through rest. referen… [\#110](https://github.com/geertmeersman/robonect/pull/110) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump colorlog from 6.7.0 to 6.8.0 [\#108](https://github.com/geertmeersman/robonect/pull/108) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.5.0](https://github.com/geertmeersman/robonect/tree/v1.5.0) (2023-11-25)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.4.2...v1.5.0)

**Merged pull requests:**

- fix: config flow fix [\#107](https://github.com/geertmeersman/robonect/pull/107) ([geertmeersman](https://github.com/geertmeersman))
- fix: move release zip [\#106](https://github.com/geertmeersman/robonect/pull/106) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.1.5 to 0.1.6 [\#105](https://github.com/geertmeersman/robonect/pull/105) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/upload-artifact from 2 to 3 [\#104](https://github.com/geertmeersman/robonect/pull/104) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/github-script from 6 to 7 [\#103](https://github.com/geertmeersman/robonect/pull/103) ([dependabot[bot]](https://github.com/apps/dependabot))
- fix: Release workflow - remove path from zip [\#102](https://github.com/geertmeersman/robonect/pull/102) ([geertmeersman](https://github.com/geertmeersman))
- fix: add version tag in commits [\#101](https://github.com/geertmeersman/robonect/pull/101) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.1.4 to 0.1.5 [\#100](https://github.com/geertmeersman/robonect/pull/100) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.1.3 to 0.1.4 [\#99](https://github.com/geertmeersman/robonect/pull/99) ([dependabot[bot]](https://github.com/apps/dependabot))
- fix: Bump Python and HA [\#98](https://github.com/geertmeersman/robonect/pull/98) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.0.292 to 0.1.3 [\#97](https://github.com/geertmeersman/robonect/pull/97) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.4.2](https://github.com/geertmeersman/robonect/tree/v1.4.2) (2023-10-17)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.4.1...v1.4.2)

**Merged pull requests:**

- fix: binary sensor, change init order for RobonectBinarySensor and co… [\#95](https://github.com/geertmeersman/robonect/pull/95) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): update pip requirement from \<23.3,\>=8.0.3 to \>=8.0.3,\<23.4 [\#94](https://github.com/geertmeersman/robonect/pull/94) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.4.1](https://github.com/geertmeersman/robonect/tree/v1.4.1) (2023-10-14)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.4.0...v1.4.1)

**Closed issues:**

- Extra info missing for mower [\#90](https://github.com/geertmeersman/robonect/issues/90)

**Merged pull requests:**

- fix: switch error removed when only mqtt is enabled [\#93](https://github.com/geertmeersman/robonect/pull/93) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.0.291 to 0.0.292 [\#92](https://github.com/geertmeersman/robonect/pull/92) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/setup-python from 4.7.0 to 4.7.1 [\#91](https://github.com/geertmeersman/robonect/pull/91) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.4.0](https://github.com/geertmeersman/robonect/tree/v1.4.0) (2023-10-03)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.3.1...v1.4.0)

**Merged pull requests:**

- feat: weather service added [\#89](https://github.com/geertmeersman/robonect/pull/89) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.0.290 to 0.0.291 [\#87](https://github.com/geertmeersman/robonect/pull/87) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.3.1](https://github.com/geertmeersman/robonect/tree/v1.3.1) (2023-09-23)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.3.0...v1.3.1)

**Merged pull requests:**

- deps: bump aiorobonect [\#86](https://github.com/geertmeersman/robonect/pull/86) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.0.287 to 0.0.290 [\#85](https://github.com/geertmeersman/robonect/pull/85) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/checkout from 3 to 4 [\#84](https://github.com/geertmeersman/robonect/pull/84) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.3.0](https://github.com/geertmeersman/robonect/tree/v1.3.0) (2023-09-09)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.3.1-beta.2...v1.3.0)

**Merged pull requests:**

- feat: lawn\_mower platform added [\#83](https://github.com/geertmeersman/robonect/pull/83) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.0.286 to 0.0.287 [\#82](https://github.com/geertmeersman/robonect/pull/82) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.3.1-beta.2](https://github.com/geertmeersman/robonect/tree/v1.3.1-beta.2) (2023-09-04)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.2.1...v1.3.1-beta.2)

**Closed issues:**

- New entity type lawnmower [\#81](https://github.com/geertmeersman/robonect/issues/81)

## [v1.2.1](https://github.com/geertmeersman/robonect/tree/v1.2.1) (2023-08-31)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.2.0...v1.2.1)

**Merged pull requests:**

- fix: names added for service fields [\#80](https://github.com/geertmeersman/robonect/pull/80) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.0.285 to 0.0.286 [\#79](https://github.com/geertmeersman/robonect/pull/79) ([dependabot[bot]](https://github.com/apps/dependabot))
- docs: finally merged into HACS default [\#78](https://github.com/geertmeersman/robonect/pull/78) ([geertmeersman](https://github.com/geertmeersman))
- fix: hex2weekdays, D400 First line should end with a period [\#77](https://github.com/geertmeersman/robonect/pull/77) ([geertmeersman](https://github.com/geertmeersman))

## [v1.2.0](https://github.com/geertmeersman/robonect/tree/v1.2.0) (2023-08-25)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.2.0-beta.5...v1.2.0)

**Documentation:**

- doc: Document REST API username/password [\#74](https://github.com/geertmeersman/robonect/pull/74) ([pdecat](https://github.com/pdecat))

**Closed issues:**

- Option to change timers without entering the whole config \(enable/disable\) [\#69](https://github.com/geertmeersman/robonect/issues/69)

**Merged pull requests:**

- feat: switch entity for timers. Replaces timer sensors, fixes \#69 [\#76](https://github.com/geertmeersman/robonect/pull/76) ([geertmeersman](https://github.com/geertmeersman))
- fix: timer ID correction in services, fixes \#68 [\#75](https://github.com/geertmeersman/robonect/pull/75) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.0.278 to 0.0.285 [\#72](https://github.com/geertmeersman/robonect/pull/72) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.2.0-beta.5](https://github.com/geertmeersman/robonect/tree/v1.2.0-beta.5) (2023-08-25)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.1.0...v1.2.0-beta.5)

**Closed issues:**

- Robonect V1.1.0 only 35 entity; vacuum missing [\#73](https://github.com/geertmeersman/robonect/issues/73)
- Changing timer from Service Call fail [\#68](https://github.com/geertmeersman/robonect/issues/68)
- values unavail if/when spotty wifi [\#65](https://github.com/geertmeersman/robonect/issues/65)

## [v1.1.0](https://github.com/geertmeersman/robonect/tree/v1.1.0) (2023-07-19)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.1.13-beta.13...v1.1.0)

**Merged pull requests:**

- fix: don't update when timeout & vacuum mqtt commands [\#66](https://github.com/geertmeersman/robonect/pull/66) ([geertmeersman](https://github.com/geertmeersman))

## [v1.1.13-beta.13](https://github.com/geertmeersman/robonect/tree/v1.1.13-beta.13) (2023-07-17)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.14-beta.2...v1.1.13-beta.13)

**Merged pull requests:**

- build\(deps\): update pip requirement from \<23.2,\>=8.0.3 to \>=8.0.3,\<23.3 [\#64](https://github.com/geertmeersman/robonect/pull/64) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump ruff from 0.0.275 to 0.0.278 [\#63](https://github.com/geertmeersman/robonect/pull/63) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/setup-python from 4.6.1 to 4.7.0 [\#62](https://github.com/geertmeersman/robonect/pull/62) ([dependabot[bot]](https://github.com/apps/dependabot))
- fix: added case sensitive remark to config flow [\#60](https://github.com/geertmeersman/robonect/pull/60) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.14-beta.2](https://github.com/geertmeersman/robonect/tree/v1.0.14-beta.2) (2023-07-09)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.13...v1.0.14-beta.2)

## [v1.0.13](https://github.com/geertmeersman/robonect/tree/v1.0.13) (2023-07-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.12...v1.0.13)

**Closed issues:**

- Robonect not working with HA 2023.7 ? [\#56](https://github.com/geertmeersman/robonect/issues/56)

**Merged pull requests:**

- fix: added missing translations, fixing 'implicitly using device name… [\#59](https://github.com/geertmeersman/robonect/pull/59) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace card to start the mower again when stopped [\#58](https://github.com/geertmeersman/robonect/pull/58) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.12](https://github.com/geertmeersman/robonect/tree/v1.0.12) (2023-07-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.11...v1.0.12)

**Merged pull requests:**

- fix: HA 2023.7 release fix, references \#56 [\#57](https://github.com/geertmeersman/robonect/pull/57) ([geertmeersman](https://github.com/geertmeersman))
- build\(deps\): bump ruff from 0.0.272 to 0.0.275 [\#55](https://github.com/geertmeersman/robonect/pull/55) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.11](https://github.com/geertmeersman/robonect/tree/v1.0.11) (2023-06-21)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.10...v1.0.11)

**Merged pull requests:**

- fix: add jsonpath dependency [\#54](https://github.com/geertmeersman/robonect/pull/54) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.10](https://github.com/geertmeersman/robonect/tree/v1.0.10) (2023-06-18)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.9...v1.0.10)

**Merged pull requests:**

- fix: bump aiorobonect to 0.2.5 [\#53](https://github.com/geertmeersman/robonect/pull/53) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.9](https://github.com/geertmeersman/robonect/tree/v1.0.9) (2023-06-18)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.8...v1.0.9)

**Merged pull requests:**

- fix: bump aiorobonect to 0.2.4 [\#52](https://github.com/geertmeersman/robonect/pull/52) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.8](https://github.com/geertmeersman/robonect/tree/v1.0.8) (2023-06-18)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.8-beta.18...v1.0.8)

**Merged pull requests:**

- fix: bump aiorobonect version [\#51](https://github.com/geertmeersman/robonect/pull/51) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.8-beta.18](https://github.com/geertmeersman/robonect/tree/v1.0.8-beta.18) (2023-06-18)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.8-beta.17...v1.0.8-beta.18)

## [v1.0.8-beta.17](https://github.com/geertmeersman/robonect/tree/v1.0.8-beta.17) (2023-06-18)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.8-beta.14...v1.0.8-beta.17)

**Merged pull requests:**

- Create FUNDING.yml [\#49](https://github.com/geertmeersman/robonect/pull/49) ([geertmeersman](https://github.com/geertmeersman))
- refactor: only validate custom\_component changes [\#48](https://github.com/geertmeersman/robonect/pull/48) ([geertmeersman](https://github.com/geertmeersman))
- refactor: workflow names [\#47](https://github.com/geertmeersman/robonect/pull/47) ([geertmeersman](https://github.com/geertmeersman))
- fix: Change bump workflow names [\#46](https://github.com/geertmeersman/robonect/pull/46) ([geertmeersman](https://github.com/geertmeersman))
- refactor: Workflows [\#45](https://github.com/geertmeersman/robonect/pull/45) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.8-beta.14](https://github.com/geertmeersman/robonect/tree/v1.0.8-beta.14) (2023-06-18)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.7...v1.0.8-beta.14)

**Closed issues:**

- Can't add integration \(module 'homeassistant.components.mqtt' has no attribute 'async\_wait\_for\_mqtt\_client'\) [\#50](https://github.com/geertmeersman/robonect/issues/50)

**Merged pull requests:**

- build\(deps\): bump ruff from 0.0.270 to 0.0.272 [\#44](https://github.com/geertmeersman/robonect/pull/44) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v1.0.7](https://github.com/geertmeersman/robonect/tree/v1.0.7) (2023-06-10)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.6...v1.0.7)

**Merged pull requests:**

- fix: RuntimeWarning: coroutine 'RobonectClient.state' was never awaited [\#43](https://github.com/geertmeersman/robonect/pull/43) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.6](https://github.com/geertmeersman/robonect/tree/v1.0.6) (2023-06-08)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.5...v1.0.6)

**Merged pull requests:**

- fix: Attributes - copy as they get updated multiple times & capitals in timer attributes [\#42](https://github.com/geertmeersman/robonect/pull/42) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.5](https://github.com/geertmeersman/robonect/tree/v1.0.5) (2023-06-08)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.5-beta.3...v1.0.5)

**Merged pull requests:**

- fix: await coroutine state [\#41](https://github.com/geertmeersman/robonect/pull/41) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.5-beta.3](https://github.com/geertmeersman/robonect/tree/v1.0.5-beta.3) (2023-06-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.4...v1.0.5-beta.3)

## [v1.0.4](https://github.com/geertmeersman/robonect/tree/v1.0.4) (2023-06-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.3...v1.0.4)

**Merged pull requests:**

- feat: Add REST sensor category to attributes [\#40](https://github.com/geertmeersman/robonect/pull/40) ([geertmeersman](https://github.com/geertmeersman))
- docs: REST/MQTT priority and update explained [\#39](https://github.com/geertmeersman/robonect/pull/39) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.3](https://github.com/geertmeersman/robonect/tree/v1.0.3) (2023-06-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.3-beta.22...v1.0.3)

**Merged pull requests:**

- docs: Config flow images [\#38](https://github.com/geertmeersman/robonect/pull/38) ([geertmeersman](https://github.com/geertmeersman))
- fix: Beta workflow [\#37](https://github.com/geertmeersman/robonect/pull/37) ([geertmeersman](https://github.com/geertmeersman))
- docs: Discord beta channel webhook [\#36](https://github.com/geertmeersman/robonect/pull/36) ([geertmeersman](https://github.com/geertmeersman))
- fix: sensor coordinator update [\#35](https://github.com/geertmeersman/robonect/pull/35) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.3-beta.22](https://github.com/geertmeersman/robonect/tree/v1.0.3-beta.22) (2023-06-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.2...v1.0.3-beta.22)

**Closed issues:**

- Clear Error/StopDer  [\#28](https://github.com/geertmeersman/robonect/issues/28)

## [v1.0.2](https://github.com/geertmeersman/robonect/tree/v1.0.2) (2023-06-06)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.1...v1.0.2)

**Merged pull requests:**

- fix: Reset error button [\#34](https://github.com/geertmeersman/robonect/pull/34) ([geertmeersman](https://github.com/geertmeersman))
- docs: TOC Update README.md [\#33](https://github.com/geertmeersman/robonect/pull/33) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.1](https://github.com/geertmeersman/robonect/tree/v1.0.1) (2023-06-04)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v1.0.0...v1.0.1)

**Merged pull requests:**

- fix: convert attribute values [\#32](https://github.com/geertmeersman/robonect/pull/32) ([geertmeersman](https://github.com/geertmeersman))
- docs: TOC & daily mowing time sensor [\#31](https://github.com/geertmeersman/robonect/pull/31) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace EOD correction in card [\#30](https://github.com/geertmeersman/robonect/pull/30) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace example details on cards, references \#28 [\#29](https://github.com/geertmeersman/robonect/pull/29) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace mower card [\#27](https://github.com/geertmeersman/robonect/pull/27) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace mower card [\#26](https://github.com/geertmeersman/robonect/pull/26) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace mower card [\#25](https://github.com/geertmeersman/robonect/pull/25) ([geertmeersman](https://github.com/geertmeersman))
- docs: lovelace mower card [\#24](https://github.com/geertmeersman/robonect/pull/24) ([geertmeersman](https://github.com/geertmeersman))

## [v1.0.0](https://github.com/geertmeersman/robonect/tree/v1.0.0) (2023-06-02)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.2.6...v1.0.0)

**Breaking changes:**

- MQTT & Rest version [\#21](https://github.com/geertmeersman/robonect/pull/21) ([geertmeersman](https://github.com/geertmeersman))

**Closed issues:**

- Use mqtt as alternative to polling for faster response [\#18](https://github.com/geertmeersman/robonect/issues/18)

**Merged pull requests:**

- Bump actions/setup-python from 4.6.0 to 4.6.1 [\#23](https://github.com/geertmeersman/robonect/pull/23) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump ruff from 0.0.269 to 0.0.270 [\#22](https://github.com/geertmeersman/robonect/pull/22) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump ruff from 0.0.267 to 0.0.269 [\#20](https://github.com/geertmeersman/robonect/pull/20) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump danielchabr/pr-labels-checker from 3.2 to 3.3 [\#19](https://github.com/geertmeersman/robonect/pull/19) ([dependabot[bot]](https://github.com/apps/dependabot))
- Discord webhook [\#17](https://github.com/geertmeersman/robonect/pull/17) ([geertmeersman](https://github.com/geertmeersman))
- Bump danielchabr/pr-labels-checker from 3.1 to 3.2 [\#16](https://github.com/geertmeersman/robonect/pull/16) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump ruff from 0.0.265 to 0.0.267 [\#15](https://github.com/geertmeersman/robonect/pull/15) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v0.2.6](https://github.com/geertmeersman/robonect/tree/v0.2.6) (2023-05-12)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.2.5...v0.2.6)

**Merged pull requests:**

- Debug line fix & device renaming [\#14](https://github.com/geertmeersman/robonect/pull/14) ([geertmeersman](https://github.com/geertmeersman))

## [v0.2.5](https://github.com/geertmeersman/robonect/tree/v0.2.5) (2023-05-12)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.2.4...v0.2.5)

**Merged pull requests:**

- Reverting to 1 device [\#13](https://github.com/geertmeersman/robonect/pull/13) ([geertmeersman](https://github.com/geertmeersman))

## [v0.2.4](https://github.com/geertmeersman/robonect/tree/v0.2.4) (2023-05-12)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.2.3...v0.2.4)

**Merged pull requests:**

- Fault-memory index fix [\#12](https://github.com/geertmeersman/robonect/pull/12) ([geertmeersman](https://github.com/geertmeersman))

## [v0.2.3](https://github.com/geertmeersman/robonect/tree/v0.2.3) (2023-05-10)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.2.2...v0.2.3)

**Merged pull requests:**

- Check fault memory list size [\#11](https://github.com/geertmeersman/robonect/pull/11) ([geertmeersman](https://github.com/geertmeersman))

## [v0.2.2](https://github.com/geertmeersman/robonect/tree/v0.2.2) (2023-05-10)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.2.1...v0.2.2)

**Merged pull requests:**

- Set tracking and update\_interval to default when integration already … [\#10](https://github.com/geertmeersman/robonect/pull/10) ([geertmeersman](https://github.com/geertmeersman))

## [v0.2.1](https://github.com/geertmeersman/robonect/tree/v0.2.1) (2023-05-09)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.2.0...v0.2.1)

**Merged pull requests:**

- Don't bypass sleep :-\) [\#9](https://github.com/geertmeersman/robonect/pull/9) ([geertmeersman](https://github.com/geertmeersman))

## [v0.2.0](https://github.com/geertmeersman/robonect/tree/v0.2.0) (2023-05-09)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.1.5...v0.2.0)

**Merged pull requests:**

- Device split and config flow options added for sensor tracking [\#8](https://github.com/geertmeersman/robonect/pull/8) ([geertmeersman](https://github.com/geertmeersman))

## [v0.1.5](https://github.com/geertmeersman/robonect/tree/v0.1.5) (2023-05-09)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.1.4...v0.1.5)

**Merged pull requests:**

- Only update status entities when the mower is sleeping \(and prevent i… [\#7](https://github.com/geertmeersman/robonect/pull/7) ([geertmeersman](https://github.com/geertmeersman))

## [v0.1.4](https://github.com/geertmeersman/robonect/tree/v0.1.4) (2023-05-09)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.1.3...v0.1.4)

**Merged pull requests:**

- Timer fix when mowing [\#6](https://github.com/geertmeersman/robonect/pull/6) ([geertmeersman](https://github.com/geertmeersman))

## [v0.1.3](https://github.com/geertmeersman/robonect/tree/v0.1.3) (2023-05-08)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.1.2...v0.1.3)

**Merged pull requests:**

- Version, status, timer and hour sensors [\#5](https://github.com/geertmeersman/robonect/pull/5) ([geertmeersman](https://github.com/geertmeersman))

## [v0.1.2](https://github.com/geertmeersman/robonect/tree/v0.1.2) (2023-05-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.1.1...v0.1.2)

**Merged pull requests:**

- Robonect services & multiple sensors added [\#4](https://github.com/geertmeersman/robonect/pull/4) ([geertmeersman](https://github.com/geertmeersman))

## [v0.1.1](https://github.com/geertmeersman/robonect/tree/v0.1.1) (2023-05-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/v0.1.0...v0.1.1)

**Documentation:**

- Robonect icons & logos black color improved [\#3](https://github.com/geertmeersman/robonect/pull/3) ([geertmeersman](https://github.com/geertmeersman))
- Robonect icons & logos [\#2](https://github.com/geertmeersman/robonect/pull/2) ([geertmeersman](https://github.com/geertmeersman))

## [v0.1.0](https://github.com/geertmeersman/robonect/tree/v0.1.0) (2023-05-07)

[Full Changelog](https://github.com/geertmeersman/robonect/compare/bb21ea38eb224911822e39398ff7565352c92941...v0.1.0)

**Merged pull requests:**

- Initial version including battery sensors [\#1](https://github.com/geertmeersman/robonect/pull/1) ([geertmeersman](https://github.com/geertmeersman))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
