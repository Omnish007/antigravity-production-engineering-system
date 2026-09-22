---
name: Spring Boot
category: backend
baselineVersion: 3.x / 4.x
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 3.3.x
supportedVersions:
- 3.3.x
- 3.2.x
- 3.4.x
- 4.x
legacyVersions:
- 3.0.x
- 3.1.x
prohibitedVersions:
- < 3.0
sources:
- https://spring.io/projects/spring-boot
---
# Spring Boot Technology Profile

## 1. Scope
Applies to JVM enterprise services, REST APIs, and microservices built with Spring Boot (Spring Boot 3.x and 4.x on Java or Kotlin).

## 2. Detection Signals
- Files: `pom.xml`, `build.gradle`, `build.gradle.kts`
- Dependencies / Plugins: `org.springframework.boot`

## 3. Supported-Version Policy
- Primary Target: Spring Boot 3.x / 4.x.
- Java Version Compatibility:
  - Spring Boot 3.x: Requires Java 17 minimum; supports Java 21 LTS.
  - Spring Boot 4.x: Requires Java 17 minimum; supports up to Java 26.
- Version Discovery: Detect the project's declared Java version from `pom.xml` (`<java.version>`) or `build.gradle` (`sourceCompatibility`) and validate compatibility against the active Spring Boot release line. Do not enforce Java 21 as a universal requirement unless selected by the project.

## 4. Documentation Sources
- Official: https://spring.io/projects/spring-boot

## 5. Core Architectural Guidance
- **Layered Boundary Architecture**:
  - **Web / API Layer**: `@RestController` with explicit request/response DTOs (using immutable Java records).
  - **Service Layer**: `@Service` containing pure business logic and transaction boundaries (`@Transactional`).
  - **Data / Repository Layer**: `@Repository` interfaces extending `JpaRepository` or `CrudRepository`.
- **Dependency Injection**:
  - Use constructor injection exclusively (facilitated by Lombok `@RequiredArgsConstructor` or explicit constructors).
  - Never use field injection (`@Autowired` on private fields), which hinders unit testing and violates encapsulation.
- **Concurrency & Virtual Threads**:
  - For I/O-bound applications on Java 21+, enable Virtual Threads via `spring.threads.virtual.enabled=true`.
  - Avoid thread pinning in Virtual Threads by replacing `synchronized` blocks with `ReentrantLock` around blocking I/O.

## 6. Security Guidance
- Configure Spring Security using component-based `SecurityFilterChain` beans (avoid legacy `WebSecurityConfigurerAdapter`).
- Enforce method-level security with `@EnableMethodSecurity` and `@PreAuthorize("hasRole('...')")`.
- Store configuration secrets in environment variables or vault services; never hardcode credentials in `application.yml` or `application.properties`.
- Use parameterized JPA queries (`@Query` with named parameters) or Spring Data derived queries to prevent SQL injection.

## 7. Performance Guidance
- **Database Access & Connection Pooling**:
  - Configure HikariCP with bounded maximum pool sizes aligned with database capacity.
  - Use `@Transactional(readOnly = true)` for read-only queries to disable Hibernate dirty-checking overhead.
  - Solve the N+1 select problem by using `JOIN FETCH` queries, Entity Graphs (`@EntityGraph`), or DTO projections.
- **Batch Processing**:
  - Enable Hibernate batching for bulk inserts/updates: `spring.jpa.properties.hibernate.jdbc.batch_size=50`.

## 8. Testing Guidance
- Unit Tests: JUnit 5 (`@ExtendWith(MockitoExtension.class)`) with Mockito for isolated service-layer testing.
- Web Slice Tests: `@WebMvcTest` for controller validation, input constraint checks, and mock MVC assertions.
- Integration Tests: `@SpringBootTest` with **Testcontainers** for real database and cache integration testing.

## 9. Common Anti-Patterns
- Using field injection (`@Autowired private FooService fooService`).
- Executing external HTTP requests or heavy computation inside `@Transactional` database methods.
- Using `FetchType.EAGER` on `@OneToMany` or `@ManyToMany` JPA relationships.
- Committing active profiles or passwords in `application-*.yml` files.

## 10. Verification Commands
- Maven:
  - Test: `./mvnw test`
  - Package: `./mvnw clean package -DskipTests=false`
- Gradle:
  - Test: `./gradlew test`
  - Build: `./gradlew build`
