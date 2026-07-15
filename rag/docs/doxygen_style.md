# Doxygen Documentation Style Guide — embedded-isp-pipeline

## Mandatory tags for every public function
- @brief: One-line description (imperative mood: "Converts...", "Applies...")
- @param: One entry per parameter (name and purpose)
- @return: Return value meaning, including error codes
- @req: One entry per SRS requirement this function implements

## Example compliant comment
```cpp
/**
 * @brief Converts raw Bayer RGGB buffer to interleaved RGB output.
 * @details Uses bilinear interpolation. All arithmetic is fixed-point.
 * @req REQ-ISP-001
 * @req REQ-ISP-002
 * @param bayer  Input Bayer buffer (uint16_t, RGGB pattern, row-major)
 * @param rgb    Output RGB buffer (uint8_t, pre-allocated by caller)
 * @param width  Frame width in pixels
 * @param height Frame height in pixels
 * @return IspError::OK on success, IspError::NULL_BUFFER if pointers are null
 */
IspError demosaic_rggb(const uint16_t* bayer, uint8_t* rgb,
                        uint16_t width, uint16_t height);
```

## Test case tags (in test files)
- @tc: Test case ID (e.g. TC-ISP-001)
- @covers: The REQ-ID this test validates
