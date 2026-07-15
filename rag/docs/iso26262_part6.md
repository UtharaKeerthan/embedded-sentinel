# ISO 26262 Part 6 — Software Safety Requirements (Summary)

## ASIL Levels
- **QM** (Quality Management): No specific safety requirement.
- **ASIL-A**: Lowest safety integrity level. Basic software quality.
- **ASIL-B**: Moderate. Requires unit testing and static analysis.
- **ASIL-C**: High. Requires MC/DC coverage for all safety-relevant code.
- **ASIL-D**: Highest. Requires formal methods or diverse redundancy.

## ISP Pipeline ASIL Classifications (reference)
- **memory_pool.cpp**: ASIL-D — allocator failure crashes entire pipeline
- **demosaic.cpp**: ASIL-B — incorrect output affects driver perception
- **canny.cpp / sobel.cpp**: ASIL-B — used for lane detection preprocessing
- **auto_exposure.cpp**: ASIL-A — affects image quality, degraded gracefully
- **hist_equalize.cpp**: QM — enhancement only

## Software Requirements (Part 6 §8)
- Software shall be designed to achieve freedom from interference
- Shared memory shall be protected against concurrent access
- All software requirements shall be verifiable
- Test coverage shall meet ASIL-appropriate criteria:
  - ASIL-B: statement and branch coverage
  - ASIL-C/D: MC/DC (Modified Condition/Decision Coverage)
