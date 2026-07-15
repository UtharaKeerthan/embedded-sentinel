# Requirements Specification — embedded-isp-pipeline (RAG copy)
<!-- This is a copy of requirements/SRS.md for use by EmbedSentinel RAG agents -->

REQ-ISP-001: Pipeline shall convert RGGB Bayer input to RGB output
REQ-ISP-002: No dynamic memory allocation (no malloc / no new)
REQ-ISP-003: Shall support 1920x1080 resolution
REQ-ISP-004: Per-frame processing latency shall not exceed 33ms
REQ-WB-001: Shall apply independent gain per R, G, B channel
REQ-WB-002: Gray world algorithm shall be the default mode
REQ-GAMMA-001: Shall use LUT-based gamma correction
REQ-GAMMA-002: Gamma value configurable in range 1.0 to 3.0
REQ-EDGE-001: Sobel shall output gradient magnitude and direction
REQ-EDGE-002: Canny shall implement non-maximum suppression
REQ-EDGE-003: Canny hysteresis thresholds shall be configurable
REQ-COLOR-001: CCM shall apply 3x3 matrix in Q4.12 fixed-point
REQ-COLOR-002: RGB to YUV conversion shall use BT.709 coefficients
REQ-HIST-001: Per-channel histogram over 256 bins
REQ-AE-001: Auto-exposure convergence within 10 frames
REQ-DPC-001: Dead pixels replaced using 4-neighbour median
REQ-RESIZE-001: Bilinear interpolation shall be used for scaling
REQ-MEM-001: Stack usage per function shall not exceed 4096 bytes
