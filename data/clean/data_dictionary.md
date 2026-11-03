# Data dictionary

Type: N = nominal, O = ordinal, Q = quantitative. Source: NASA Exoplanet Archive `pscomppars` ([column docs](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)). Blank cell = missing in the archive (never filled).

| Column | Meaning | Unit | Type | Source column |
|---|---|---|---|---|
| planet | Planet name most commonly used in the literature | - | N | `pl_name` |
| host | Host star name most commonly used in the literature | - | N | `hostname` |
| method | Method by which the planet was first identified | - | N | `discoverymethod` |
| year | Year the planet was discovered | year | O | `disc_year` |
| facility | Facility that made the discovery observations | - | N | `disc_facility` |
| orbital_period_days | Time to complete one orbit | days | Q | `pl_orbper` |
| radius_earth | Planet radius | Earth radii | Q | `pl_rade` |
| mass_earth | Best available mass (true mass, else M*sin(i)/sin(i), else M*sin(i)); see mass_source | Earth masses | Q | `pl_bmasse` |
| mass_source | Provenance of the best mass (Mass, Msini, Msini/sini) | - | N | `pl_bmassprov` |
| equilibrium_temp_k | Equilibrium temperature (black-body, heated by host star only) | K | Q | `pl_eqt` |
| distance_pc | Distance to the planetary system | parsecs | Q | `sy_dist` |
| method_group | Top 5 discovery methods by planet count; all others labelled 'Other' | - | N | derived from `method` |
| has_scatter_values | true only if orbital period AND radius are both > 0 (usable on a log-log scatterplot) | - | N | derived from `orbital_period_days, radius_earth` |
| mass_is_estimated | true if mass_source is 'Msini' (minimum mass only, not a true mass); false for 'Mass' and 'Msin(i)/sin(i)'; blank for undocumented values such as 'M-R relationship' | - | N | derived from `mass_source` |

Notes: `year` is typed O (ordered, discrete); treat as Q if you want a continuous axis. Booleans are written as `true`/`false`.
