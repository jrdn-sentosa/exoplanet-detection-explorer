# Cleaning report

## Source and row counts
- Raw file used: `data\raw\pscomppars_2026-11-03.csv`
- Download date: 2026-11-03
- Source URL: https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+%2A+from+pscomppars&format=csv
- Column documentation checked: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html (all 11 source columns documented for `pscomppars`)
- Raw rows: 6451; clean rows: 6451 (no planets dropped)
- Report generated: 2026-11-03; TOP_N_METHODS = 5

## Missing values per column (blank in the clean file)
| column | missing | percent |
|---|---|---|
| planet | 0 | 0.00% |
| host | 0 | 0.00% |
| method | 0 | 0.00% |
| year | 0 | 0.00% |
| facility | 0 | 0.00% |
| orbital_period_days | 354 | 5.49% |
| radius_earth | 50 | 0.78% |
| mass_earth | 30 | 0.47% |
| mass_source | 0 | 0.00% |
| equilibrium_temp_k | 540 | 8.37% |
| distance_pc | 28 | 0.43% |
| method_group | 0 | 0.00% |
| has_scatter_values | 0 | 0.00% |
| mass_is_estimated | 3035 | 47.05% |

## Numeric summary (non-missing values)
| column | n | min | median | max |
|---|---|---|---|---|
| year | 6451 | 1992 | 2016 | 2026 |
| orbital_period_days | 6097 | 0.0907063 | 10.6413 | 4.02e+08 |
| radius_earth | 6401 | 0.3098 | 2.86 | 87.2059 |
| mass_earth | 6421 | 0.02 | 9.32 | 12651.5 |
| equilibrium_temp_k | 5911 | 1.48 | 758 | 7777.78 |
| distance_pc | 6423 | 1.30119 | 349 | 8500 |

## Planets per method
| method | planets |
|---|---|
| Transit | 4785 |
| Radial Velocity | 1204 |
| Microlensing | 292 |
| Imaging | 98 |
| Transit Timing Variations | 29 |
| Eclipse Timing Variations | 17 |
| Orbital Brightness Modulation | 9 |
| Pulsar Timing | 8 |
| Astrometry | 6 |
| Pulsation Timing Variations | 2 |
| Disk Kinematics | 1 |

## Planets per method_group (named groups: Transit, Radial Velocity, Microlensing, Imaging, Transit Timing Variations)
| method_group | planets |
|---|---|
| Transit | 4785 |
| Radial Velocity | 1204 |
| Microlensing | 292 |
| Imaging | 98 |
| Other | 43 |
| Transit Timing Variations | 29 |

## Discovery year range
1992 to 2026

## Scatterplot (orbital period vs radius)
- Can appear (has_scatter_values = true): **6050**
- Omitted: **401**
  - missing period only: 351
  - missing radius only: 47
  - missing both: 3
  - period <= 0 (any radius): 0
  - radius <= 0 (any period): 0
  (categories 4 and 5 may overlap with each other; 1-3 are exclusive of them.)

## Log-scale problems (flagged, not changed)
- None: no zero or negative values in any numeric column.

## Duplicate planet names (reported, NOT removed)
- None found (exact or case-insensitive).
- Blank planet names: 0

## mass_is_estimated
Docs (pl_bmassprov): `Mass` = measured mass; `Msini/sini` = true mass computed from a minimum mass plus inclination; `Msini` = minimum mass from radial velocity, no inclination correction.
- Counted as estimated (true): ['Msini'] — a lower limit, not a true mass.
- Counted as not estimated (false): ['Mass', 'Msin(i)/sin(i)', 'Msini/sini']
- Left BLANK: any other value, e.g. `M-R relationship` (present in the data but NOT in the docs page checked; it is probably a mass modelled from radius, but I did not assume that). **Decision needed.**
| mass_source | planets |
|---|---|
| M-R relationship | 3035 |
| Mass | 2477 |
| Msini | 924 |
| Msin(i)/sin(i) | 15 |

mass_is_estimated: true=924, false=2492, blank=3035

## Spot checks (raw vs clean)
**51 Peg b**

