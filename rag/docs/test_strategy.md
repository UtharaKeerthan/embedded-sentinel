# Testing Strategy — embedded-isp-pipeline

## Test levels
1. **Unit tests** (tests/unit/): One test file per source module.
   Each public function must have at minimum:
   - Happy path test with valid input
   - Null pointer test (expect IspError::NULL_BUFFER)
   - Boundary value test (min/max resolution, edge pixel values)

2. **Integration tests** (tests/integration/):
   - Full pipeline end-to-end on a synthetic Bayer frame
   - Performance test verifying 33ms latency budget (REQ-ISP-004)

## Test ID naming convention
TC-{MODULE}-{NUMBER}
- TC-ISP-001: Demosaic basic conversion
- TC-WB-001:  White balance gain application
- TC-GAMMA-001: Gamma LUT apply
- TC-EDGE-001: Sobel edge detection
- TC-MEM-001: Memory pool alloc/reset

## Coverage targets (per ASIL level)
- ASIL-D modules (memory_pool): 100% MC/DC coverage
- ASIL-B modules (demosaic, canny): 100% branch coverage
- ASIL-A modules (auto_exposure): 80% statement coverage
- QM modules: best effort
