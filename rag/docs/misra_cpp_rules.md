# MISRA C++:2008 — Key Rules for Embedded ISP Pipeline

## Mandatory Rules (must not be violated)
- **18-4-1**: The allocation functions malloc, calloc, realloc and free shall not be used.
  Rationale: Heap fragmentation causes non-deterministic behavior in embedded systems.
- **15-0-1**: Exceptions shall only be used for error handling.
  In practice: -fno-exceptions means exceptions are completely banned in this codebase.
- **0-1-1**: A project shall not contain unreachable code.

## Required Rules (should not be violated without documented deviation)
- **5-0-8**: An explicit integral or floating-point conversion shall not increase the size
  of the underlying type of a cvalue expression.
- **7-5-4**: Functions shall not call themselves, either directly or indirectly.
  Rationale: Stack depth on embedded systems must be bounded and deterministic.
- **6-4-1**: An if (condition) construct shall be followed by a compound statement.
  The else keyword shall be followed by either a compound statement, or another if statement.
- **5-0-3**: A cvalue expression shall not be implicitly converted to a different underlying type.
- **16-2-1**: The pre-processor shall only be used for file inclusion and include guards.

## Advisory Rules (best practice)
- **0-1-2**: A project shall not contain infeasible paths.
- **5-2-12**: An identifier with array type passed as a function argument shall not decay to a pointer.
