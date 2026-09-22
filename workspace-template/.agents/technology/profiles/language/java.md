---
name: Java
category: language
baselineVersion: 21 / 25 LTS
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 21 LTS
supportedVersions:
- 25 LTS
- 21 LTS
- 17 LTS
legacyVersions:
- 11 LTS
prohibitedVersions:
- < 11
sources:
- https://docs.oracle.com/en/java/
---
# Java Language Profile

## 1. Scope
Applies to modern Java applications, backend services, and libraries (Java 17 LTS, Java 21 LTS).

## 2. Detection Signals
- Files: `pom.xml`, `build.gradle`, `build.gradle.kts`, `*.java`

## 3. Supported-Version Policy
- Primary Target: Java 17 LTS and Java 21 LTS.
- Detect the project's declared version in `pom.xml` (`<java.version>`) or `build.gradle` (`sourceCompatibility`).

## 4. Documentation Sources
- Official: https://docs.oracle.com/en/java/

## 5. Core Architectural Guidance
- **Modern Language Idioms**:
  - Use `record` for immutable data transfer objects (DTOs), value objects, and internal carrier types.
  - Use sealed interfaces (`sealed interface`) with permits to model finite domain types and state machines.
  - Use pattern matching for `instanceof` and `switch` expressions for concise, type-safe branch handling.
  - Use text blocks (`"""`) for multiline SQL, JSON, or XML literals.
- **Concurrency**:
  - Leverage Virtual Threads (`Executors.newVirtualThreadPerTaskExecutor()`) on Java 21+ for high-concurrency I/O-bound workloads.
  - Use structured concurrency and scoped values where supported to manage task lifecycles safely.
- **Null Safety**:
  - Use `Optional<T>` as a return type for methods where absence is a valid domain outcome.
  - Avoid returning raw `null`; never pass `Optional` as method arguments or store in entity fields.
  - Annotate with `@NonNull` / `@Nullable` (Jakarta / SpotBugs) for static analysis.

## 6. Security Guidance
- Prevent Insecure Deserialization: Prohibit native Java object serialization (`ObjectInputStream`); use JSON (Jackson) with strict typing and polymorphic type handling disabled.
- Prevent SQL Injection: Use prepared statements or JPA named queries with bound parameters.
- Validate inputs using Jakarta Bean Validation (`@Valid`, `@NotNull`, `@Size`, `@Pattern`).

## 7. Performance Guidance
- Collection Choices: Use `ArrayList` for indexed access, `HashMap` for key-value lookups, and `ConcurrentHashMap` for thread-safe maps.
- Avoid Virtual Thread Pinning: Replace `synchronized` blocks around blocking socket I/O with `ReentrantLock`.
- JVM Memory Tuning: Configure initial and maximum heap (`-Xms`, `-Xmx`) and choose the appropriate GC (G1GC for standard services, ZGC for ultra-low latency).

## 8. Testing Guidance
- Unit Tests: JUnit 5 (`@Test`, `@ParameterizedTest`) with AssertJ (`assertThat(...)`) for fluent assertions.
- Mocking: Mockito (`@ExtendWith(MockitoExtension.class)`).
- Integration: Testcontainers for real database and message broker integration.

## 9. Common Anti-Patterns
- Using legacy `Vector`, `Hashtable`, or `StringBuffer`.
- Using raw collection types (`List` instead of `List<String>`).
- Catching `Exception` or `Throwable` and silently swallowing errors.
- Excessive defensive null checks when `Optional` or `@NonNull` contracts should govern.

## 10. Verification Commands
- Maven: `./mvnw compile` and `./mvnw test`
- Gradle: `./gradlew compileJava` and `./gradlew test`
