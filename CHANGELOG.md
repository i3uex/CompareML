# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2022-02-15

### Added

- Favicon.

### Changed

- Use relative URLs.

## [1.0.0] - 2021-08-03

This release matches the version published at [IJIMAI Journal][ijimai].

[ijimai]: https://www.ijimai.org/journal/bibcite/reference/2982 "CompareML: A Novel Approach to Supporting Preliminary Data Analysis Decision Making"

### Added

- Journal information in footer.
- Citation information in footer.
- [CFF][cff] citation file.
- Show R2 in regression. 
- Requirements file (requirements.txt) for the libraries the project needs.

[cff]: https://citation-file-format.github.io

### Fixed

- Not supported algorithm is now notified as error.
- Javascript Scikit's `getPrecision()` and `getRecall()` only worked with sample dataset **mushroom**.
- Disabled start button no longer calls submit method.
