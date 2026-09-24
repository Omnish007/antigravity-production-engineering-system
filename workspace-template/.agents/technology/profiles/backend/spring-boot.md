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

The structure below is the profile's preferred boundary pattern. Follow the project's accepted architecture and ADRs when they intentionally use a different valid structure.
- **Preferred Boundary Structure (RULE-ARCH-LAYER-001)**:
  - **Controllers (`@RestController`)**: Thin HTTP entry points. Accept `@Valid` DTO records, delegate to `@Service`, and return `ResponseEntity<T>`. Querying repositories or databases directly inside controllers is STRICTLY FORBIDDEN.
  - **Services (`@Service`)**: Contain domain business logic, workflow rules, validation, and transaction boundaries (`@Transactional`). Completely decoupled from `HttpServletRequest` or `HttpServletResponse`.
  - **Repositories (`@Repository`)**: Spring Data JPA repositories or custom persistence implementations. Encapsulate all database queries and projections.
  - **DTOs / Contracts**: Immutable Java records with Jakarta Bean Validation annotations (`@NotNull`, `@Email`, `@Size`).
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

## 9. Common Anti-Patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Repository Access in Controllers
```java
// ❌ FORBIDDEN: Injecting repository directly into controller
@RestController
@RequestMapping("/users")
public class UserController {
    @Autowired
    private UserRepository userRepository; // VIOLATION: Bypassing service layer!

    @PostMapping
    public User create(@RequestBody User user) {
        return userRepository.save(user); // VIOLATION: Database query in controller!
    }
}
```

### FORBIDDEN: HttpServletRequest/Response in Service Layer
```java
// ❌ FORBIDDEN: Passing HttpServletRequest into Service
@Service
public class UserService {
    public void register(HttpServletRequest request) { // VIOLATION: Transport coupling!
        String token = request.getHeader("Authorization");
    }
}
```

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
- Architecture Check: `python3 .agents/validation/check-architecture.py`

## 11. Standard Layered Code Blueprint

```java
// 1. DTO Record (src/main/java/com/example/dto/CreateUserRequest.java)
public record CreateUserRequest(
    @NotBlank @Email String email,
    @NotBlank @Size(min = 2) String name
) {}

public record UserResponse(UUID id, String email, String name) {}

// 2. Repository Layer (src/main/java/com/example/repository/UserRepository.java)
@Repository
public interface UserRepository extends JpaRepository<UserEntity, UUID> {
    Optional<UserEntity> findByEmail(String email);
}

// 3. Service Layer (src/main/java/com/example/service/UserService.java)
@Service
@Transactional
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public UserResponse register(CreateUserRequest request) {
        if (userRepository.findByEmail(request.email()).isPresent()) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Email exists");
        }
        UserEntity entity = new UserEntity(request.email(), request.name());
        UserEntity saved = userRepository.save(entity);
        return new UserResponse(saved.getId(), saved.getEmail(), saved.getName());
    }
}

// 4. Controller Layer (src/main/java/com/example/controller/UserController.java)
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping
    public ResponseEntity<UserResponse> register(@Valid @RequestBody CreateUserRequest request) {
        UserResponse response = userService.register(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
```