| clean column | raw value | clean value | match |
|---|---|---|---|
| host | 51 Peg | 51 Peg | yes |
| method | Radial Velocity | Radial Velocity | yes |
| year | 1995 | 1995 | yes |
| facility | Haute-Provence Observatory | Haute-Provence Observatory | yes |
| orbital_period_days | 4.23079660000 | 4.2307966 | yes |
| radius_earth | 14.10000000 | 14.1 | yes |
| mass_earth | 193.87532827 | 193.87532827 | yes |
| mass_source | Mass | Mass | yes |
| equilibrium_temp_k | 1328.93 | 1328.93 | yes |
| distance_pc | 15.46140000 | 15.4614 | yes |

**Kepler-22 b**

| clean column | raw value | clean value | match |
|---|---|---|---|
| host | Kepler-22 | Kepler-22 | yes |
| method | Transit | Transit | yes |
| year | 2011 | 2011 | yes |
| facility | Kepler | Kepler | yes |
| orbital_period_days | 289.86387600000 | 289.863876 | yes |
| radius_earth | 2.10000000 | 2.1 | yes |
| mass_earth | 9.10000000 | 9.1 | yes |
| mass_source | Mass | Mass | yes |
| equilibrium_temp_k | 279.00 | 279.0 | yes |
| distance_pc | 194.64200000 | 194.642 | yes |

**TRAPPIST-1 e**

| clean column | raw value | clean value | match |
|---|---|---|---|
| host | TRAPPIST-1 | TRAPPIST-1 | yes |
| method | Transit | Transit | yes |
| year | 2017 | 2017 | yes |
| facility | Multiple Observatories | Multiple Observatories | yes |
| orbital_period_days | 6.10101300000 | 6.101013 | yes |
| radius_earth | 0.92000000 | 0.92 | yes |
| mass_earth | 0.69200000 | 0.692 | yes |
| mass_source | Mass | Mass | yes |
| equilibrium_temp_k | 249.70 | 249.7 | yes |
| distance_pc | 12.42988881 | 12.42988881 | yes |

**Proxima Cen b**

| clean column | raw value | clean value | match |
|---|---|---|---|
| host | Proxima Cen | Proxima Cen | yes |
| method | Radial Velocity | Radial Velocity | yes |
| year | 2016 | 2016 | yes |
| facility | European Southern Observatory | European Southern Observatory | yes |
| orbital_period_days | 11.18465000000 | 11.18465 | yes |
| radius_earth | 1.02000000 | 1.02 | yes |
| mass_earth | 1.05500000 | 1.055 | yes |
| mass_source | Msini | Msini | yes |
| equilibrium_temp_k | 218.00 | 218.0 | yes |
| distance_pc | 1.30119000 | 1.30119 | yes |

**WASP-47 c**

| clean column | raw value | clean value | match |
|---|---|---|---|
| host | WASP-47 | WASP-47 | yes |
| method | Radial Velocity | Radial Velocity | yes |
| year | 2015 | 2015 | yes |
| facility | La Silla Observatory | La Silla Observatory | yes |
| orbital_period_days | 589.57000000000 | 589.57 | yes |
| radius_earth | (blank) | (blank) | yes |
| mass_earth | 447.00000000 | 447.0 | yes |
| mass_source | Mass | Mass | yes |
| equilibrium_temp_k | 247.00 | 247.0 | yes |
| distance_pc | 264.78000000 | 264.78 | yes |

## Anything unusual / uncertain
- OPEN QUESTION: `mass_source = 'M-R relationship'` is undocumented on the column page, so mass_is_estimated is blank for those planets.
- Max orbital_period_days = 4.02e+08 (COCONUTS-2 b); extreme but positive, left as is.
- Judgement call: `Msini/sini` is treated as NOT estimated (it is a derived true mass). Say if you'd rather count it.
- Judgement call: `mass_earth` mixes true masses and minimum masses; use mass_is_estimated/mass_source before comparing.
- Judgement call: `year` typed O in the dictionary; method_group is blank where method is blank.
- All non-blank numeric cells parsed cleanly.
