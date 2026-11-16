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
| mass_type | 30 | 0.47% |
| mass_is_estimated | 30 | 0.47% |
| radius_reference | 50 | 0.78% |
| radius_is_estimated | 50 | 0.78% |

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

## Mass type and mass_is_estimated
Mapping from mass_source (any other non-blank value stops the script): `Mass` -> measured, `Msin(i)/sin(i)` -> derived_from_inclination, `Msini` -> minimum_mass, `M-R relationship` -> estimated. Blank when mass_earth is missing.
| mass_type | planets |
|---|---|
| estimated | 3035 |
| measured | 2477 |
| minimum_mass | 894 |
| (blank: mass missing) | 30 |
| derived_from_inclination | 15 |

mass_is_estimated: true=3035, false=3386, blank=30

## Radius: radius_is_estimated
Identified by the radius reference column `pl_rade_reflink`: the archive writes 'Calculated Value' there when it computed a radius itself (for planets with a mass but no published radius, using the Chen & Kipping 2017 mass-radius relation; archive docs: https://exoplanetarchive.ipac.caltech.edu/docs/pscp_calc.html). true = reference is 'Calculated Value'; false = any other reference; blank = radius missing. Note: 'false' means published by a source, which may itself include model-based values.
| radius_is_estimated | planets |
|---|---|
| false | 4862 |
| true | 1539 |
| (blank: radius missing) | 50 |

### Method by radius_is_estimated
| method | true | false | (radius missing) | total |
|---|---|---|---|---|
| Transit | 2 | 4782 | 1 | 4785 |
| Radial Velocity | 1134 | 33 | 37 | 1204 |
| Microlensing | 292 | 0 | 0 | 292 |
| Imaging | 53 | 41 | 4 | 98 |
| Transit Timing Variations | 25 | 3 | 1 | 29 |
| Eclipse Timing Variations | 15 | 0 | 2 | 17 |
| Orbital Brightness Modulation | 3 | 3 | 3 | 9 |
| Pulsar Timing | 6 | 0 | 2 | 8 |
| Astrometry | 6 | 0 | 0 | 6 |
| Pulsation Timing Variations | 2 | 0 | 0 | 2 |
| Disk Kinematics | 1 | 0 | 0 | 1 |

### Scatterplot planets by radius type
- Measured/published radius (radius_is_estimated = false): 4834
- Estimated radius (radius_is_estimated = true): 1216
- Total on scatterplot: 6050

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
- `M-R relationship` is not listed in the archive's pl_bmassprov column docs, but you specified it as 'estimated'; it is used as such.
- Planets with mass missing: 30 (all blank mass_type / mass_is_estimated).
- Radius present but reference blank: 0 (radius_is_estimated left blank for these).
- Max orbital_period_days = 4.02e+08 (COCONUTS-2 b); extreme but positive, left as is.
- `mass_earth` mixes measured, derived and minimum masses; use mass_type before comparing.
- Judgement call: `year` typed O in the dictionary; method_group is blank where method is blank.
- All non-blank numeric cells parsed cleanly.
